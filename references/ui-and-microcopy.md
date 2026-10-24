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
Good Persian error messages state **(1) what happened** and **(2) how to fix it**, in active, non-blaming language, under 15 words:

<!-- fa-check-ignore-start -->

| Scenario | ❌ Robotic / Calqued Error | ✅ Natural Product Persian |
|---|---|---|
| Invalid phone prefix | `شماره تلفن وارد شده توسط شما معتبر نمی‌باشد.` | `شماره باید با ۰۹ شروع شود.` |
| Phone too short | `تعداد ارقام وارد شده جهت شماره موبایل کافی نیست.` | `شمارهٔ موبایل باید ۱۱ رقم باشد.` |
| Network / server down | `خطایی در برقراری ارتباط با سرور به وقوع پیوست.` | `ارتباط با سرور برقرار نشد. اینترنت خود را بررسی کنید و دوباره بزنید.` |
| Temporarily closed | `ثبت سفارش در حال حاضر امکان‌پذیر نمی‌باشد.` | `فروش آنلاین فعلاً بسته است. برای سفارش با ما تماس بگیرید.` |
| Empty state (list) | `هیچ آیتمی در این لیست وجود ندارد.` | `هنوز دستگاهی اضافه نکرده‌اید.` |

<!-- fa-check-ignore-end -->

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
