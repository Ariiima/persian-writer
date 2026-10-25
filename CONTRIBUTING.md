# Contributing to `persian-writer`

Thank you for helping make AI-generated Persian sound genuinely native! Because Persian writing quality has both a **deterministic floor** (orthography, ZWNJ, character hygiene, register purity, banned fossils) and a **stylistic ceiling** (natural verb-centric syntax, idiom accuracy, UX conciseness), every change to this skill is backed by automated tests, golden evaluation tasks, and human sentence ratings.

---

## 1. How the Skill & Verification Pipeline Work

```text
persian-writer/
├── SKILL.md                        # Core router, 6-register lock table, anti-calque rules & verification workflow
├── references/
│   ├── registers.md                # Register detection & lock table (formal-human, formal-admin, semi-formal, light/full colloquial, academic)
│   ├── anti-calque-and-style.md    # English→Persian syntactic shifts, calque dictionary & AI-tell fixes
│   ├── orthography-1401.md         # Farhangestan 1401 ZWNJ rules, هکسره differential test, tanvin, digits & BiDi
│   └── ui-and-microcopy.md         # Product UX copy, inline validation vs network errors, buttons, SMS, SEO & B2B proposals
├── scripts/
│   ├── fa_check.py                 # Zero-dependency deterministic linter, register-mix grep & safe auto-fixer
│   └── run_benchmark.py            # Multi-skill benchmark runner (fa_check + blind LLM judge across 4 suites)
├── evals/
│   ├── README.md                   # Detailed guide to the 4 benchmark suites, schema & human rating workflow
│   ├── evals.json                  # 16 golden evaluation tasks across 4 suites
│   ├── triggers.json               # 20 should-trigger / should-not-trigger queries
│   ├── human_ratings.json          # Logged human sentence ratings & diagnostic notes used to tune the skill
│   └── files/                      # Input fixtures for rewrite & orthography repair tasks
└── tests/
    └── test_fa_check.py            # Unit test suite for fa_check.py
```

---

## 2. How to Tune the Skill From Real Bad Sentences (The 4-Step Loop)

Whenever you spot an unnatural, calqued, or stiff Persian sentence produced by Claude (or another LLM):

### Step 1: Classify the Failure Mode
Ask which layer failed:
1. **Syntactic / Lexical Calque (`calque` / `بوی ترجمه`):** Did the model translate an English verb/idiom literally?
   - *Example A (`human_ratings.json`, Task #1):* Writing `همین متن کار می‌کند` (*"this text works"*). In Persian, `کار کردن` is only for machines, devices, or people—never for a piece of text or an option (`همین متن مناسب / کافی است` or `جواب می‌دهد`).
   - *Example B (`human_ratings.json`, Task #5):* Writing `یک دستگاه هر دو در را مدیریت می‌کند` (*"manages both doors"*). Physical doors and keys are **opened** (`باز می‌کند`), not "managed" (`مدیریت می‌کند`).
   - *Example C (`human_ratings.json`, Task #2):* Writing `با اجازهٔ شما، گوشی به بلوتوث وصل می‌شود` (*"With your permission..."*) in an OS permission dialog, or `با اولین باز شدن در` (*"With the first opening of the door"*) instead of `به‌محض باز شدن اولین در`.
2. **Stiff / Padded UX or Bureaucratic Prose (`stiff` / `خشک و اداری`):** Did the model add patronizing filler or government-office fossils?
   - *Real example from human rating:* Appending a second scolding sentence to an inline form-field validation error (`شماره موبایل باید ۱۱ رقم باشد. لطفاً رقم‌های باقی‌مانده را وارد کنید.`). Inline field errors under an input must be **one single 5–8 word clause** (`شماره موبایل باید ۱۱ رقم باشد.`).
3. **Register Mixing (`register_mix` / `قاطی شدن لحن`):** Did the model mix written (`کتابی`) and spoken (`شکسته`) forms, or pair spoken verbs (`می‌ره`) with formal possessive clitics (`پول‌تان` instead of `پول‌تون`) in `light-colloquial`?
4. **Orthography / ZWNJ / `هکسره` (`orthography`):** Did the model drop ZWNJ on colloquial verbs (`میشه`, `میخوام` instead of `می‌شه`, `می‌خوام`), drop silent `ه` before clitics (`آمادس`, `نتیجش` instead of `آماده‌ست`, `نتیجه‌ش`), or coordinate a comparative with a superlative (`بزرگ‌تر و مهم‌ترین` instead of `بزرگ‌ترین و مهم‌ترین`)?

### Step 2: Add the Rule to `SKILL.md` and `references/`
- Keep `SKILL.md` concise and high-signal so it fits comfortably in agent context.
- Put deep tables and before/after examples in the matching file under `references/` (`registers.md`, `anti-calque-and-style.md`, `orthography-1401.md`, or `ui-and-microcopy.md`).
- Mark every rule with its severity tier:
  - 🔴 **Hard Ban (`مطلق`):** Wrong in every register.
  - 🟡 **Register-Dependent (`رجیستری`):** Valid in one register, wrong in another.
  - 🔵 **Diagnostic (`تشخیصی`):** Acceptable once, AI-tell when repeated.

### Step 3: If Deterministic, Add a Pattern + Unit Test to `scripts/fa_check.py`
If the mistake can be caught reliably via regex or token inspection without false positives:
1. Add the pattern to `BANNED_FOSSILS`, `CALQUE_PATTERNS`, or the orthographic checks in `scripts/fa_check.py`.
2. Add a unit test in `tests/test_fa_check.py`.
3. Run the unit test suite and lint all markdown files in the repo:
   ```bash
   python3 -m unittest discover -s tests -v
   python3 scripts/fa_check.py --check SKILL.md references/*.md
   ```
   *(Note: When documenting a deliberate bad example inside `SKILL.md` or `references/*.md`, wrap the table or line in `<!-- fa-check-ignore-start --> ... <!-- fa-check-ignore-end -->` so the linter knows the error is intentional.)*

### Step 4: Add or Update a Benchmark Case in `evals/evals.json`
Add a task or an expectation in `evals/evals.json` (and log your human rating in `evals/human_ratings.json`), then run `scripts/run_benchmark.py` to verify that the score improves without regressing other suites.

---

## 3. Submitting a Pull Request Checklist

Before opening a PR, make sure these commands pass with exit code `0`:

```bash
# 1. All linter unit tests pass
python3 -m unittest discover -s tests -v

# 2. SKILL.md and all reference guides pass fa_check.py with 0 errors
python3 scripts/fa_check.py --check SKILL.md references/registers.md references/anti-calque-and-style.md references/orthography-1401.md references/ui-and-microcopy.md
```
