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

## Multi-Skill Benchmark (`scripts/run_benchmark.py`)

Evaluates **16 golden tasks across 4 benchmark suites** (`evals/evals.json`) on **`claude-sonnet-5-5`** and **`claude-opus-5-5`**, comparing `persian-writer` head-to-head against the leading open-source Persian skills (`ali2000hos/persian-writing`, `shervinshirkubi/native-farsi`, `onlymaj/simplified-technical-persian`, and raw Claude without a skill), graded by both **`fa_check.py`** and a randomized 5-way blind judge (`gemini-3.1-pro-preview`):

### Benchmark Suites (`evals/evals.json`)
1. **Product & UX Writing (`product_ux`):** Login validation errors, empty states, Bluetooth permission dialogs, destructive confirmation modals, 3-slide `light-colloquial` onboarding, and 120-char SMS/push notifications.
2. **Marketing & Copywriting (`marketing_copy`):** Landing page Hero + 3 feature cards, de-AI-ing marketing copy, colloquial Instagram cafe captions, and 90-word spoken video voiceover (`نریشن`).
3. **Translation, Tech Docs & B2B (`translation_anticalque`):** English-to-Persian SaaS release note translation, unambiguous `HTTP 429` API rate-limit documentation, 1-page B2B proposal, and Answer-First SEO pricing guide.
4. **Formal, Admin, Academic & Proofreading (`formal_orthography`):** Slang-prompted tax office `نامه اداری` tripwire, Farhangestan 1401 orthography & `هکسره` repair, Master's thesis `چکیده + مقدمه`, and colloquial-to-standard incident report conversion.

### Results on `claude-sonnet-5-5` (16 Golden Tasks)

| Skill / Configuration | Overall Blind Judge (1–5) | Product & UX | Marketing & Copy | Translation & Tech | Formal & Orthography | Linter Pass Rate (`fa_check.py`) | Head-to-Head (`persian-writer` W-L-T) |
|---|---|---|---|---|---|---|---|
| **`Ariiima/persian-writer`** | **`4.89 / 5.00`** | **`5.00`** | `4.69` | **`4.94`** | **`4.94`** | **`16 / 16` (100%, 0E)** | — |
| `ali2000hos/persian-writing` | `4.73 / 5.00` | `4.75` | `4.75` | `4.62` | `4.81` | `11 / 16` (68.8%, 6E) | **12W – 2L – 2T** |
| `onlymaj/simplified-technical-persian` | `4.64 / 5.00` | `4.88` | `4.44` | `4.62` | `4.62` | `15 / 16` (93.8%, 1E) | **11W – 4L – 1T** |
| `shervinshirkubi/native-farsi` | `4.64 / 5.00` | `4.88` | `4.75` | `4.56` | `4.38` | `13 / 16` (81.2%, 4E) | **12W – 4L – 0T** |
| Raw `claude-sonnet-5-5` *(no skill)* | `4.56 / 5.00` | `4.69` | **`4.94`** | `4.44` | `4.19` | `13 / 16` (81.2%, 3E) | **12W – 4L – 0T** |

### Results on `claude-opus-5-5` (16 Golden Tasks)

| Skill / Configuration | Overall Blind Judge (1–5) | Product & UX | Marketing & Copy | Translation & Tech | Formal & Orthography | Linter Pass Rate (`fa_check.py`) | Head-to-Head (`persian-writer` W-L-T) |
|---|---|---|---|---|---|---|---|
| **`Ariiima/persian-writer`** | **`4.86 / 5.00`** | `4.88` | **`5.00`** | `4.56` | **`5.00`** | **`16 / 16` (100%, 0E)** | — |
| `onlymaj/simplified-technical-persian` | `4.81 / 5.00` | **`4.94`** | `4.75` | **`4.75`** | `4.81` | `14 / 16` (87.5%, 3E) | **11W – 4L – 1T** |
| `shervinshirkubi/native-farsi` | `4.73 / 5.00` | `4.81` | `4.75` | `4.62` | `4.75` | `15 / 16` (93.8%, 1E) | **10W – 3L – 3T** |
| Raw `claude-opus-5-5` *(no skill)* | `4.61 / 5.00` | `4.62` | `4.75` | `4.56` | `4.50` | `14 / 16` (87.5%, 2E) | **14W – 2L – 0T** |
| `ali2000hos/persian-writing` | `4.61 / 5.00` | `4.69` | `4.50` | `4.69` | `4.56` | `13 / 16` (81.2%, 5E) | **14W – 2L – 0T** |

## License

MIT
