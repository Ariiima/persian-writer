# persian-writer

**نگارش فارسی طبیعی و استاندارد برای دستیارهای هوش مصنوعی — Natural, native-sounding Persian (Farsi) writing skill for Claude, Claude Code, Cursor & Codex**

Large language models know Persian grammar rules on paper, yet their Persian output routinely reads as machine-translated (**ترجمه‌زده**) or stiffly bureaucratic (**اداری‌زده**). This skill fixes the four root causes without bloating context with `.docx` / `.pptx` / LibreOffice layout instructions:

1. **Syntactic Anti-Calque (`ضد گرته‌برداری نحوی`):** Shifts English noun-heavy, passive (`توسط`), SVO-ordered sentences into verb-centric Persian.
2. **Bureaucratic & AI Fossil Removal (`حذف کلیشه‌های اداری و ماشینی`):** Strips `می‌باشد`, `گردید`, `نمود`, `در راستای`, `لازم به ذکر است`, `مورد ... قرار گرفتن`, `نه تنها... بلکه همچنین`, and em-dashes (`—`).
3. **5-Register Routing & Lock (`تشخیص و قفل رجیستر`):** Separates the user's *prompt tone* from the *deliverable register* and prevents mid-paragraph mixing between written (`کتابی`) and spoken (`شکسته`) forms.
4. **Farhangestan 1401 Orthography (`دستور خطّ فرهنگستان ۱۴۰۱`):** Enforces ZWNJ (`نیم‌فاصله`) in both formal and colloquial verbs (`می‌شود` / `می‌شه`), prevents `هکسره` errors (`کتابه من` ❌ → `کتابِ من` ✅), preserves silent `ه` in colloquial clitics (`آماده‌ست`, `نتیجه‌ش`), bans fake tanvin (`گاهاً` → `گاهی`, `دوماً` → `دوم اینکه`), and normalizes digits/punctuation.

---

## Supported Registers

| Register | Surface / Audience | Verbs | Object & Pronouns |
|---|---|---|---|
| **`formal-human`** (`رسمی روان` — *Default*) | B2B emails, proposals, reports, docs, standard UI, company websites | `است`, `شد`, `می‌شود`, `می‌توانید` | `را`, `این / آن`, `آن‌ها`, `شما` |
| **`formal-admin`** (`رسمی اداری`) | Official letters (`نامه اداری`) to ministries, tax office, banks, universities | `است`, `می‌شود` + `دستور فرمایید` | `را`, `این / آن`, `جناب‌عالی` |
| **`semi-formal`** (`نیمه‌رسمی / آموزشی`) | Blog posts, newsletters, tutorials, technical guides, LinkedIn | `است`, `می‌شود`, `می‌کنیم` | `را`, `این / آن`, direct `شما` |
| **`light-colloquial`** (`محاورهٔ نرم`) | Friendly consumer app UI, onboarding, casual landing pages, support chat | `می‌شه`, `می‌تونید`, `داره`, `ـه` | Keeps **`را`** and **`این / آن`** |
| **`full-colloquial`** (`محاورهٔ کامل / نریشن`) | Instagram/Telegram captions, friendly DMs, podcast & video voiceover (`نریشن`) | `می‌شه`, `می‌خوام`, `می‌رم`, `می‌گه`, `بذار` | **`رو`**, **`اون / اونا / اینا`**, `واسه`, `دیگه` |

---

## Repository Structure

```text
persian-writer/
├── SKILL.md                        # Core router, register lock table, anti-calque rules & verification workflow
├── references/
│   ├── registers.md                # 6-step register detection, lock table & rules per register
│   ├── anti-calque-and-style.md    # English→Persian syntactic transforms, calque lexicon & AI-tell fixes
│   ├── orthography-1401.md         # Farhangestan 1401 ZWNJ rules, هکسره differential test, tanvin, BiDi & numbers
│   └── ui-and-microcopy.md         # Product UX copy, buttons, error messages, SMS & landing pages
├── scripts/
│   ├── fa_check.py                 # Zero-dependency deterministic linter, register-mix detector & safe auto-fixer
│   └── run_benchmark.py            # Automated evaluation harness (fa_check + blind pairwise LLM judge)
├── evals/
│   ├── evals.json                  # 8 golden evaluation tasks across all 5 registers
│   ├── triggers.json               # 20 trigger / non-trigger test queries
│   └── files/                      # Sample AI-generated & orthographically broken test inputs
└── tests/
    └── test_fa_check.py            # Unit test suite for fa_check.py
```

---

## Install

### Claude Code
```bash
git clone https://github.com/Ariiima/persian-writer ~/.claude/skills/persian-writer
```

### Cursor / Windsurf / Codex (`AGENTS.md` or `CLAUDE.md`)
Clone into your project (e.g. `skills/persian-writer/`) and add to `CLAUDE.md` or `AGENTS.md`:
```markdown
For any Persian (Farsi) writing, editing, translation, or UI copy task, read `skills/persian-writer/SKILL.md` first and run `python3 skills/persian-writer/scripts/fa_check.py --check` before returning Persian text.
```

---

## Deterministic Linter & Auto-Fixer (`scripts/fa_check.py`)

Requires only Python 3.8+ standard library (zero third-party dependencies):

```bash
# Check a file or stdin (reports errors and warnings with line numbers)
python3 scripts/fa_check.py --check draft.md
cat draft.md | python3 scripts/fa_check.py --check --register formal-human -

# Apply safe orthographic fixes in place (ی/ک, ZWNJ, tanvin, هکسره, digits, punctuation)
python3 scripts/fa_check.py --fix draft.md

# Emit structured JSON report
python3 scripts/fa_check.py --check --json draft.md

# Run unit tests
python3 -m unittest discover -s tests -v
```

---

## Benchmark (`scripts/run_benchmark.py`)

Evaluates `evals/evals.json` on `claude-sonnet-4-5` using both deterministic linting (`fa_check.py`) and a randomized blind pairwise A/B judge (`gemini-3.1-pro-preview`):

| Configuration | Deterministic Linter Pass Rate | Total Hard Errors / Warnings | Blind Judge Mean (1–5) |
|---|---|---|---|
| **Raw Claude Sonnet 4.5** *(no skill)* | `5 / 8` (62.5%) | `7 errors, 3 warnings` | `4.06 / 5.00` |
| **`persian-writer v0`** *(33-line checklist)* | `5 / 8` (62.5%) | `3 errors, 7 warnings` | `4.25 / 5.00` |
| **`persian-writer v1`** *(full skill + `fa_check.py`)* | **`8 / 8` (100%)** | **`0 errors, 0 warnings`** | **`4.78 / 5.00`** |

## License

MIT
