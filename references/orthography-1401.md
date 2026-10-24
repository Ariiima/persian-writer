# Persian Orthography & Script Mechanics (دستور خطّ فرهنگستان ۱۴۰۱)

Script mechanics are **never optional**, regardless of register. Even a casual Instagram caption or chat message must use Persian codepoints, proper ZWNJ (`نیم‌فاصله`), and clean punctuation.

---

## 1. Character Codepoints (حروف فارسی، نه عربی)

Never emit Arabic presentation variants or Arabic-Indic digits in Persian text:

<!-- fa-check-ignore-start -->

| Correct Persian | Codepoint | ❌ Wrong (Arabic) | Codepoint |
|---|---|---|---|
| `ی` | `U+06CC` | `ي` / `ى` | `U+064A` / `U+0649` |
| `ک` | `U+06A9` | `ك` | `U+0643` |
| `هٔ` or `ه‌ی` | `U+0647 U+0654` | `ة` | `U+0629` |
| `۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹` | `U+06F0..U+06F9` | `٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩` | `U+0660..U+0669` |

<!-- fa-check-ignore-end -->

---

## 2. ZWNJ (`نیم‌فاصله` — `U+200C`)

The Zero-Width Non-Joiner separates morphemes inside a single phonological word while preventing cursive joining.

### 2.1 Mandatory ZWNJ Positions

<!-- fa-check-ignore-start -->

| Morpheme | ❌ Wrong (Spaced / Attached) | ✅ Right (with ZWNJ) |
|---|---|---|
| `می` / `نمی` + verb | `می شود`, `نمی دانم`, `میشود` (in formal) | `می‌شود`, `نمی‌دانم`, `می‌روم` |
| Plural `ها` | `کتاب ها`, `پروژه های`, `سفارشها` | `کتاب‌ها`, `پروژه‌های`, `سفارش‌ها` |
| Comparative `تر / ترین` | `بزرگ تر`, `مهم ترین` | `بزرگ‌تر`, `مهم‌ترین` |
| Verbal & pronominal clitics after silent `ه` | `خانه ام`, `پروژه اش`, `خسته ایم`, `گفته اند` | `خانه‌ام`, `پروژه‌اش`, `خسته‌ایم`, `گفته‌اند` |
| Indefinite / relative `ای` after silent `ه` | `حرفه ای`, `نقطه ای`, `هفته ای` | `حرفه‌ای`, `نقطه‌ای`, `هفته‌ای` |
| Compound prefixes (`بی‌`, `هم‌`, `بر`, `فرا`) | `بی دقت`, `هم زمان` (when prefix ends in joiner) | `بی‌دقت`, `هم‌زمان`, `هم‌راستا` |
| Non-joined compounds | `نرم افزار`, `وب سایت`, `صفحه کلید`, `ثبت نام` | `نرم‌افزار`, `وب‌سایت`, `صفحه‌کلید`, `ثبت‌نام` |

<!-- fa-check-ignore-end -->

### 2.2 Lexicalized Solid Words (پیوسته‌نویسی — Do NOT insert ZWNJ)
Per Farhangestan 1401, short lexicalized words whose components have fused or whose first element ends in a non-joining letter (`ا، د، ذ، ر، ز، ژ، و`) are often written solid:
- **Comparatives:** `بهتر`, `بیشتر`, `کمتر`, `بدتر`, `پیشتر` (never `به‌تر` or `بیش‌تر`).
- **Compounds & prefixes:** `همکار`, `همراه`, `همدل`, `امروزه`, `چنانچه`, `بنابراین`, `درحالی‌که`, `تاجایی‌که`, `کتابخانه`, `آشپزخانه`, `دلگیر`, `خودکار`, `پشتکار`.
- **Pronouns:** Either `آن‌ها / این‌ها` or `آنها / اینها` is accepted—keep one style across the document (`آن‌ها / این‌ها` preferred).

---

## 3. The `هکسره` Trap (`ـه` vs. Ezafe `ـِ`)

Confusing the spoken copula `ـه` (= `است`) with the ezafe link (`ـِ`) is the most stigmatized spelling error in modern Persian.

### 3.1 After Consonants (e.g., `کتاب`, `دست`, `کار`)
- **Spoken copula (`است`):** Written with `ـه` in colloquial Persian:
  - `این کتابه` = `این کتاب است` ✅
  - `کارش خوبه` = `کارش خوب است` ✅
- **Ezafe (`کسرهٔ اضافه`):** **Never** written as `ـه`. Leave it unwritten (or use `ـِ` only when disambiguating):
  - ❌ `کتابه من رو بده` / `واسه کاره جدیدم`
  - ✅ `کتابِ من رو بده` / `کتاب من رو بده` / `واسه کار جدیدم`

**The Differential Test:** Replace `ـه` with `است`. If the clause still makes grammatical sense (`این کتاب است`), `ـه` is right. If it becomes nonsense (`کتاب است من را بده`), delete `ـه` immediately.

### 3.2 After Words Ending in Silent `ه` (`های غیرملفوظ`: `خانه`, `پروژه`, `برنامه`, `ساده`)
- **Ezafe:** Write either `خانه‌ی ما` (`ه` + ZWNJ + `ی`) or `خانهٔ ما` (`ه` + hamza above `U+0654`). Pick one convention per document and hold it. **Never** write `خانه ی ما` (with a full space) and **never** drop the `ی/ء` in formal text (`خانه ما` is only acceptable in casual chat).
- **Spoken copula (`است`):** Write `ـست` after silent `ه`: `پروژه آماده‌ست` (`آماده است`), `خونه‌ست` (`خانه است`).

---

## 4. Fake Tanvin vs. Required Tanvin (تنوین)

Tanvin (`اً`) is an Arabic morphological suffix.
- **🔴 Never put tanvin on Persian or European words (تنوین جعلی):**

<!-- fa-check-ignore-start -->

| ❌ Wrong (Fake Tanvin) | ✅ Correct Persian |
|---|---|
| `گاهاً` | `گاهی` |
| `دوماً` / `سوماً` / `چهارماً` | `دوم اینکه` / `سوم اینکه` / `دوم،` |
| `ناچاراً` | `به‌ناچار` |
| `تلفناً` | `تلفنی` |
| `زباناً` | `زبانی` / `شفاهی` |
| `جانانهً` | `جانانه` |

<!-- fa-check-ignore-end -->

- **🟢 Keep tanvin on established Arabic adverbs (do not drop the `اً`):**
  `لطفاً`, `حتماً`, `واقعاً`, `مثلاً`, `کاملاً`, `اصلاً`, `معمولاً`, `تقریباً`, `دقیقاً`, `فعلاً`, `قطعاً`, `اتفاقاً`, `احتمالاً`, `مخصوصاً`, `اساساً`, `عملاً`, `نسبتاً`, `صرفاً`, `عمدتاً`.

---

## 5. Numbers, Currency, Dates, and Singular Nouns

1. **Digits:** Use Persian digits (`۰۱۲۳۴۵۶۷۸۹`) in all Persian prose. Keep Latin digits (`0-9`) only inside URLs, code, version tags (`v2.4`), international phone numbers (`+98...`), and technical IDs (`ESP32`, `433 MHz` when written in Latin).
2. **Separators:**
   - Thousands separator: `٬` (`U+066C`, e.g., `۱۲٬۵۰۰٬۰۰۰ تومان`).
   - Decimal separator: `٫` (`U+066B`, e.g., `۰٫۷ درصد` or `۰٫۷٪`).
3. **Singular Noun After Numbers (معدود مفرد):**
   In Persian, a noun following a number is **always singular**:
   - ❌ `۵ ویژگی‌های کلیدی` / `۳ روزهای کاری`
   - ✅ `۵ ویژگی کلیدی` / `۳ روز کاری`
4. **Currency:** Always specify `تومان` or `ریال` after the number (`۸۵۰٬۰۰۰ تومان`). Never mix them in one context.

---

## 6. Punctuation & BiDi Rules

- Use Persian comma `،` (`U+060C`), semicolon `؛` (`U+061B`), question mark `؟` (`U+061F`), and guillemets `«...»`.
- **Spacing:** Attach punctuation directly to the preceding word, followed by one space: `سلام، خوبی؟` (never `سلام ، خوبی ؟`).
- **No Em-Dashes (`—`):** Never use `—` or `--` in Persian text.
- **BiDi safety:** In Markdown or plain text, avoid starting a Persian paragraph with a bare Latin word if the viewer lacks `dir="rtl"`—prefix with a Persian category noun (`ابزار GitHub`, `سرویس API`, `کتابخانهٔ React`) so the paragraph auto-detects as RTL.
