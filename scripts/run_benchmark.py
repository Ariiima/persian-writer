#!/usr/bin/env python3
"""
run_benchmark.py — Automated Benchmark & Blind Pairwise A/B Evaluator for persian-writer.

Runs the golden tasks in `evals/evals.json` through Claude under two configurations:
  - Baseline / v0 (without skill or with a baseline SKILL.md)
  - Candidate / v1 (with the current SKILL.md + fa_check.py self-repair pass)

Grades every output using:
  1. Deterministic Linter (`scripts/fa_check.py`): hard error count, warning count, pass rate.
  2. Blind Pairwise Judge (Gemini 3.1 Pro): randomized A/B order, 1-5 scores across
     Anti-Calque Syntax, Register Purity, Orthography, and Task Fidelity.

Usage:
  python3 scripts/run_benchmark.py --baseline /tmp/v0_SKILL.md --out evals/latest_benchmark.json
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fa_check import analyze_text, safe_fix_text  # noqa: E402


def call_claude(system_prompt: str, user_prompt: str, model: str = "claude-sonnet-4-5") -> str:
    """Call Claude via Mana router (if available) or ANTHROPIC_API_KEY."""
    try:
        import mana_router
        an = mana_router.provider("anthropic")
        url = an.url + "/v1/messages"
        headers = dict(an.headers)
    except Exception:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise RuntimeError("Neither mana_router nor ANTHROPIC_API_KEY is available.")
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    payload = {
        "model": model,
        "max_tokens": 1500,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    if system_prompt:
        payload["system"] = system_prompt

    for attempt in range(3):
        r = requests.post(url, headers=headers, json=payload, allow_redirects=False, timeout=60)
        if r.status_code == 200:
            data = r.json()
            return "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text").strip()
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Claude call failed ({r.status_code}): {r.text[:300]}")


def call_gemini_judge(prompt: str, model: str = "gemini-3.1-pro-preview") -> Dict:
    """Call Gemini 3.1 Pro as a blind pairwise judge returning structured JSON."""
    try:
        import mana_router
        gm = mana_router.provider("gemini")
        url = f"{gm.url}/models/{model}:generateContent"
        headers = dict(gm.headers)
        params = {}
    except Exception:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise RuntimeError("Neither mana_router nor GEMINI_API_KEY is available.")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        headers = {"content-type": "application/json"}
        params = {"key": api_key}

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.0,
            "responseMimeType": "application/json",
        },
    }
    for attempt in range(3):
        r = requests.post(url, headers=headers, params=params, json=payload, allow_redirects=False, timeout=60)
        if r.status_code == 200:
            text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text)
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Gemini judge failed ({r.status_code}): {r.text[:300]}")


def run_v1_with_verification(skill_system: str, user_prompt: str, expected_register: str, model: str) -> Tuple[str, int]:
    """Run Claude with the v1 skill + deterministic fa_check.py verification loop (max 1 repair turn)."""
    draft = call_claude(skill_system, user_prompt, model=model)
    draft = safe_fix_text(draft)
    rep = analyze_text(draft, expected_register=expected_register)
    repairs = 0
    if not rep["ok"] or rep["warning_count"] > 0:
        issue_lines = "\n".join(
            f"- [{i['severity'].upper()}] {i['category']}: «{i['match']}» -> {i['message']}"
            for i in rep["issues"]
        )
        repair_prompt = (
            f"{user_prompt}\n\n"
            f"---\n"
            f"پیش‌نویس قبلی شما این موارد را در اسکریپت بررسی نگارش (`fa_check.py`) نقض کرده است:\n"
            f"{issue_lines}\n\n"
            f"لطفاً پیش‌نویس زیر را طوری بازنویسی کن که همهٔ این خطاها برطرف شوند و فقط متن نهایی را برگردان:\n\n{draft}"
        )
        draft = call_claude(skill_system, repair_prompt, model=model)
        draft = safe_fix_text(draft)
        repairs = 1
    return draft, repairs


def evaluate_case(case: Dict, v0_system: str, v1_system: str, model: str) -> Dict:
    cid = case["id"]
    name = case["name"]
    prompt = case["prompt"]
    reg = case.get("expected_register", "auto")

    # 1. Generate v0 (baseline skill) and v1 (new skill + fa_check gate)
    v0_out = call_claude(v0_system, prompt, model=model)
    v1_out, repairs = run_v1_with_verification(v1_system, prompt, reg, model=model)

    # 2. Score both with deterministic linter
    v0_lint = analyze_text(v0_out, expected_register=reg)
    v1_lint = analyze_text(v1_out, expected_register=reg)

    # 3. Blind Pairwise Judge with deterministic randomized order based on case id
    flip = int(hashlib.md5(name.encode()).hexdigest(), 16) % 2 == 1
    cand_a, cand_b = (v1_out, v0_out) if flip else (v0_out, v1_out)
    label_a, label_b = ("v1", "v0") if flip else ("v0", "v1")

    judge_prompt = f"""تو یک داور و ویراستار ارشد زبان فارسی هستی. دو متن «A» و «B» را که در پاسخ به یک درخواست نوشته شده‌اند، به‌صورت کور (بدون اطلاع از نویسنده) مقایسه و داوری کن.

درخواست کاربر:
{prompt}

رجیستر مورد انتظار: {reg}
معیارهای مورد انتظار:
{json.dumps(case.get("expectations", []), ensure_ascii=False)}

--- متن A ---
{cand_a}

--- متن B ---
{cand_b}

به هر متن در ۴ محور زیر از ۱ تا ۵ نمره بده (۵ = عالی و کاملاً طبیعی در فارسی؛ ۱ = پر از خطا یا ترجمه‌زدگی):
1. natural_syntax: طبیعی بودن ساختار جمله و نبودن گرته‌برداری از انگلیسی (ضد ترجمه‌زدگی)
2. register_purity: تناسب لحن با مقصد متن و یکدستی کامل رجیستر (کتابی در برابر شکسته، نبودن «می‌باشد/گردید»)
3. orthography: رعایت دستور خط فرهنگستان (نیم‌فاصله، ی و ک، نبودن هکسره و تنوین جعلی، اعداد و علائم نگارشی فارسی)
4. fidelity: وفاداری کامل به اطلاعات و خواستهٔ کاربر

خروجی را دقیقاً با این ساختار JSON برگردان:
{{
  "score_A": {{"natural_syntax": int, "register_purity": int, "orthography": int, "fidelity": int}},
  "score_B": {{"natural_syntax": int, "register_purity": int, "orthography": int, "fidelity": int}},
  "winner": "A" | "B" | "tie",
  "reason_fa": "توضیح کوتاه و دقیق در یک یا دو جمله درباره دلیل برتری"
}}"""

    judge_raw = call_gemini_judge(judge_prompt)
    raw_winner = judge_raw.get("winner", "tie")
    if raw_winner == "A":
        winner = label_a
    elif raw_winner == "B":
        winner = label_b
    else:
        winner = "tie"

    scores_v0 = judge_raw["score_B" if flip else "score_A"]
    scores_v1 = judge_raw["score_A" if flip else "score_B"]

    return {
        "id": cid,
        "name": name,
        "expected_register": reg,
        "v0_output": v0_out,
        "v1_output": v1_out,
        "v1_repairs": repairs,
        "v0_lint": {
            "ok": v0_lint["ok"],
            "errors": v0_lint["error_count"],
            "warnings": v0_lint["warning_count"],
            "issues": v0_lint["issues"],
        },
        "v1_lint": {
            "ok": v1_lint["ok"],
            "errors": v1_lint["error_count"],
            "warnings": v1_lint["warning_count"],
            "issues": v1_lint["issues"],
        },
        "judge": {
            "winner": winner,
            "v0_scores": scores_v0,
            "v1_scores": scores_v1,
            "v0_avg": round(sum(scores_v0.values()) / 4.0, 2),
            "v1_avg": round(sum(scores_v1.values()) / 4.0, 2),
            "reason_fa": judge_raw.get("reason_fa", ""),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run persian-writer benchmark suite.")
    parser.add_argument("--baseline", default="", help="Path to baseline SKILL.md (empty = raw Claude with no skill)")
    parser.add_argument("--skill", default=str(ROOT / "SKILL.md"), help="Path to candidate SKILL.md")
    parser.add_argument("--evals", default=str(ROOT / "evals" / "evals.json"), help="Path to evals.json")
    parser.add_argument("--model", default="claude-sonnet-4-5", help="Claude model ID")
    parser.add_argument("--out", default=str(ROOT / "evals" / "latest_benchmark.json"), help="Output JSON report path")
    args = parser.parse_args()

    v0_system = Path(args.baseline).read_text(encoding="utf-8") if args.baseline and Path(args.baseline).exists() else ""
    v1_system = Path(args.skill).read_text(encoding="utf-8")
    # Also append key reference tables so single-turn API calls have the full skill context
    for ref_name in ("registers.md", "anti-calque-and-style.md", "orthography-1401.md", "ui-and-microcopy.md"):
        ref_path = ROOT / "references" / ref_name
        if ref_path.exists():
            v1_system += f"\n\n---\n\n{ref_path.read_text(encoding='utf-8')}"

    eval_cases = json.loads(Path(args.evals).read_text(encoding="utf-8"))["evals"]
    print(f"Running {len(eval_cases)} benchmark cases on {args.model}...")

    results: List[Dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(evaluate_case, c, v0_system, v1_system, args.model): c for c in eval_cases}
        for fut in concurrent.futures.as_completed(futs):
            res = fut.result()
            results.append(res)
            print(
                f"  Case #{res['id']} ({res['name']}): "
                f"v0 lint={res['v0_lint']['errors']}E/{res['v0_lint']['warnings']}W (judge {res['judge']['v0_avg']}) | "
                f"v1 lint={res['v1_lint']['errors']}E/{res['v1_lint']['warnings']}W (judge {res['judge']['v1_avg']}) "
                f"-> Winner: {res['judge']['winner'].upper()}"
            )

    results.sort(key=lambda x: x["id"])

    v0_total_err = sum(r["v0_lint"]["errors"] for r in results)
    v1_total_err = sum(r["v1_lint"]["errors"] for r in results)
    v0_total_warn = sum(r["v0_lint"]["warnings"] for r in results)
    v1_total_warn = sum(r["v1_lint"]["warnings"] for r in results)
    v0_pass = sum(1 for r in results if r["v0_lint"]["ok"])
    v1_pass = sum(1 for r in results if r["v1_lint"]["ok"])
    v1_wins = sum(1 for r in results if r["judge"]["winner"] == "v1")
    v0_wins = sum(1 for r in results if r["judge"]["winner"] == "v0")
    ties = sum(1 for r in results if r["judge"]["winner"] == "tie")
    v0_mean_score = round(sum(r["judge"]["v0_avg"] for r in results) / len(results), 2)
    v1_mean_score = round(sum(r["judge"]["v1_avg"] for r in results) / len(results), 2)

    summary = {
        "model": args.model,
        "judge_model": "gemini-3.1-pro-preview",
        "total_cases": len(results),
        "v0_lint_pass_rate": f"{v0_pass}/{len(results)}",
        "v1_lint_pass_rate": f"{v1_pass}/{len(results)}",
        "v0_total_errors": v0_total_err,
        "v1_total_errors": v1_total_err,
        "v0_total_warnings": v0_total_warn,
        "v1_total_warnings": v1_total_warn,
        "v0_judge_mean_score": v0_mean_score,
        "v1_judge_mean_score": v1_mean_score,
        "pairwise_record": {"v1_wins": v1_wins, "v0_wins": v0_wins, "ties": ties},
        "cases": results,
    }

    Path(args.out).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n=== BENCHMARK SUMMARY ===")
    print(f"Linter Pass Rate: v0={v0_pass}/{len(results)} ({v0_total_err}E, {v0_total_warn}W) vs v1={v1_pass}/{len(results)} ({v1_total_err}E, {v1_total_warn}W)")
    print(f"Blind Judge Mean: v0={v0_mean_score}/5.00 vs v1={v1_mean_score}/5.00")
    print(f"Pairwise Record : v1 wins={v1_wins}, v0 wins={v0_wins}, ties={ties}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
