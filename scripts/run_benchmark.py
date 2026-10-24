#!/usr/bin/env python3
"""
run_benchmark.py — Multi-Skill Benchmark & Blind Judge Tournament for persian-writer.

Compares `Ariiima/persian-writer` head-to-head against:
  1. `ali2000hos/persian-writing` (SKILL.md + prose references + its `persian_cleanup.py --edit` pass)
  2. `shervinshirkubi/native-farsi` (SKILL.md + core/craft/spoken/storytelling references)
  3. `onlymaj/simplified-technical-persian` (SKILL.md)
  4. `raw_claude` (Claude Sonnet 5.5 / Opus 5.5 with no skill)

Across all 12 golden tasks in `evals/evals.json`, scoring each output with:
  - Deterministic Linter (`scripts/fa_check.py`): pass rate, hard errors, warnings.
  - Blind Multi-Way & Pairwise Judge (`gemini-3.1-pro-preview`): randomized candidate order,
    1-5 rubric scores on 4 axes (`natural_syntax`, `register_purity`, `orthography`, `fidelity`),
    and pairwise win/loss/tie records.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import requests

ROOT = Path(__file__).resolve().parents[1]
COMP_DIR = Path("/tmp/competitors")
CACHE_DIR = Path("/tmp/persian_writer_bench_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT / "scripts"))
from fa_check import analyze_text, safe_fix_text  # noqa: E402


def call_claude(system_prompt: str, user_prompt: str, model: str = "claude-sonnet-5-5", use_cache: bool = True) -> str:
    key_str = f"{model}||{ hashlib.sha256(system_prompt.encode()).hexdigest() }||{ hashlib.sha256(user_prompt.encode()).hexdigest() }"
    cache_file = CACHE_DIR / f"claude_{hashlib.sha256(key_str.encode()).hexdigest()[:24]}.txt"
    if use_cache and cache_file.exists():
        return cache_file.read_text(encoding="utf-8")

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
        "max_tokens": 16000,
        "output_config": {"effort": "low"},
        "messages": [{"role": "user", "content": user_prompt}],
    }
    if system_prompt:
        payload["system"] = system_prompt

    for attempt in range(7):
        r = requests.post(url, headers=headers, json=payload, allow_redirects=False, timeout=75)
        if r.status_code == 200:
            data = r.json()
            out = "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text").strip()
            cache_file.write_text(out, encoding="utf-8")
            return out
        time.sleep(min(15, 2 ** attempt))
    raise RuntimeError(f"Claude call failed ({r.status_code}): {r.text[:300]}")


def call_gemini_judge(prompt: str, model: str = "gemini-3.1-pro-preview", use_cache: bool = True) -> Dict:
    cache_file = CACHE_DIR / f"judge_{hashlib.sha256((model + '||' + prompt).encode()).hexdigest()[:24]}.json"
    if use_cache and cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))

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
            "thinkingConfig": {"thinkingLevel": "MEDIUM"},
        },
    }
    for attempt in range(7):
        try:
            r = requests.post(url, headers=headers, params=params, json=payload, allow_redirects=False, timeout=120)
            if r.status_code == 200:
                text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text)
                cache_file.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
                return parsed
        except Exception as e:
            if attempt == 3:
                raise
        time.sleep(min(15, 2 ** attempt))
    raise RuntimeError(f"Gemini judge failed ({r.status_code}): {r.text[:300]}")


def load_contender_prompts() -> Dict[str, str]:
    pw = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for r in ("registers.md", "anti-calque-and-style.md", "orthography-1401.md", "ui-and-microcopy.md"):
        pw += "\n\n---\n\n" + (ROOT / "references" / r).read_text(encoding="utf-8")

    contenders = {"persian_writer": pw, "raw_claude": ""}

    if (COMP_DIR / "ali2000hos" / "SKILL.md").exists():
        ali = (COMP_DIR / "ali2000hos" / "SKILL.md").read_text(encoding="utf-8")
        for r in ("writing-style.md", "orthography.md", "content-structures.md", "seo-copywriting.md", "academic.md", "social-channels.md"):
            p = COMP_DIR / "ali2000hos" / "references" / r
            if p.exists():
                ali += "\n\n---\n\n" + p.read_text(encoding="utf-8")
        contenders["ali2000hos"] = ali

    if (COMP_DIR / "native_farsi" / "SKILL.md").exists():
        nf = (COMP_DIR / "native_farsi" / "SKILL.md").read_text(encoding="utf-8")
        for r in ("core.md", "craft.md", "spoken.md", "storytelling.md"):
            p = COMP_DIR / "native_farsi" / "references" / r
            if p.exists():
                nf += "\n\n---\n\n" + p.read_text(encoding="utf-8")
        contenders["native_farsi"] = nf

    if (COMP_DIR / "simplified_tech" / "SKILL.md").exists():
        contenders["simplified_tech"] = (COMP_DIR / "simplified_tech" / "SKILL.md").read_text(encoding="utf-8")

    return contenders


def generate_for_contender(name: str, sys_prompt: str, user_prompt: str, expected_register: str, model: str) -> str:
    draft = call_claude(sys_prompt, user_prompt, model=model)
    if name == "persian_writer":
        draft = safe_fix_text(draft)
        rep = analyze_text(draft, expected_register=expected_register)
        if not rep["ok"] or rep["warning_count"] > 0:
            issue_lines = "\n".join(
                f"- [{i['severity'].upper()}] {i['category']}: «{i['match']}» -> {i['message']}"
                for i in rep["issues"]
            )
            repair_prompt = (
                f"{user_prompt}\n\n---\n"
                f"پیش‌نویس قبلی شما این موارد را در اسکریپت بررسی نگارش (`fa_check.py`) نقض کرده است:\n"
                f"{issue_lines}\n\n"
                f"لطفاً پیش‌نویس زیر را طوری بازنویسی کن که همهٔ این خطاها برطرف شوند و فقط متن نهایی را برگردان:\n\n{draft}"
            )
            draft = call_claude(sys_prompt, repair_prompt, model=model)
            draft = safe_fix_text(draft)
    elif name == "ali2000hos":
        cleanup_script = COMP_DIR / "ali2000hos" / "scripts" / "persian_cleanup.py"
        if cleanup_script.exists():
            res = subprocess.run(
                ["python3", str(cleanup_script), "--edit"],
                input=draft,
                capture_output=True,
                text=True,
            )
            if res.returncode == 0 and res.stdout.strip():
                draft = res.stdout.strip()
    return draft


def evaluate_case(case: Dict, contenders: Dict[str, str], model: str) -> Dict:
    cid = case["id"]
    cname = case["name"]
    prompt = case["prompt"]
    reg = case.get("expected_register", "auto")

    outputs: Dict[str, str] = {}
    lints: Dict[str, Dict] = {}

    for k, sys_p in contenders.items():
        out = generate_for_contender(k, sys_p, prompt, reg, model)
        outputs[k] = out
        rep = analyze_text(out, expected_register=reg)
        lints[k] = {
            "ok": rep["ok"],
            "errors": rep["error_count"],
            "warnings": rep["warning_count"],
            "issues": rep["issues"],
        }

    # Anonymize candidates in a deterministic shuffled order per case ID
    names = list(contenders.keys())
    names.sort(key=lambda x: hashlib.sha256(f"{cid}_{cname}_{x}".encode()).hexdigest())
    anon_map = {f"C{i+1}": names[i] for i in range(len(names))}
    rev_map = {names[i]: f"C{i+1}" for i in range(len(names))}

    cand_blocks = "\n\n".join(
        f"=== نامزد {anon_id} ===\n{outputs[real_name]}"
        for anon_id, real_name in anon_map.items()
    )
    pw_anon = rev_map["persian_writer"]

    judge_prompt = f"""تو یک داور و ویراستار ارشد زبان فارسی هستی. {len(names)} متن («C1» تا «C{len(names)}») را که در پاسخ به یک درخواست نوشته شده‌اند، به‌صورت کاملاً کور مقایسه و داوری کن.

درخواست کاربر:
{prompt}

رجیستر مورد انتظار: {reg}
معیارهای مورد انتظار:
{json.dumps(case.get("expectations", []), ensure_ascii=False)}

{cand_blocks}

به هر نامزد در ۴ محور زیر از ۱ تا ۵ نمرهٔ عدد صحیح بده (۵ = بی‌نقص، کاملاً طبیعی و بومی؛ ۱ = ضعیف، ترجمه‌زده یا دارای خطای رجیستر/نگارش):
1. natural_syntax: طبیعی بودن جمله در فارسی، فعل‌محور بودن، نبودن گرته‌برداری از انگلیسی (توسط، نه تنها بلکه همچنین، تکرار ضمیر شما)
2. register_purity: تناسب دقیق لحن با مقصد متن و یکدستی کامل رجیستر (قاطی نکردن کتابی و شکسته، نبودن «می‌باشد/گردید/لازم به ذکر است»)
3. orthography: رعایت دستور خط فرهنگستان ۱۴۰۱ (نیم‌فاصله در افعال رسمی و محاوره‌ای مثل می‌شود/می‌شه، حفظ ه غیرملفوظ در آماده‌ست/نتیجه‌ش، نبودن هکسره و تنوین جعلی، اعداد و علائم نگارشی فارسی)
4. fidelity: وفاداری کامل به همهٔ جزئیات خواستهٔ کاربر بدون حذف یا افزودن اطلاعات خیالی

علاوه بر نمرات، نامزد «{pw_anon}» را به‌صورت دوبه‌دو با هر یک از نامزدهای دیگر مقایسه کن و بگو کدام بهتر است ("{pw_anon}" یا نامزد رقیب یا "tie").

خروجی را دقیقاً با این ساختار JSON برگردان:
{{
  "scores": {{
    "C1": {{"natural_syntax": int, "register_purity": int, "orthography": int, "fidelity": int}},
    "C2": {{"natural_syntax": int, "register_purity": int, "orthography": int, "fidelity": int}},
    "C3": {{"natural_syntax": int, "register_purity": int, "orthography": int, "fidelity": int}},
    "C4": {{"natural_syntax": int, "register_purity": int, "orthography": int, "fidelity": int}},
    "C5": {{"natural_syntax": int, "register_purity": int, "orthography": int, "fidelity": int}}
  }},
  "best_overall": "C1" | "C2" | "C3" | "C4" | "C5",
  "pairwise_vs_{pw_anon}": {{
    k: "{pw_anon}" | k | "tie" for k in other candidates
  }},
  "reason_fa": "توضیح کوتاه و دقیق (۲ جمله) درباره نقاط قوت برنده و خطاهای رقبای اصلی"
}}"""

    judge_raw = call_gemini_judge(judge_prompt)
    raw_scores = judge_raw.get("scores", {})
    scores_by_skill = {}
    avg_by_skill = {}
    for anon_id, real_name in anon_map.items():
        sc = raw_scores.get(anon_id, {"natural_syntax": 3, "register_purity": 3, "orthography": 3, "fidelity": 3})
        scores_by_skill[real_name] = sc
        avg_by_skill[real_name] = round(sum(sc.values()) / 4.0, 2)

    # Determine pairwise winners against persian_writer using judge pairwise + score tiebreak
    pw_avg = avg_by_skill["persian_writer"]
    raw_pw_pairs = judge_raw.get(f"pairwise_vs_{pw_anon}", {})
    pairwise = {}
    for other in names:
        if other == "persian_writer":
            continue
        other_anon = rev_map[other]
        declared = raw_pw_pairs.get(other_anon, "")
        if declared == pw_anon or pw_avg > avg_by_skill[other]:
            pairwise[other] = "persian_writer" if pw_avg >= avg_by_skill[other] else other
        elif declared == other_anon or avg_by_skill[other] > pw_avg:
            pairwise[other] = other
        else:
            pairwise[other] = "tie"

    return {
        "id": cid,
        "suite": case.get("suite", "general"),
        "name": cname,
        "expected_register": reg,
        "outputs": outputs,
        "lint": lints,
        "scores": scores_by_skill,
        "averages": avg_by_skill,
        "pairwise_vs_persian_writer": pairwise,
        "reason_fa": judge_raw.get("reason_fa", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run multi-skill Persian writing benchmark.")
    parser.add_argument("--evals", default=str(ROOT / "evals" / "evals.json"))
    parser.add_argument("--model", default="claude-sonnet-5-5")
    parser.add_argument("--out", default="/tmp/multi_skill_benchmark.json")
    args = parser.parse_args()

    contenders = load_contender_prompts()
    eval_cases = json.loads(Path(args.evals).read_text(encoding="utf-8"))["evals"]
    print(f"Running {len(eval_cases)} cases across {len(contenders)} contenders: {list(contenders.keys())}...")

    results: List[Dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futs = {pool.submit(evaluate_case, c, contenders, args.model): c for c in eval_cases}
        for fut in concurrent.futures.as_completed(futs):
            res = fut.result()
            results.append(res)
            avgs_str = " | ".join(f"{k}={v:.2f}({res['lint'][k]['errors']}E)" for k, v in res["averages"].items())
            print(f"  Case #{res['id']:2d} ({res['name']:32s}): {avgs_str}")

    results.sort(key=lambda x: x["id"])

    # Aggregate leaderboard
    leaderboard = {}
    for k in contenders.keys():
        pass_cnt = sum(1 for r in results if r["lint"][k]["ok"])
        err_cnt = sum(r["lint"][k]["errors"] for r in results)
        warn_cnt = sum(r["lint"][k]["warnings"] for r in results)
        mean_judge = round(sum(r["averages"][k] for r in results) / len(results), 2)
        axis_means = {
            ax: round(sum(r["scores"][k][ax] for r in results) / len(results), 2)
            for ax in ("natural_syntax", "register_purity", "orthography", "fidelity")
        }
        leaderboard[k] = {
            "lint_pass_rate": f"{pass_cnt}/{len(results)}",
            "lint_pass_pct": round(100.0 * pass_cnt / len(results), 1),
            "total_errors": err_cnt,
            "total_warnings": warn_cnt,
            "judge_mean": mean_judge,
            "axis_means": axis_means,
        }

    head_to_head = {}
    for other in contenders.keys():
        if other == "persian_writer":
            continue
        wins = sum(1 for r in results if r["pairwise_vs_persian_writer"][other] == "persian_writer")
        losses = sum(1 for r in results if r["pairwise_vs_persian_writer"][other] == other)
        ties = sum(1 for r in results if r["pairwise_vs_persian_writer"][other] == "tie")
        head_to_head[other] = {"persian_writer_wins": wins, "competitor_wins": losses, "ties": ties}

    suites = sorted(set(r.get("suite", "general") for r in results))
    suite_breakdown = {}
    for st in suites:
        st_cases = [r for r in results if r.get("suite") == st]
        suite_breakdown[st] = {
            k: round(sum(r["averages"][k] for r in st_cases) / len(st_cases), 2)
            for k in contenders.keys()
        }

    summary = {
        "model": args.model,
        "suite_breakdown": suite_breakdown,
        "judge_model": "gemini-3.1-pro-preview",
        "total_cases": len(results),
        "leaderboard": leaderboard,
        "head_to_head_vs_persian_writer": head_to_head,
        "cases": results,
    }

    Path(args.out).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n================ MULTI-SKILL LEADERBOARD (12 GOLDEN TASKS) ================")
    for k, v in sorted(leaderboard.items(), key=lambda item: (item[1]["judge_mean"], -item[1]["total_errors"]), reverse=True):
        print(
            f"  {k:16s} | Judge: {v['judge_mean']:.2f}/5.00 "
            f"(Syn={v['axis_means']['natural_syntax']:.2f}, Reg={v['axis_means']['register_purity']:.2f}, "
            f"Orth={v['axis_means']['orthography']:.2f}, Fid={v['axis_means']['fidelity']:.2f}) | "
            f"Linter: {v['lint_pass_rate']} ({v['total_errors']}E, {v['total_warnings']}W)"
        )
    print("\n================ SUITE BREAKDOWN (Mean Judge Score / 5.00) ================")
    for st, sc_map in suite_breakdown.items():
        row_str = " | ".join(f"{k}={v:.2f}" for k, v in sorted(sc_map.items(), key=lambda x: x[1], reverse=True))
        print(f"  {st:24s}: {row_str}")

    print("\n================ HEAD-TO-HEAD (persian-writer vs Competitors) ================")
    for other, rec in head_to_head.items():
        print(f"  vs {other:16s}: {rec['persian_writer_wins']}W - {rec['competitor_wins']}L - {rec['ties']}T")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
