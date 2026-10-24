# Persian Product UI, UX Microcopy & Landing Pages (رابط کاربری و میکروکاپی)

When writing Persian for apps, web interfaces, SMS/notifications, or product landing pages, follow these rules alongside the chosen register (`formal-human` or `light-colloquial`).

---

## 1. Zero Untranslated English UI Chrome
Never leave English boilerplate inside a Persian UI (`Submit`, `Cancel`, `Loading...`, `Oops!`, `Something went wrong`, `N/A`).
- `Loading...` → `در حال بارگذاری...` / `کمی صبر کنید...`
- `Cancel` → `انصراف`
- `Confirm` → `تأیید`
- `Save changes` → `ذخیرهٔ تغییرات`
- `Retry` → `تلاش دوباره`

---

## 2. Button & CTA Consistency (یکدستی دکمه‌ها)
Persian buttons use one of two grammatical shapes:
1. **Verbal Noun (`اسم مصدر`):** `ثبت‌نام`, `ورود`, `ذخیره`, `افزودن دستگاه`, `دانلود گزارش`
2. **Polite Plural Imperative (`فعل امری`):** `ثبت‌نام کنید`, `وارد شوید`, `ذخیره کنید`, `دستگاه را اضافه کنید`

**Rule:** Do not mix both styles in the same navigation bar, modal, or form pair (e.g., `ذخیره کنید` beside `انصراف` is jarring; use `ذخیره` + `انصراف`). Primary landing-page hero CTAs work well with action-specific verbal nouns (`ساخت اولین فاکتور`, `دریافت مشاورهٔ رایگان`) or direct imperatives (`همین حالا شروع کنید`).

---

## 3. Error Messages & Validation Microcopy

Distinguish **Inline Field Validation** (under an input box) from **Action / Network Failures** (toast/alert when a request fails):

### A. Inline Field Validation (`خطای زیر فیلد ورودی`) — One Single Clause (5–8 words)
When the user types an invalid phone number, code, or email, the constraint itself **is** the instruction.
- **Rule:** Write **one single short sentence** stating the rule (`شماره موبایل باید با ۰۹ شروع شود.` · `شماره موبایل باید ۱۱ رقم باشد.`).
- **🔴 Never append a second scolding/padding sentence:** Never tack on `لطفاً شماره را دوباره بررسی کنید`, `لطفاً رقم‌های باقی‌مانده را وارد کنید`, or `رقم‌های واردشده را بررسی کنید`. It reads as stiff (`خشک و اداری`) and overflows single-line helper text under mobile inputs.
- **🔴 Never use `لطفاً` in inline validation or button labels.**
- **🔴 Orthographic uniformity across sibling strings:** Keep recurring noun phrases identical across all strings on the same screen (write `شماره موبایل` in both rules, or `شمارهٔ موبایل` in both—never mix them across sibling lines).

### B. Action / Network / System Failures (`خطای ارسال یا ارتباط`) — Failed Action + Recovery Step
When an action fails due to network or server state, lead with **what failed** (`کد ارسال نشد.`), then state **what to do** (`اینترنت خود را بررسی کنید و دوباره تلاش کنید.`). Do not repeat synonymous nouns (`ارتباط با اینترنت... اتصال خود را...`) in back-to-back clauses.

<!-- fa-check-ignore-start -->

| Scenario | ❌ Stiff / Padded / Calqued | ✅ Natural Product Persian |
|---|---|---|
| Invalid phone prefix (Inline) | `شماره موبایل باید با ۰۹ شروع شود. لطفاً دوباره بررسی کنید.` | `شماره موبایل باید با ۰۹ شروع شود.` |
| Phone too short (Inline) | `شماره موبایل ۱۱ رقم دارد. لطفاً رقم‌های باقی‌مانده را وارد کنید.` | `شماره موبایل باید ۱۱ رقم باشد.` |
| Network error on OTP send | `ارتباط با اینترنت برقرار نیست. اتصال خود را بررسی کنید.` | `کد ارسال نشد. اینترنت خود را بررسی کنید و دوباره تلاش کنید.` |
| Temporarily closed | `ثبت سفارش در حال حاضر امکان‌پذیر نمی‌باشد.` | `فروش آنلاین فعلاً بسته است. برای سفارش با ما تماس بگیرید.` |
| Empty state (list) | `هیچ آیتمی در این لیست وجود ندارد.` | `هنوز ترددی ثبت نشده است.` |

<!-- fa-check-ignore-end -->

### C. Deliver Only the Copy (No Unrequested Meta-Explanations)
When asked to write UI strings, buttons, or microcopy, output **only** the requested items. Do not append explanatory notes like `هر دو دکمه به‌صورت اسم مصدر نوشته شده‌اند...` unless the user explicitly asks for rationale.

---

## 4. SMS & Push Notifications
Iranian users are sensitive to spammy or cryptic SMS/push copy:
- Put the **brand name** and the **core event/code** in the first 40 characters.
- One action per message; never stack polite formulas (`مشترک گرامی، با سلام و احترام به استحضار می‌رساند...`).
- Example (Invite SMS): `حمیدرضا شما را به نوا دعوت کرد. برنامهٔ نوا را نصب کنید و با همین شماره وارد شوید.`
- Example (OTP): `کد ورود شما به نوا: ۴۸۲۹۱۰`

---

## 5. Product & Landing Page Copywriting
1. **Use the everyday word the customer actually says:**
   - `گوشی` (or `موبایل`), not `تلفن همراه هوشمند`
   - `فاکتور` and `رسید`, not `سند صورت‌حساب مالی`
   - `اینترنت`, not `شبکهٔ جهانی`
   - `اپلیکیشن` or `برنامه`, not `نرم‌افزار کاربردی تلفن همراه`
2. **Concrete mechanisms over adjectives:**
   - ❌ `سیستم پیشرفته و منحصربه‌فرد ما امنیت بی‌نظیری را برای ساختمان شما به ارمغان می‌آورد.`
   - ✅ `فاکتورهای ماهانه را در ۳۰ ثانیه صادر کنید و لینک پرداخت مستقیم بفرستید.`
3. **Reassurance beats artificial scarcity:**
   Iranian buyers distrust fake countdowns (`فقط تا پایان امشب!`). Build trust with concrete guarantees: `۱۸ ماه گارانتی تعویض`, `نصب در کمتر از ۳۰ دقیقه`, `بدون نیاز به کارت بانکی`.

---

## 6. Technical Documentation & Developer Guides (مستندات فنی بی‌ابهام)
1. **One Instruction Per Sentence:** Write procedures as numbered steps using polite plural imperatives (`فایل پیکربندی را باز کنید. مقدار کلید را تغییر دهید.`). Never chain 3 actions with `و` or participial `کرده و...`.
2. **Dual Terminology Strategy (استاندارد جامعهٔ فنی ایران):**
   - Keep universal developer tokens in Latin script inline: `API`, `Webhook`, `Token`, `Header`, `JSON`, `DNS`, `CDN`, `HTTP 429`, `SDK`.
   - For conceptual technical terms, use the natural Persian term and pair it with the English term in parentheses on **first mention only**: `حافظهٔ نهان (Cache)`, `تأخیر نمایی (Exponential Backoff)`.
   - **One Word, One Meaning:** Pick one term per concept and use it consistently throughout the doc (do not cycle between `توکن`, `کلید دسترسی`, and `رمزینه` for the same thing).
3. **Keep Compound Verbs Adjacent:** Do not wedge long prepositional phrases between the noun and light verb of a compound verb (`درخواست را پس از ۱۰ ثانیه دوباره بفرستید` ✅ vs `دوباره پس از ۱۰ ثانیه و بررسی هدرها ارسال نمایید` ❌).

---

## 7. Persian SEO Articles & B2B Proposals
### A. SEO Blog Posts (`سئو و محتوای وبلاگ`)
1. **Answer-First Opening (`اول جواب، بعد توضیح`):** The first 2–3 sentences must directly answer the user's search query (e.g., state the actual price range or core mechanism immediately). Never open with history or `در دنیای امروز`.
2. **Metadata Block:** When asked for SEO metadata, provide:
   - **عنوان سئو (Title Tag, ~50–60 chars):** Put the exact primary keyword at the **rightmost start** of the title (`قیمت طراحی سایت فروشگاهی در ۱۴۰۵ | راهنمای کامل`).
   - **توضیحات متا (Meta Description, ~130–155 chars):** Value proposition + concrete detail + soft CTA.
3. **Subheadings (`H2 / H3`) as Real Reader Questions:** Phrase H2s around the concrete questions searchers ask (`چه عواملی روی قیمت طراحی سایت اثر می‌گذارد؟`).
4. **Honest Range Pricing in `تومان`:** When exact tariffs aren't provided, give realistic, transparent tiers/ranges in `تومان` and explain what drives the difference.
5. **FAQ Section (`سؤالات متداول`):** Close with 3–5 concise, non-repetitive Q&As that directly answer long-tail queries.

### B. B2B Proposals (`پروپوزال و پیشنهاد قیمت`)
- Use **`formal-human` (`رسمی روان`)**: crisp headings, concrete scope/phases, exact timeline (`۴۵ روز کاری`) and price (`۸۵ میلیون تومان`), and a clear next-step CTA (`پیشنهاد می‌کنیم این هفته جلسه‌ای ۱۵ دقیقه‌ای برگزار کنیم`).
- **Never** use bureaucratic fossils (`می‌باشد`, `گردید`, `در راستای`), and **never** use street slang (`خیالتون راحت`, `کار رو جمع می‌کنیم`).
