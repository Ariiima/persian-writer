# Persian Registers & Tone Routing (تشخیص و قفل رجیستر)

Written Persian has a sharp divide between **written standard (`کتابی / معیار`)** and **spoken/colloquial (`محاوره / شکسته`)**, with distinct gradations inside each. Mixing them in one piece—or choosing the wrong one for the audience—is the fastest way to make Persian text sound machine-generated.

## 1. The 6-Step Routing Procedure

Apply this procedure **before** generating a single word:

1. **Explicit instruction wins:** If the user says «رسمی بنویس», «خودمونی باشه», «لحن اداری», or «برای نریشن ویدیو», obey that instruction regardless of topic.
2. **Classify the DELIVERABLE, never the prompt tone:** Users routinely type prompts in casual Persian («دمت گرم یه نامه واسه اداره مالیات بنویس»). The prompt is casual; the deliverable is `formal-admin`. Never mirror the user's chat slang in a formal artifact.
3. **Destination & audience:**
   - Going to a government body, ministry, bank, court, or university administration → **`formal-admin` (`رسمی اداری`)**
   - Going to a B2B client, investor, enterprise page, legal/terms page, or official report → **`formal-human` (`رسمی روان`)**
   - Going to a blog reader, newsletter, documentation user, or LinkedIn audience → **`semi-formal` (`نیمه‌رسمی`)**
   - Living inside a consumer app UI, onboarding flow, toast, or modern startup landing page where colloquial is requested → **`light-colloquial` (`محاورهٔ نرم`)**
   - Going to Instagram/Telegram captions, stories, friendly DMs, or spoken audio/video voiceover → **`full-colloquial` (`محاورهٔ کامل و گفتاری`)**
4. **One register per artifact:** If the user asks for an official email plus 3 Instagram captions in the same turn, treat them as separate artifacts with separate register locks.
5. **High stakes + genuine ambiguity → ask ONE short question:** («متن رسمی باشد یا محاوره‌ای؟»).
6. **Default when unspecified:** **`formal-human` (`رسمی روان`)** for prose/docs/UI, because accidental slang in a serious context is much costlier than clean standard Persian.

---

## 2. The 5 Registers at a Glance

| Register | Typical Surfaces | Verb Forms | Object Marker & Pronouns | Tone & Boundaries |
|---|---|---|---|---|
| **1. `formal-human`** (`رسمی روان`) | Proposals, reports, B2B websites, product UI (standard), press releases, emails | Full written: `است`, `شد`, `می‌شود`, `می‌توانید` | `را`, `این / آن`, `آن‌ها`, `شما` | Direct, concrete, warm, active. **Zero** `می‌باشد / گردید / نمود`. |
| **2. `formal-admin`** (`رسمی اداری`) | Official letters (`نامه اداری`) to tax office, ministries, banks, universities | Full written: `است`, `می‌شود`, `رسید` + polite formulas (`دستور فرمایید`) | `را`, `این / آن`, `ایشان / جناب‌عالی` | Uses fixed letter furniture (موضوع، گیرنده، با سلام و احترام). Still **no** `می‌باشد`. |
| **3. `semi-formal`** (`نیمه‌رسمی / آموزشی`) | Blog articles, newsletters, tutorials, technical guides, LinkedIn posts | Full written: `است`, `می‌شود`, `می‌کنیم` | `را`, `این / آن`, direct `شما` | Conversational rhythm and questions (`چرا؟`) with standard written morphology. |
| **4. `light-colloquial`** (`محاورهٔ نرم`) | Consumer product UI, friendly onboarding, casual landing pages, support chat | Spoken verbs: `می‌شه`, `می‌تونید`, `داره`, `ـه` (`خوبه`) | Keeps **`را`** and **`این / آن`** | Warm and approachable without street slang (`واسه / توش / اونا`). Polite plural (`شما بگید`). |
| **5. `full-colloquial`** (`محاورهٔ کامل / گفتاری`) | Instagram/Telegram, DMs, podcast scripts, video voiceover (`نریشن`) | Spoken + clipped: `می‌شه`, `می‌خوام`, `می‌رم`, `می‌گه`, `بذار`, `ـه / ـست` | **`رو`** (`کتاب رو`), **`اون / اونا / اینا`**, `واسه`, `دیگه`, `مگه` | Written as spoken. Breath-length clauses (<15 words for audio). |

---

## 3. The Register Lock Table (کتابی vs. شکسته)

Once you pick either the **Written (`کتابی`)** side (`formal-admin`, `formal-human`, `semi-formal`) or the **Spoken (`شکسته`)** side (`light-colloquial`, `full-colloquial`), **never cross the line** outside direct quotations:

<!-- fa-check-ignore-start -->

| Feature | Written (`کتابی`) — Never in `full-colloquial` | Spoken (`شکسته`) — Never in `formal-*` or `semi-formal` |
|---|---|---|
| Copula ("is") | `است`, `نیست`, `هستند`, `نیستند` | `ـه` (`خوبه`, `مهمه`), `ـست` (`اینجاست`), `هستن`, `نیستن` |
| Modal / Auxiliary | `می‌شود`, `نمی‌شود`, `می‌توانید`, `می‌خواهم` | `می‌شه / میشه`, `نمی‌شه`, `می‌تونید`, `می‌خوام` |
| Common Verbs | `می‌کند`, `می‌کنند`, `می‌گوید`, `می‌گویند`, `می‌دهد`, `بگذارید` | `می‌کنه`, `می‌کنن`, `می‌گه`, `می‌گن`, `می‌ده`, `بذارید` |
| Demonstratives | `آن`, `آن‌ها`, `این‌ها`, `همان` | `اون`, `اونا`, `اینا`, `همون` *(keep `این/آن` in `light-colloquial`)* |
| Object Marker | `را` (`فایل را فرستادم`) | `رو` / `ـو` (`فایل رو فرستادم` / `فایلو فرستادم`) *(keep `را` in `light-colloquial`)* |
| Conjunctions / Particles | `اگر`, `مگر`, `دیگر`, `برای`, `در آن` | `اگه`, `مگه`, `دیگه`, `واسه / برا`, `توش` |
| Clitic Pronouns | `بقیه‌اش`, `کارتان`, `به او`, `از او` | `بقیه‌ش`, `کارتون`, `بهش`, `ازش` |

<!-- fa-check-ignore-end -->

---

## 4. Deep Rules per Register

### A. `formal-human` (`رسمی روان`) — Avoiding the Two Traps
Models fail here in two opposite ways:
1. **The Bureaucracy Trap:** Writing `می‌باشد`, `گردید`, `جهت`, `در خصوص`, `مورد بررسی قرار گرفت`. Replace with `است`, `شد`, `برای`, `دربارهٔ`, `بررسی شد`.
2. **The Sloppy-Warmth Trap:** Trying to sound "human" in a proposal or contract by dropping in chat idioms like `کار رو جمع می‌کنیم`, `خیالتون راحت`, `ردیفه`, `رهایتان نمی‌کنیم`. Warmth in formal Persian comes from **clarity, concrete numbers, active verbs, and direct `شما`**—not street slang.

### B. `formal-admin` (`نامه اداری`) — Fixed Furniture
An administrative letter uses standard formal-human verbs (`است`, `می‌شود`, never `می‌باشد`) inside a strict structural frame:
- **Header:** `موضوع: [یک خط دقیق و کوتاه]`
- **Recipient:** `جناب آقای / سرکار خانم [نام خانوادگی]` یا `ریاست / مدیریت محترم [نام سازمان / واحد]`
- **Opener:** `با سلام و احترام؛` (do not stack `احتراماً، با تقدیم احترام به استحضار عالی می‌رساند...`).
- **Body:** 1–2 short paragraphs. State the reference/date, the concrete fact, and the single request (`خواهشمند است دستور فرمایید...`).
- **Closer:** `با تشکر و احترام` or `پیشاپیش از همکاری شما سپاسگزارم` + sender name/role.

### C. `full-colloquial` & Audio/Voiceover (`نریشن`)
- **Selective `ان → ون` vowel shift:** Shift everyday words (`خانه ← خونه`, `نان ← نون`, `زبان ← زبون`, `می‌دانم ← می‌دونم`, `آسان ← آسون`, `نشان ← نشون`, `خیابان ← خیابون`). **Never** shift formal/abstract/proper nouns (`ایران`, `انسان`, `جهان`, `امکان`, `داستان`, `پایان`, `سازمان`, `جریان`, `درمان`).
- **Spoken cadence for Voiceover/TTS:**
  - Keep clauses to **one breath** ($\le 12	ext{–}15$ words).
  - Avoid nested `که` relative clauses; chain short clauses with `و`, `ولی`, `چون`, or a pause.
  - Note for Persian TTS pipelines: standard written Persian (`رسمی روان`) reads cleaner in TTS engines unless full colloquial is specifically desired; never mix spoken verb endings (`می‌بره`) into a formal script.
