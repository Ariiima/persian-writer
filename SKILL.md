---
name: persian-writer
description: >-
  Write, edit, translate, and humanize natural, native-sounding Persian (Farsi)
  text across all registers: formal-human (رسمی روان), administrative letters
  (نامه اداری), semi-formal articles, product/UI microcopy (محاورهٔ نرم), and
  colloquial social/voiceover scripts (محاورهٔ کامل و نریشن). Eliminates English
  syntactic calques (ترجمه‌زدگی), bureaucratic fossils (می‌باشد، گردید، در راستای),
  register mixing, ZWNJ (نیم‌فاصله) errors, and هکسره mistakes. Use whenever any
  deliverable or text string is in Persian/Farsi.
when_to_use: >-
  Trigger whenever the user asks to write, rewrite, translate, proofread,
  humanize, or localize Persian/Farsi text—including emails, official letters,
  blog posts, landing pages, UI strings, error messages, SMS/notifications,
  social captions, or video/podcast voiceover scripts—even if the user prompts
  in English or Finglish.
metadata:
  version: "1.0.0"
  authorities: "دستور خطّ فارسی فرهنگستان (ویراست ۱۴۰۱)؛ Microsoft fa-IR Style Guide"
license: MIT
---

# Persian Writer (`persian-writer`)

When writing Persian, **think in Persian verbs—never draft in English syntax and translate word-by-word.**

Models fail at Persian in four predictable ways:
1. **Syntactic calques (`ترجمه‌زدگی`):** English noun-heavy, passive (`توسط`), SVO-ordered sentences dressed in Persian words.
2. **Bureaucratic fossils (`اداری‌زدگی`):** Defaulting to government-office clichés (`می‌باشد`, `گردید`, `نمود`, `در راستای`, `لازم به ذکر است`).
3. **Register bleeding (`قاطی‌کردن لحن`):** Mirroring the user's casual prompt tone in a formal deliverable, or mixing written (`کتابی`) and spoken (`شکسته`) forms in one text.
4. **Orthographic & script errors:** Missing ZWNJ (`نیم‌فاصله`), `هکسره` (`کتابه من`), fake tanvin (`گاهاً`, `دوماً`), Arabic `ي/ك`, and em-dashes (`—`).

Rules use three severity levels:
- 🔴 **Hard Ban (`مطلق`):** Wrong in every register. Never emit.
- 🟡 **Register-Dependent (`رجیستری`):** Valid in one register, an error in another.
- 🔵 **Diagnostic (`تشخیصی`):** Acceptable once, machine-tell when repeated or clustered.

---

## Step 1: Route & Lock the Register (Before Writing)

Determine the register from the **deliverable's destination and audience**, **NEVER** from the tone of the user's prompt. A casual request (*«دمت گرم یه نامه واسه اداره مالیات بنویس»*) still requires a 100% `formal-admin` deliverable.

| Register | Destination / Surface | Verbs | Object & Pronouns | Reference |
|---|---|---|---|---|
| **`formal-human`** (`رسمی روان` — *Default*) | B2B emails, proposals, reports, docs, standard product UI, company sites, press | `است`, `شد`, `می‌شود`, `می‌توانید` | `را`, `این / آن`, `آن‌ها`, `شما` | `references/registers.md` |
| **`formal-admin`** (`رسمی اداری`) | Official letters (`نامه اداری`) to ministries, tax office, banks, universities | `است`, `می‌شود` + `دستور فرمایید` | `را`, `این / آن`, `جناب‌عالی` | `references/registers.md` §4B |
| **`semi-formal`** (`نیمه‌رسمی / آموزشی`) | Blog posts, newsletters, tutorials, technical guides, LinkedIn | `است`, `می‌شود`, `می‌کنیم` | `را`, `این / آن`, direct `شما` | `references/registers.md` |
| **`light-colloquial`** (`محاورهٔ نرم`) | Friendly consumer app UI, onboarding, casual landing pages, support chat | `می‌شه`, `می‌تونید`, `داره`, `ـه` | Keeps **`را`** and **`این / آن`** | `references/ui-and-microcopy.md` |
| **`full-colloquial`** (`محاورهٔ کامل / نریشن`) | Instagram/Telegram, friendly DMs, podcast & video voiceover (`نریشن`) | `می‌شه`, `می‌خوام`, `می‌رم`, `می‌گه`, `بذار`, `ـه` | **`رو`**, **`اون / اونا / اینا`**, `واسه`, `دیگه` | `references/registers.md` §4C |

### 🔴 The Register Lock Rule
Once you select a register, **never cross between `کتابی` and `شکسته`** outside direct quotes (`«...»`):
- **Written (`کتابی`):** `است / نیست`, `می‌شود`, `می‌کند`, `می‌گوید`, `بدهید`, `بگذارید`, `آن / آن‌ها`, `را`, `دیگر / اگر / مگر`, `برای`.
- **Spoken (`شکسته`):** `ـه / ـست` (`خوبه`), `می‌شه`, `می‌کنه`, `می‌گه`, `بدید`, `بذارید`, `اون / اونا` *(Full only)*, `رو` *(Full only)*, `دیگه / اگه / مگه`, `واسه / توش` *(Full only)*.

---

## Step 2: Think in Persian Verbs, Not English Nouns (ضد گرته‌برداری)

Read `references/anti-calque-and-style.md` for the full catalogue. Apply these core syntactic transforms on every sentence:

1. **🔴 Unpack Nominalization Wrappers (`مورد ... قرار گرفتن`):**
   - ❌ `مورد بررسی قرار گرفت` / `مورد استفاده قرار می‌گیرد` / `اقدام به ثبت‌نام نمود`
   - ✅ `بررسی شد` / `استفاده می‌شود` (یا `به‌کار می‌رود`) / `ثبت‌نام کرد`
2. **🔴 Eliminate `توسط` Passives:**
   Persian does not name the agent with `توسط` in a passive sentence. Make the actor the subject:
   - ❌ `این تصمیم توسط تیم فنی گرفته شد.` → ✅ `تیم فنی این تصمیم را گرفت.`
3. **🟡 Place `را` Before Relative `که` (in Formal/Semi-Formal):**
   - ❌ `گزارشی که دیروز فرستاده بودید را خواندم.` → ✅ `گزارشی را که دیروز فرستاده بودید، خواندم.`
4. **🔵 Cap Ezafe Chains at ≤ 3 Nouns (`تتابع اضافات`):**
   Break 4+ chained nouns with a preposition (`در`, `برای`, `از`):
   - ❌ `بررسی گزارش خطای سرور نسخه جدید برنامه` → ✅ `بررسی گزارش خطای سرور در نسخهٔ جدید برنامه`
5. **🔵 Use Present Tense Instead of Calqued Future (`خواهد`):**
   - ❌ `با زدن این دکمه، در باز خواهد شد.` → ✅ `با زدن این دکمه، در باز می‌شود.`
6. **🔵 Drop Redundant Indefinite `یک` (`a / an`):**
   - ❌ `او یک مهندس باتجربه است.` → ✅ `او مهندسی باتجربه است.` (or `او مهندس باتجربه‌ای است.`)
7. **🔴 Ban Literal English Idiom Calques:**
   - `در پایان روز` (*at the end of the day*) → `در نهایت` / `آخرش`
   - `شما را قادر می‌سازد تا` (*enables you to*) → `به شما امکان می‌دهد` / `کمکتان می‌کند`
   - `نه تنها ... بلکه همچنین` (*not only... but also*) → `هم ... و هم ...` / `علاوه بر`
   - `X را تجربه کنید` (*experience X*) → state what actually happens (`سایت در ۲ ثانیه باز می‌شود`)
   - `شیرجه بزنیم به` / `نگاهی بیندازیم به` → `بررسی کنیم` / `بریم سراغِ`
   - `پتانسیل X را آزاد کنید` (*unlock X's potential*) → `از تمام توان/امکانات X استفاده کنید` or `X را متحول/به‌روز کنید` (never delete the sentence in translation!)
   - `بهترین نسخهٔ خودتان` → `بهترین عملکرد خودتان` · `سفر کاربری` → `مسیر استفاده`

---

## Step 3: Strip Bureaucratic Fossils & AI Furniture

<!-- fa-check-ignore-start -->

| 🔴 Banned AI / Bureaucratic Tell | ✅ Replace With |
|---|---|
| `می‌باشد` / `می‌باشند` / `نمی‌باشد` | `است` / `هستند` / `نیست` (even in `نامه اداری`!) |
| `گردید` / `گردیده است` / `نمود` | `شد` / `شده است` / `کرد` |
| `لازم به ذکر است که` / `شایان ذکر است` / `قابل توجه است` | *(Delete completely; state the point)* |
| `در راستای` / `در همین راستا` / `جهتِ` | `برای` |
| `در خصوصِ` / `پیرامونِ` | `دربارهٔ` / `در موردِ` |
| `از اهمیت ویژه‌ای برخوردار است` / `نقش بسزایی ایفا می‌کند` | `بسیار مهم است` (or state the concrete effect) |
| `به شمار می‌رود` / `محسوب می‌شود` / `به حساب می‌آید` | `است` |
| `در دنیای امروز، با پیشرفت تکنولوژی...` | *(Delete; start with the first real sentence)* |
| `در نهایت می‌توان گفت...` / `امیدوارم مفید بوده باشد` | *(Delete; end with a concrete fact or next step)* |
| `...که نشان‌دهندهٔ / بیانگرِ ... است` | *(Delete tacked-on participial tail)* |

<!-- fa-check-ignore-end -->

**Structural rules:**
- 🔴 **Zero em-dashes (`—`):** Never use `—` or `--` in Persian prose. Use `،`, `؛`, parentheses `(...)`, or a period.
- 🟡 **No ChatGPT bold-colon bullet lists (`- **عنوان:** توضیح`) in prose:** Write coherent paragraphs. Use bullets only for genuine lists.
- 🔵 **No decorative synonym triads:** Cut empty triads (`سریع، امن و مطمئن`); state specific facts (`نصب در ۳۰ دقیقه با ۱۸ ماه گارانتی`).
- 🔵 **Vary sentence rhythm:** Do not write choppy verbless fragments (`هر روز. سال‌هاست.`) or monotonous 20-word sentences. Connect clauses naturally (`و`, `اما`, `چون`, `تا`) and keep sentence-length variation healthy ($CV \ge 0.35$).

---

## Step 4: Script & Orthography Mechanics (دستور خطّ ۱۴۰۱)

See `references/orthography-1401.md` for full edge cases.

1. **🔴 Persian Codepoints Only:** Always use `ی` (`U+06CC`) and `ک` (`U+06A9`), never Arabic `ي`, `ى`, `ك`, `ة`, or `٠-٩`.
2. **🔴 ZWNJ (`نیم‌فاصله` `U+200C`) — In Both Formal AND Colloquial:**
   - **Always** keep ZWNJ after `می / نمی` in every register, including colloquial: write `می‌شود`, `نمی‌دانم`, `می‌شه`, `نمی‌شه`, `می‌رم`, `می‌گه`, `می‌گیم`, `می‌خوام`, `می‌خوایم`, `می‌ذاریم`, `می‌گذره` (never `میشه`, `میگم`, `میخوام`, `میذاریم`).
   - Mandatory in plural `ها` (`کتاب‌ها`, `پروژه‌های`), comparatives (`بزرگ‌تر`, `مهم‌ترین`), clitics after silent `ه` (`خانه‌ام`, `پروژه‌اش`, `حرفه‌ای`), and non-joined compounds (`نرم‌افزار`, `وب‌سایت`, `ثبت‌نام`, `صفحه‌کلید`, `هم‌زمان`, `بی‌دقت`).
   - **Never drop silent `ه` (`های غیرملفوظ`) in colloquial clitics:** write `نتیجه‌ش`, `مزه‌ش`, `خونه‌تون`, `بقیه‌ش`, `آماده‌ست`, `ساده‌ست` (never `نتیجش`, `مزش`, `خونتون`, `آمادس`).
   - Do **not** split lexicalized solid words: `بهتر`, `بیشتر`, `کمتر`, `همکار`, `همراه`, `امروزه`, `کتابخانه`, `بنابراین`.
3. **🔴 The `هکسره` Trap (`ـه` vs. Ezafe):**
   - In colloquial Persian, `ـه` means `است` (`این کتابه` = `این کتاب است` ✅).
   - **Never** write the ezafe link (`ـِ`) as `ـه`: `کتابه من` ❌ → `کتابِ من` / `کتاب من` ✅; `واسه کاره جدیدم` ❌ → `واسه کار جدیدم` ✅.
   - **Differential test:** Swap `ـه` with `است`. If the sentence breaks, delete `ـه`.
   - After silent `ه` (`خانه`, `پروژه`, `صفحه`), write the ezafe as `خانه‌ی ما` (with ZWNJ) or `خانهٔ ما`—never with a space (`خانه ی ما` ❌).
4. **🔴 Fake Tanvin vs. Required Tanvin:**
   - **Ban fake tanvin:** `گاهاً` ← `گاهی` · `دوماً / سوماً` ← `دوم اینکه / سوم اینکه` · `ناچاراً` ← `به‌ناچار` · `تلفناً` ← `تلفنی` · `زباناً` ← `زبانی`.
   - **Keep required tanvin:** `لطفاً`, `حتماً`, `واقعاً`, `مثلاً`, `کاملاً`, `اصلاً`, `معمولاً`, `تقریباً`, `دقیقاً`, `فعلاً`, `قطعاً`.
5. **🔴 Digits, Currency & Singular Nouns:**
   - Use Persian digits (`۰۱۲۳۴۵۶۷۸۹`) in prose, `٬` for thousands (`۱۲٬۵۰۰٬۰۰۰ تومان`), and `٪` for percent (`۲۰٪`). Keep Latin digits only in code, URLs, and Latin technical IDs (`ESP32`, `v2.1`).
   - **Noun after a number is always singular:** `۵ ویژگی کلیدی` و `۳ روز کاری` (never `۵ ویژگی‌های کلیدی` ❌).
6. **🔴 Punctuation:** Use `،` `؛` `؟` and `«گیومه»`. Attach punctuation to the preceding word with no space before it (`سلام، خوبی؟`).

---

## Step 5: Mandatory Verification Workflow

1. **Select & lock register** (Step 1) and read the matching reference file if needed (`references/registers.md`, `references/anti-calque-and-style.md`, `references/orthography-1401.md`, `references/ui-and-microcopy.md`).
2. **Draft directly in Persian** using verb-centric clauses:
   - **Strict 1-to-1 Fidelity on Rewrites & Translations:** Preserve every claim, actor, and list structure from the source text. **Never** add unstated product details (e.g., do not add "via mobile app" or "automatic categorization" if the source text did not state it), and **never** drop a sentence.
   - **Formal vs. Colloquial Morphology:**
     - In `formal-human` and `formal-admin`, use animate plurals with `ـان` (`مهمانان`, `کاربران`, `ساکنان`, `مهندسان`) rather than `ـها` (`مهمان‌ها`).
     - In `light-colloquial`, only verbs soften (`می‌تونید`, `می‌شه`, `باشه`); keep standard `را`, `این / آن`, `به آن` (never `رو`, `اون`, `بهش / ازش / توش / واسه`), and write plural possessive with `ـهایتان` (`هزینه‌هایتان`, `هدف‌هایتان`—never `هزینه‌هاتان`).
   - **Lexical Precision & Cultural Anchors:** Never calque *"track money/expenses"* as `ردیابی پول/هزینه` (`ردیابی` is for parcels/missiles; use `مدیریت هزینه‌ها` or `حساب دخل‌وخرج`). "New Year" is `اول سال / نوروز` (never `اول بهمن` or `ژانویه`).
3. **Run verification silently before answering:**
   - **If shell / code execution is available:** run `python3 scripts/fa_check.py --check --register <register>` on the draft (or `python3 scripts/fa_check.py --fix` for safe orthographic repairs). Fix every reported `🔴` error and `🟡` warning before presenting the text.
   - **If in a chat-only environment:** mentally grep the draft for:
     1. Zero `می‌باشد / گردید / نمود / در راستای / لازم به ذکر است / توسط`.
     2. Zero register mix between `کتابی` (`است / می‌شود / را / آن‌ها`) and `شکسته` (`ـه / می‌شه / رو / اونا`).
     3. Every `ـه` passes the `است` substitution test (no `هکسره`).
     4. Every `می/نمی` (formal and colloquial `می‌شه/می‌خوام`), `ها`, `تر/ترین`, and silent-`ه` clitic (`آماده‌ست`, `نتیجه‌ش`) has its ZWNJ (`نیم‌فاصله`).
     5. Zero em-dashes (`—`), zero ASCII `? , ;` in Persian text, Persian digits `۰–۹`.
   - Output **only** the clean final text unless the user explicitly asked for an edit log or rule breakdown.
