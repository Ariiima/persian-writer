# Evaluation & Benchmark Guide (`evals/`)

This directory contains the benchmark suites, trigger tests, input fixtures, and human rating logs used to measure and improve `persian-writer`.

---

## 1. The 4 Benchmark Suites (`evals/evals.json`)

Each task in `evals/evals.json` belongs to one of four real-world Persian writing suites:

| Suite ID | Name | What It Tests | Tasks |
|---|---|---|---|
| `product_ux` | **Product & UX Writing** (`محصول و رابط کاربری`) | Single-clause inline validation errors, empty states, Bluetooth permission dialogs, destructive confirmation modals, `light-colloquial` onboarding, and <120-char SMS/push alerts | `#1` – `#4` |
| `marketing_copy` | **Marketing & Copywriting** (`مارکتینگ و تبلیغات`) | Landing page Hero + 3 feature cards (zero fluff adjectives), de-AI-ing marketing copy, colloquial Instagram captions, and spoken video voiceover (`نریشن`) | `#5` – `#8` |
| `translation_anticalque` | **Translation, Tech Docs & B2B** (`ترجمه، مستندات فنی و B2B`) | English-to-Persian SaaS release translation, unambiguous `HTTP 429` API documentation, 1-page B2B proposal, and Answer-First SEO pricing guide | `#9` – `#12` |
| `formal_orthography` | **Formal, Admin, Academic & Proofreading** (`رسمی، اداری، علمی و ویراستاری`) | Slang-prompted tax office `نامه اداری` tripwire, Farhangestan 1401 orthography & `هکسره` repair, Master's thesis `چکیده + مقدمه`, and colloquial-to-standard incident report conversion | `#13` – `#16` |

---

## 2. Schema for Adding a New Benchmark Task (`evals/evals.json`)

To add a new test case, append an object to the `"evals"` array in `evals/evals.json`:

```json
{
  "id": 17,
  "suite": "product_ux",
  "name": "ux-checkout-payment-failed",
  "expected_register": "formal-human",
  "prompt": "متن پیام خطای پرداخت ناموفق در صفحه تسویه‌حساب فروشگاه را بنویس (پاسخ بانک: عدم موجودی کافی؛ به همراه اینکه اگر مبلغی کسر شده تا ۷۲ ساعت برمی‌گردد).",
  "expected_output": "Clear, reassuring formal-human payment failure message stating the bank reason (موجودی ناکافی), the ۷۲-hour automatic refund guarantee in Persian digits, and a retry CTA—zero می‌باشد/گردید.",
  "files": [],
  "expectations": [
    "States clearly that account balance was insufficient (موجودی کافی نیست)",
    "Reassures the user that any deducted amount returns within ۷۲ ساعت (in Persian digits)",
    "Contains zero می‌باشد / گردید / توسط"
  ]
}
```

### Fields
- `id` *(int)*: Unique task ID.
- `suite` *(string)*: One of `product_ux`, `marketing_copy`, `translation_anticalque`, `formal_orthography`.
- `name` *(string)*: Short kebab-case slug.
- `expected_register` *(string)*: Passed to `fa_check.py --register` (`formal-human`, `formal-admin`, `semi-formal`, `light-colloquial`, `full-colloquial`, or `auto`).
- `prompt` *(string)*: The exact user prompt sent to the model.
- `expected_output` *(string)*: Summary of what a 5/5 output looks like.
- `files` *(list[string])*: Optional relative paths under `evals/files/`.
- `expectations` *(list[string])*: Verifiable assertions checked by human reviewers and the blind LLM judge.

---

## 3. How to Record Human Sentence Ratings (`evals/human_ratings.json`)

Automated judges catch many issues, but native Persian editors catch subtle calques (such as `"همین متن کار می‌کند"` or second-sentence validation bloat). When you rate outputs from different skills or models, append your rating to `evals/human_ratings.json`:

```json
{
  "model": "claude-opus-5-5",
  "case_id": 1,
  "skill": "ali2000hos",
  "score": 3,
  "tags": ["stiff", "calque"],
  "note": ""همین متن کار می‌کند" is wrong in Persian (calque of 'this text works'); also added redundant 2nd sentence on error #2.",
  "reviewer": "your-github-handle"
}
```

### Standard Diagnostic Tags
- `natural` (`طبیعی و عالی` — reads like a native Iranian writer)
- `calque` (`بوی ترجمه` — English syntax or literal idiom translation)
- `stiff` (`خشک / اداری` — bureaucratic fossils or patronizing padding)
- `register_mix` (`قاطی شدن لحن` — mixing `کتابی` and `شکسته` forms)
- `orthography` (`خطای نیم‌فاصله / املا` — missing ZWNJ, `هکسره`, fake tanvin, wrong digits)
- `verbose` (`حشو / تغییر معنی` — unrequested meta-commentary or invented facts)

---

## 4. Running the Benchmark (`scripts/run_benchmark.py`)

```bash
# Run all 16 tasks on Claude Sonnet 5.5 (or claude-opus-5-5)
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="AIza..."
python3 scripts/run_benchmark.py --model claude-sonnet-5-5 --out /tmp/bench_results.json
```

If you also clone competing skills into `/tmp/competitors/{ali2000hos,native_farsi,simplified_tech}`, `run_benchmark.py` automatically includes them in a 5-way blind randomized tournament and prints both the per-suite leaderboard and head-to-head win/loss/tie records.
