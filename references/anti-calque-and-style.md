# Anti-Calque, Syntactic Shifts & De-AI-ing (ضد گرته‌برداری و طبیعی‌سازی)

Large language models plan sentences in an English-heavy latent representation and map them onto Persian words. The result is grammatically legal but syntactically foreign (**ترجمه‌زدگی**). Apply the rules below by their severity tier:

- 🔴 **Hard Ban (`مطلق`):** Wrong in every register. Fix unconditionally.
- 🟡 **Register-Dependent (`رجیستری`):** Allowed in one register, wrong in another.
- 🔵 **Diagnostic Signal (`تشخیصی`):** Acceptable once, machine-tell when repeated or clustered.

---

## 1. Syntactic Shifts: English Structure → Native Persian Structure

### 1.1 🔴 Verb-Centric, Not Noun-Centric (فعل، قلب جملهٔ فارسی است)
English packs meaning into abstract nouns and light verbs (*"perform an analysis"*, *"make a decision"*). Persian puts the weight on the verb.
- ❌ `بررسی این موضوع توسط تیم ما انجام شد.`
- ✅ `تیم ما این موضوع را بررسی کرد.`
- ❌ `در صورت وجود نیاز به تغییر رمز عبور، اقدام به ویرایش آن نمایید.`
- ✅ `اگر می‌خواهید رمز عبورتان را عوض کنید، آن را ویرایش کنید.`

### 1.2 🔴 Cut Bureaucratic Nominalization Wrappers (`مورد ... قرار گرفتن`)
Never wrap a verbal noun inside `مورد ... قرار گرفتن / دادن`, `به ... پرداختن`, `اقدام به ... نمودن`, `به عمل آوردن`, or `صورت پذیرفتن`.

<!-- fa-check-ignore-start -->

| ❌ Bureaucratic Wrapper | ✅ Clean Persian Verb |
|---|---|
| `مورد بررسی قرار گرفت` | `بررسی شد` |
| `مورد استفاده قرار می‌گیرد` | `استفاده می‌شود` / `به‌کار می‌رود` |
| `مورد تأیید قرار داد` | `تأیید کرد` |
| `اقدام به ثبت‌نام نمود` | `ثبت‌نام کرد` |
| `به تحلیل این داده می‌پردازیم` | `این داده را تحلیل می‌کنیم` |
| `قابلیت ... را دارا می‌باشد` | `می‌تواند ...` / `... دارد` |
| `از اهمیت بالایی برخوردار است` | `بسیار مهم است` |

<!-- fa-check-ignore-end -->

### 1.3 🔴 Eliminate `توسط` Passives
In Persian, passive voice (`مجهول`) is only used when the actor is genuinely unknown or irrelevant—and Persian **never** names the actor with `توسط` / `به‌وسیلهٔ` inside a passive clause (that is a direct calque of English *"by"*).
- ❌ `این بسته توسط کارشناس پشتیبانی ارسال شد.`
- ✅ `کارشناس پشتیبانی این بسته را فرستاد.`
- *Note:* Do not blindly flag every `شدن` as passive; inchoative compounds like `روشن شد` ("turned on") or `تمام شد` ("finished") are active in meaning.

### 1.4 🟡 Position of `را` with Relative Clauses
In formal and semi-formal prose, `را` belongs immediately after the head noun phrase, **before** `که`—not stranded at the end of a long relative clause:
- ❌ `گزارشی که دیروز برای مدیرعامل فرستاده بودید را خواندم.` *(Acceptable in spoken/colloquial, wrong in formal prose)*
- ✅ `گزارشی را که دیروز برای مدیرعامل فرستاده بودید، خواندم.`

### 1.5 🔵 Break Ezafe Chains (`تتابع اضافات` ≤ 3 nouns)
Because the ezafe (`ـِ`) is unwritten, chaining 4+ nouns creates ambiguity and heavy administrative prose. Break chains at 3 links using a preposition (`در`, `برای`, `از`):
- ❌ `بررسی گزارش خطای سرور نسخه جدید برنامه` (6 chained nouns)
- ✅ `بررسی گزارش خطای سرور در نسخهٔ جدید برنامه`

### 1.6 🔵 Present Tense Over Calqued Future (`خواهد + فعل`)
English uses *"will"* for promises, UI outcomes, and article roadmaps (*"In this guide, we will explore..."*, *"Clicking this button will save your file"*). Natural Persian uses the **present indicative** (`می‌کند`) or **subjunctive**:
- ❌ `در این مقاله به بررسی روش‌های کشینگ خواهیم پرداخت.`
- ✅ `در این مقاله روش‌های کشینگ را بررسی می‌کنیم.`
- ❌ `با زدن این دکمه، در باز خواهد شد.`
- ✅ `با زدن این دکمه، در باز می‌شود.`

### 1.7 🔵 Drop Redundant Indefinite `یک` (`a / an` Calque)
English requires *a/an* before singular count nouns; Persian uses the enclitic `ـی` (`کتابی`) or bare noun, reserving `یک` for when the number *one* matters or in spoken `یه`:
- ❌ `او یک برنامه‌نویس باتجربه است و یک راه‌حل ساده پیشنهاد داد.`
- ✅ `او برنامه‌نویسی باتجربه است و راه‌حلی ساده پیشنهاد داد.`

---

## 2. Lexical Calques Table (جدول گرته‌برداری‌های واژگانی)

<!-- fa-check-ignore-start -->

| English Source | ❌ Literal Calque | ✅ Natural Persian (Formal / Spoken) |
|---|---|---|
| *At the end of the day* | `در پایان روز` | `در نهایت` / `آخرش، ته‌ش` |
| *Enables / empowers you to* | `شما را قادر می‌سازد تا` | `به شما امکان می‌دهد` / `کمکتان می‌کند، باهاش می‌تونید` |
| *Be able to* | `قادر به انجام ... هستید` | `می‌توانید ... انجام دهید` / `می‌تونید` |
| *Not only ... but also* | `نه تنها ... بلکه همچنین` | `هم ... و هم ...` / `علاوه بر ...` |
| *Experience [noun]* | `سرعت بالا را تجربه کنید` | `سایت سریع‌تر باز می‌شود` / `ببینید چقدر سریع‌تره` |
| *Let's take a look at / dive into* | `بیایید نگاهی بیندازیم به / شیرجه بزنیم در` | `بررسی کنیم` / `بریم سراغِ` |
| *The best version of yourself* | `بهترین نسخهٔ خودتان` | (State the specific improvement) |
| *Journey* (for onboarding/process) | `سفر کاربری شما` | `مسیر استفاده` / `مراحل کار` |
| *Embrace [thing]* | `تغییر را در آغوش بگیرید` | `با تغییر همراه شوید` / `تغییر رو بپذیرید` |
| *Unlock potential* | `پتانسیل خود را آزاد کنید` | `از تمام امکانات ... استفاده کنید` / `امکانات ... را ارتقا دهید` |
| *What matters is that* | `چیزی که مهم است این است که` | `مهم این است که` / `اصل ماجرا اینه که` |
| *There is / are* (overused) | `سه روش وجود دارد که...` | `سه راه داریم:` / `سه روش هست:` |
| *In order to / Toward* | `در راستای / در جهتِ` | `برای` |
| *Regarding* | `در خصوصِ / پیرامونِ` | `دربارهٔ / در موردِ` |

<!-- fa-check-ignore-end -->

---

## 3. Persian AI Structural Tells (نشانه‌های ساختاری متن هوش مصنوعی)

1. **🔴 Copula Inflation (`بیماری می‌باشد`):**
   Never use `می‌باشد`, `می‌باشند`, `گردید`, `گردیده است`, `به شمار می‌رود`, `محسوب می‌شود`, or `به حساب می‌آید` as fancy substitutes for `است / شد`.
2. **🔴 Ceremonial Throat-Clearing:**
   Delete `لازم به ذکر است که`, `شایان ذکر است`, `قابل توجه است که`, `همان‌طور که مستحضرید`, `باید خاطرنشان کرد`. Start directly with the claim.
3. **🔴 Empty Scene-Setting Openers & Mirror Closers:**
   - Never open with `در دنیای امروز`, `در عصر دیجیتال`, `امروزه با پیشرفت روزافزون تکنولوژی`.
   - Never close with `در نهایت می‌توان گفت`, `به طور کلی، همان‌طور که دیدیم`, `انتخابی هوشمندانه برای آینده‌ای روشن`, or `امیدواریم این مطلب برای شما مفید بوده باشد`.
4. **🔴 Em-Dashes (`—`) in Persian Prose:**
   Persian typography does not use `—` for parenthetical pauses. Replace with `،`, `؛`, parentheses `(...)`, or a period.
5. **🟡 Bold-Header Bullet Furniture (`**عنوان:** توضیح`):**
   ChatGPT/Claude default to turning every paragraph into 4 bullets formatted as `**سرعت بالا:** توضیح...`. In articles, emails, and stories, write real paragraphs. Use bullets only for true enumerations.
6. **🔵 Decorative Rule-of-Three Triads:**
   Avoid reflexively pairing three near-synonyms (`سریع، امن و مطمئن`, `جامع، کاربردی و هدفمند`). Use one concrete fact (`نصب در ۱۰ دقیقه با ۱۸ ماه گارانتی`) or a genuine enumeration where each item carries distinct meaning.
7. **🔵 Tacked-on Participial Tails:**
   Cut trailing clauses like `...که نشان‌دهندهٔ تعهد ما به کیفیت است` or `...که بیانگر اهمیت این موضوع می‌باشد`.
8. **🔵 Synonym Cycling (تنوع واژگانی کاذب):**
   In technical or product text, do not cycle between `اپلیکیشن`, `برنامه`, `نرم‌افزار`, and `پلتفرم` for the same object across four sentences. Pick one term and keep it stable.
9. **🔵 Choppy Fragment Chains vs. Connected Flow:**
   "Short sentences" does not mean verbless staccato fragments (`هر روز. سال‌هاست. بدون خستگی.`). Write complete, verb-ending clauses connected by natural Persian conjunctions (`و`, `اما`, `چون`, `تا`) and vary sentence lengths so the rhythm breathes ($CV \ge 0.35$).
