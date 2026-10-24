#!/usr/bin/env python3
"""
fa_check.py — Deterministic Persian Writing Linter, Register-Consistency Gate & Safe Auto-Fixer.

Zero third-party dependencies (Python 3.8+ stdlib only).

Checks 8 layers of Persian writing quality:
  1. Character hygiene: Arabic ي / ك / ى / ة and Arabic-Indic digits ٠-٩
  2. Banned bureaucratic & AI fossil phrases (می‌باشد، گردید، در راستای، لازم به ذکر است...)
  3. Syntactic & lexical calques (توسط + passive, مورد ... قرار گرفتن, نه تنها... بلکه همچنین...)
  4. Fake tanvin (گاهاً، دوماً، ناچاراً...) & missing required tanvin (لطفا → لطفاً...)
  5. ZWNJ (نیم‌فاصله) mechanics: می/نمی prefixes, ها plurals, تر/ترین, silent-ه clitics
  6. The هکسره trap (کتابه من vs این کتابه) & spaced silent-ه ezafe (خانه ی من)
  7. Register-consistency grep (کتابی vs شکسته mixing outside quotations)
  8. Punctuation, digits & sentence rhythm (em-dashes, ASCII punctuation, که-chains, CV)

Usage:
  python3 scripts/fa_check.py --check file.md [file2.txt ...]
  cat draft.md | python3 scripts/fa_check.py --check -
  python3 scripts/fa_check.py --check --register formal-human file.md
  python3 scripts/fa_check.py --check --json file.md
  python3 scripts/fa_check.py --fix file.md
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ZWNJ = "\u200c"
FA_LETTERS = r"\u0621-\u063a\u0641-\u064a\u067e\u0686\u0698\u06a9\u06af\u06cc\u0629\u0649\u06c0\u0654"
FA_WORD_CHAR = FA_LETTERS + ZWNJ
FA_BOUND_L = rf"(?<![{FA_WORD_CHAR}])"
FA_BOUND_R = rf"(?![{FA_WORD_CHAR}\u064b-\u0652])"

ARABIC_CHARS = {
    "\u064a": ("ی", "Arabic Yeh (ي U+064A) → Persian Yeh (ی U+06CC)"),
    "\u0649": ("ی", "Alef Maksura (ى U+0649) → Persian Yeh (ی U+06CC)"),
    "\u0643": ("ک", "Arabic Kaf (ك U+0643) → Persian Kaf (ک U+06A9)"),
    "\u0629": ("ه", "Arabic Teh Marbuta (ة U+0629) → Persian Heh (ه)"),
}
ARABIC_INDIC_DIGITS = {
    "٠": "۰", "١": "۱", "٢": "۲", "٣": "۳", "٤": "۴",
    "٥": "۵", "٦": "۶", "٧": "۷", "٨": "۸", "٩": "۹",
}
ASCII_TO_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

# 1. Hard-banned bureaucratic & AI fossils (🔴 Error in all registers)
BANNED_FOSSILS: List[Tuple[str, str, str]] = [
    (r"می[\u200c\s]?باشد|می[\u200c\s]?باشند|نمی[\u200c\s]?باشد|نمی[\u200c\s]?باشند", "banned-fossil", "Replace «می‌باشد/نمی‌باشد» with «است/نیست» or a specific verb"),
    (r"گردید(?:ه\s+است|ند|ه)?", "banned-fossil", "Replace bureaucratic «گردید» with «شد»"),
    (r"(?:اقدام\s+به\s+[^\s.]+\s+)?نمود(?:ند|یم|ید|ه\s+است|ن)?", "banned-fossil", "Replace bureaucratic «نمود» with «کرد»"),
    (r"لازم\s+به\s+ذکر\s+است|شایان\s+ذکر\s+است|قابل\s+توجه\s+است\s+که|ناگفته\s+نماند\s+که", "banned-fossil", "Delete ceremonial throat-clearing; state the point directly"),
    (r"در\s+راستای|در\s+همین\s+راستا|در\s+جهت\s+نیل\s+به", "banned-fossil", "Replace «در راستای» with «برای»"),
    (r"از\s+اهمیت\s+(?:ویژه[\u200c\s]?ای|بالایی|بسزایی)\s+برخوردار", "banned-fossil", "Replace inflated «از اهمیت ... برخوردار است» with «بسیار مهم است» or concrete impact"),
    (r"نقش\s+(?:بسزایی|کلیدی|مهمی)\s+(?:در\s+[^.،؛]+\s+)?ایفا\s+می[\u200c\s]?کن", "banned-fossil", "Replace «نقش بسزایی ایفا می‌کند» with a concrete verb"),
    (r"در\s+دنیای\s+امروز|در\s+عصر\s+دیجیتال|امروزه\s+با\s+پیشرفت", "banned-fossil", "Delete generic AI scene-setting opener; start with the core point"),
    (r"در\s+نهایت\s+می[\u200c\s]?توان\s+گفت|به\s+طور\s+کلی\s+می[\u200c\s]?توان\s+گفت", "banned-fossil", "Delete generic summary opener; end with a concrete fact or action"),
    (r"امیدوار(?:م|یم)\s+این\s+مطلب\s+برای\s+شما\s+مفید", "banned-fossil", "Delete chatbot sign-off residue"),
    (r"به\s+شمار\s+می[\u200c\s]?رود|به\s+حساب\s+می[\u200c\s]?آید|محسوب\s+می[\u200c\s]?شود", "banned-fossil", "Replace «محسوب می‌شود / به شمار می‌رود» with «است»"),
    (r"مورد\s+[آ-ی]+\s+قرار\s+(?:گرفت|می[\u200c\s]?گیرد|دهید|داد|بگیرد)", "banned-fossil", "Replace nominalization wrapper «مورد X قرار گرفتن/دادن» with simple verb «X شدن/کردن»"),
    (r"به\s+عمل\s+آورد|صورت\s+می[\u200c\s]?پذیرد|صورت\s+پذیرفت", "banned-fossil", "Replace bureaucratic compound with a simple active verb"),
]

# 2. Calque / Translationese signals (🟡 Warning)
CALQUE_PATTERNS: List[Tuple[str, str, str]] = [
    (r"توسط\s+[آ-ی]+", "calque-passive-tavassot", "Avoid «توسط + actor» passive calque; rewrite in active voice with the actor as subject"),
    (r"نه[\u200c\s]+تنها\s+[^.؟!]+بلکه\s+همچنین", "calque-not-only-but-also", "English «not only... but also» calque; use «هم ... و هم ...» or «علاوه بر»"),
    (r"شما\s+را\s+قادر\s+می[\u200c\s]?سازد|قادر\s+می[\u200c\s]?سازد\s+تا", "calque-enables-you", "Calque of «enables you to»; use «به شما امکان می‌دهد» or «کمکتان می‌کند»"),
    (r"در\s+پایان\s+روز", "calque-end-of-day", "Calque of «at the end of the day»; use «در نهایت» or «آخرش»"),
    (r"بهترین\s+نسخه[\u200cٔ\s]?ی?\s+خود(?:تان|ت)?", "calque-best-version", "Calque of «best version of yourself»; state the specific benefit"),
    (r"شیرجه\s+بزنیم\s+(?:به|در)|نگاهی\s+بیندازیم\s+به", "calque-dive-into", "Calque of «dive into / take a look at»; use «بررسی کنیم» or «بریم سراغ»"),
    (r"پتانسیل\s+خود\s+را\s+آزاد", "calque-unlock-potential", "Calque of «unlock your potential»; state the concrete capability"),
    (r"که\s+نشان[\u200c\s]?دهنده(?:ٔ|‌ی|\s+ی)?\s+[^.،؛]+است|که\s+بیانگر\s+[^.،؛]+است", "ai-tacked-participle", "Tacked-on «که نشان‌دهندهٔ ... است» tail; delete or make a concrete sentence"),
]

# 3. Fake tanvin (🔴 Error) vs. Missing required tanvin (🟡 Fixable)
FAKE_TANVIN = {
    "گاهاً": "گاهی", "گاها": "گاهی",
    "دوماً": "دوم اینکه", "سوماً": "سوم اینکه", "چهارماً": "چهارم اینکه",
    "تلفناً": "تلفنی", "زباناً": "زبانی", "ناچاراً": "به‌ناچار", "اقلاً": "دست‌کم",
}
REQUIRED_TANVIN = {
    "لطفا": "لطفاً", "حتما": "حتماً", "واقعا": "واقعاً", "اصلا": "اصلاً",
    "کاملا": "کاملاً", "مثلا": "مثلاً", "معمولا": "معمولاً", "تقریبا": "تقریباً",
    "دقیقا": "دقیقاً", "فعلا": "فعلاً", "قطعا": "قطعاً", "اتفاقا": "اتفاقاً",
    "احتمالا": "احتمالاً", "مخصوصا": "مخصوصاً", "اساسا": "اساساً", "عملا": "عملاً",
    "صرفا": "صرفاً", "نسبتا": "نسبتاً", "عمدتا": "عمدتاً",
}

# 4. Register markers (کتابی vs شکسته)
FORMAL_ONLY_MARKERS = [
    (r"می[‌]?شود|نمی[‌]?شود|می[‌]?شوند|نمی[‌]?شوند", "می‌شود/نمی‌شود"),
    (r"می[‌]?کند|نمی[‌]?کند|می[‌]?کنند|نمی[‌]?کنند", "می‌کند/می‌کنند"),
    (r"می[‌]?گوید|می[‌]?گویند|می[‌]?دهد|می[‌]?دهند|بدهید|بگویید|بگذارید", "می‌گوید/می‌دهد/بدهید"),
    (r"می[‌]?توانم|می[‌]?توانید|می[‌]?تواند|می[‌]?توانند|می[‌]?خواهم|می[‌]?خواهد|می[‌]?خواهند", "می‌توانید/می‌خواهم"),
    (r"آن[‌]?ها|این[‌]?ها", "آن‌ها/این‌ها"),
    (r"دیگر|اگر|مگر", "دیگر/اگر/مگر"),
]
SPOKEN_VERBS_AND_PARTICLES = [
    (r"ن?می[‌]?(?:شه|شم|شی|شیم|شید|شن)", "میشه/نمیشه"),
    (r"ن?می[‌]?(?:کنه|کنن)", "می‌کنه/می‌کنن"),
    (r"ن?می[‌]?(?:گه|گن|ده|دن|ره|رن|خوام|خوای|خواد|خوایم|خواید|خوان|تونم|تونی|تونه|تونیم|تونید|تونن|دونم|دونی|دونه|دونیم|دونید|دونن|اد|ان)", "spoken-verb"),
    (r"بذار|بذارید|بذاریم|بدید|بگید|برید", "spoken-imperative"),
    (r"دیگه|اگه|مگه", "دیگه/اگه/مگه"),
]
FULL_COLLOQUIAL_ONLY = [
    (r"(?<!از\s)(?<!به\s)(?<!پیش\s)(?<!رو\sبه\s)(?<!رو\sدر\s)رو(?!\s+(?:به\s+رو|در\s+رو|شد|کرد|افتاد|برگرداند|داد|انداخت))", "رو (object marker)"),
    (r"اون|اونا|اینا|همون|واسه|توش|بهش|ازش|خونه|چیزا|وقتا", "اون/اونا/واسه/توش/بهش/خونه"),
]

# 5. هکسره detection (words ending in consonant + ه followed by pronoun/modifier)
CONSONANT_STEMS_FOR_HE_KASRE = (
    "کتاب|دست|کار|دل|اسم|پول|حرف|چشم|سر|پا|لب|گوش|فکر|حس|راه|ماه|سال|روز|"
    "شب|وقت|نفر|چیز|جا|میز|کیف|کفش|لباس|ماشین|گوشی|تلفن|سایت|فایل|کد|لینک|"
    "اکانت|حساب|رمز|پسورد|سفارش|فرم|متن|پیام|پست|کانال|پیج|برند|تیم|شرکت|مشتری|"
    "محصول|دستگاه|کلید|سنسور|پکیج|فاکتور|قرارداد"
)
PRONOUNS_AND_MODS = (
    "من|تو|ما|شما|او|اون|اونا|اینا|ایشون|خودم|خودت|خودش|خودمون|خودتون|"
    "جدید|قدیمی|خوب|بد|بزرگ|کوچیک|کوچک|اول|دوم|اصلی|بعدی|قبلی|دیگه|دیگر"
)
RE_HE_KASRE = re.compile(
    rf"{FA_BOUND_L}({CONSONANT_STEMS_FOR_HE_KASRE})ه\s+({PRONOUNS_AND_MODS}){FA_BOUND_R}"
)

# Silent-ه followed by spaced ی (خانه ی من → خانه‌ی من)
SILENT_HE_WORDS = (
    "خانه|خونه|نامه|برنامه|هفته|پروژه|مدرسه|نقشه|جمعه|قهوه|بچه|شنبه|دقیقه|ثانیه|"
    "پنجره|اندازه|سفره|کوچه|میوه|لحظه|جمله|مرحله|نتیجه|مقاله|هزینه|گزینه|نمونه|"
    "زمینه|دسته|بسته|پوشه|شبکه|حوزه|دوره|چهره|سلیقه|علاقه|سابقه|تجربه|قطعه|منطقه|"
    "فاصله|مجموعه|مسئله|وسیله|هدیه|اجاره|اداره|اشاره|ستاره|ساده|آماده|ایده|شماره|"
    "اجازه|انگیزه|اندیشه|بهانه|نشانه|خاطره|پرونده|آینده|گذشته|رابطه|قاعده|معامله|"
    "محاسبه|مطالعه|مراجعه|مصاحبه|مقایسه|صفحه|نسخه|حرفه|نقطه|کلمه|واژه"
)
RE_SPACED_SILENT_HE_YE = re.compile(
    rf"{FA_BOUND_L}({SILENT_HE_WORDS})\s+ی\s+([{FA_LETTERS}]+)"
)
RE_SILENT_HE_CLITIC = re.compile(
    rf"{FA_BOUND_L}({SILENT_HE_WORDS})\s+(ام|ات|اش|ایم|اید|اند|ای){FA_BOUND_R}"
)

# ZWNJ patterns: spaced می / نمی before verb stems, attached میشود, spaced ها / تر / ترین
RE_SPACED_MI = re.compile(rf"{FA_BOUND_L}(ن?می)\s+([{FA_LETTERS}]{{2,}}){FA_BOUND_R}")
# Common nouns/words after "می" or "نمی" that are NOT verbs (extremely rare, e.g. می ناب)
MI_NON_VERBS = {"ناب", "انگور", "سرخ", "تلخ", "صافی"}

RE_ATTACHED_MI_FORMAL = re.compile(
    rf"{FA_BOUND_L}(ن?می)(شود|شوند|کند|کنند|گوید|گویند|دهد|دهند|تواند|توانند|توانم|توانی|توانیم|توانید|خواهد|خواهند|خواهم|خواهی|خواهیم|خواهید|رسد|رسند|آید|آیند|رود|روند|باشد|باشند|"
    rf"شه|شم|شی|شیم|شید|شن|کنم|کنی|کنه|کنیم|کنید|کنن|گم|گی|گه|گیم|گید|گن|دم|دی|ده|دیم|دید|دن|رم|ری|ره|ریم|رید|رن|"
    rf"خوام|خوای|خواد|خوایم|خواید|خوان|تونم|تونی|تونه|تونیم|تونید|تونن|ذارم|ذاری|ذاره|ذاریم|ذارید|ذارن|گذره|گذرن|"
    rf"ریزم|ریزی|ریزه|ریزیم|ریزید|ریزن|ارم|اری|اره|اریم|ارید|ارن|بینم|بینی|بینه|بینیم|بینید|بینن|"
    rf"خورم|خوری|خوره|خوریم|خورید|خورن|خرم|خری|خره|خریم|خرید|خرن|سازم|سازی|سازه|سازیم|سازید|سازن|"
    rf"مونم|مونی|مونه|مونیم|مونید|مونن|زنم|زنی|زنه|زنیم|زنید|زنن){FA_BOUND_R}"
)
RE_DROPPED_SILENT_HE = re.compile(
    rf"{FA_BOUND_L}(آماد|ساد|خست|برند|آیند|گذشت|نتیج|مز|خان|خون|بچ|صفح|نسخ|پروژ|برنام|هفت|فاصل|حافظ|سابق|تجرب|علاق|سلیق)(س|ست|ش|م|ت|مون|تون|شون){FA_BOUND_R}"
)

# Spaced plural ها (excluding standalone demonstratives/pronouns or non-plural contexts)
HA_EXCLUDE_PREV = {"آن", "این", "همان", "چنین", "همه", "به", "از", "در", "با", "تا", "که", "نه", "و", "یا"}
RE_SPACED_HA = re.compile(rf"{FA_BOUND_L}([{FA_LETTERS}]{{2,}})\s+(ها(?:ی|یی|یم|یت|یش|یمان|یتان|یشان)?){FA_BOUND_R}")

# Spaced comparative تر / ترین
TAR_EXCLUDE_PREV = {"از", "به", "با", "در", "که", "و", "یا", "نه", "خیلی", "بسیار", "کمی", "چند", "هرچه"}
RE_SPACED_TAR = re.compile(rf"{FA_BOUND_L}([{FA_LETTERS}]{{2,}})\s+(ترین?){FA_BOUND_R}")

# Spaced compound prefixes بی / هم
RE_SPACED_BI_HAM = re.compile(
    rf"{FA_BOUND_L}(بی|هم)\s+(دقت|توجه|نتیجه|معنی|معنا|هدف|نقص|نظیر|سابقه|تفاوت|مورد|ربط|انگیزه|زمان|وطن|زبان|صدا|فکر|گام|مسیر|راستا|جهت|سطح|شکل|نام|وزن){FA_BOUND_R}"
)


def strip_protected_regions(text: str) -> Tuple[str, List[str]]:
    """Replace fenced code blocks, inline code, URLs, HTML comments, and ignore blocks with placeholders."""
    tokens: List[str] = []

    def save(m: re.Match) -> str:
        idx = len(tokens)
        tokens.append(m.group(0))
        # Preserve newline count so line numbers stay exact
        nl = "\n" * m.group(0).count("\n")
        return f"__FAPROT_{idx}__{nl}"

    # 0. YAML frontmatter
    text = re.sub(r"\A---\n.*?\n---\n", save, text, flags=re.DOTALL)
    # 1. Ignore blocks
    text = re.sub(r"<!--\s*fa-(?:check|lint)-ignore-start\s*-->.*?<!--\s*fa-(?:check|lint)-ignore-end\s*-->", save, text, flags=re.DOTALL)
    text = re.sub(r"<!--\s*fa-(?:check|lint)-ignore-next-line\s*-->\n[^\n]*", save, text)
    # 2. Fenced code blocks
    text = re.sub(r"```.*?```", save, text, flags=re.DOTALL)
    # 3. Inline code
    text = re.sub(r"`[^`\n]+`", save, text)
    # 4. URLs and emails
    text = re.sub(r"https?://[^\s)\]>«»]+", save, text)
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", save, text)
    return text, tokens


def restore_protected_regions(text: str, tokens: List[str]) -> str:
    for idx in range(len(tokens) - 1, -1, -1):
        # Match placeholder + its preserved newlines
        nl = "\n" * tokens[idx].count("\n")
        text = text.replace(f"__FAPROT_{idx}__{nl}", tokens[idx])
    return text



def is_persian_dominant(line: str) -> bool:
    fa_count = len(re.findall(rf"[{FA_LETTERS}]", line))
    en_count = len(re.findall(r"[A-Za-z]", line))
    return fa_count > 0 and fa_count >= en_count

def strip_quotations(text: str) -> str:
    """Remove text inside «...» or "..." when checking register mixing so direct quotes don't false-positive."""
    text = re.sub(r"«[^»]{1,200}»", " ", text)
    text = re.sub(r'"[^"\n]{1,200}"', " ", text)
    return text


def analyze_text(raw_text: str, expected_register: str = "auto") -> Dict:
    cleaned, _ = strip_protected_regions(raw_text)
    lines = cleaned.splitlines()
    issues: List[Dict] = []

    def add_issue(severity: str, category: str, line_no: int, match_str: str, message: str):
        issues.append({
            "severity": severity,  # "error" | "warning"
            "category": category,
            "line": line_no,
            "match": match_str.strip()[:60],
            "message": message,
        })

    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        # 1. Character hygiene
        for ar_ch, (fa_ch, desc) in ARABIC_CHARS.items():
            if ar_ch in line:
                add_issue("error", "arabic-char", idx, ar_ch, desc)
        for ar_dig, fa_dig in ARABIC_INDIC_DIGITS.items():
            if ar_dig in line:
                add_issue("error", "arabic-digit", idx, ar_dig, f"Arabic-Indic digit {ar_dig} → Persian {fa_dig}")

        # 2. Banned bureaucratic & AI fossils
        for pat, cat, msg in BANNED_FOSSILS:
            for m in re.finditer(FA_BOUND_L + f"(?:{pat})" + FA_BOUND_R, line):
                add_issue("error", cat, idx, m.group(0), msg)

        # 3. Syntactic & lexical calques
        for pat, cat, msg in CALQUE_PATTERNS:
            for m in re.finditer(FA_BOUND_L + f"(?:{pat})" + FA_BOUND_R, line):
                add_issue("warning", cat, idx, m.group(0), msg)

        # 4. Fake tanvin & missing required tanvin
        for bad, good in FAKE_TANVIN.items():
            for m in re.finditer(FA_BOUND_L + re.escape(bad) + FA_BOUND_R, line):
                add_issue("error", "fake-tanvin", idx, m.group(0), f"Fake tanvin: replace «{bad}» with «{good}»")
        for bare, req in REQUIRED_TANVIN.items():
            for m in re.finditer(FA_BOUND_L + re.escape(bare) + FA_BOUND_R, line):
                add_issue("warning", "missing-tanvin", idx, m.group(0), f"Missing tanvin: write «{req}»")

        # 5. ZWNJ checks
        for m in RE_SPACED_MI.finditer(line):
            stem = m.group(2)
            if stem not in MI_NON_VERBS:
                add_issue("error", "zwnj-mi", idx, m.group(0), f"Use ZWNJ after {m.group(1)}: «{m.group(1)}{ZWNJ}{stem}»")

        for m in RE_ATTACHED_MI_FORMAL.finditer(line):
            add_issue("error", "zwnj-mi-attached", idx, m.group(0), f"Insert ZWNJ after {m.group(1)}: «{m.group(1)}{ZWNJ}{m.group(2)}»")
        for m in RE_DROPPED_SILENT_HE.finditer(line):
            suffix = "ست" if m.group(2) in ("س", "ست") else m.group(2)
            add_issue("error", "dropped-silent-he", idx, m.group(0), f"Preserve silent ه with ZWNJ: «{m.group(1)}ه{ZWNJ}{suffix}»")

        for m in RE_SPACED_HA.finditer(line):
            prev_w = m.group(1)
            if prev_w not in HA_EXCLUDE_PREV:
                add_issue("error", "zwnj-ha", idx, m.group(0), f"Attach plural with ZWNJ: «{prev_w}{ZWNJ}{m.group(2)}»")

        for m in RE_SPACED_TAR.finditer(line):
            prev_w = m.group(1)
            if prev_w not in TAR_EXCLUDE_PREV:
                add_issue("error", "zwnj-tar", idx, m.group(0), f"Attach comparative with ZWNJ: «{prev_w}{ZWNJ}{m.group(2)}»")

        for m in RE_SPACED_BI_HAM.finditer(line):
            add_issue("error", "zwnj-prefix", idx, m.group(0), f"Use ZWNJ in compound: «{m.group(1)}{ZWNJ}{m.group(2)}»")

        for m in RE_SILENT_HE_CLITIC.finditer(line):
            add_issue("error", "zwnj-clitic", idx, m.group(0), f"Use ZWNJ after silent ه: «{m.group(1)}{ZWNJ}{m.group(2)}»")

        # 6. هکسره & spaced silent-ه ezafe
        for m in RE_HE_KASRE.finditer(line):
            add_issue("error", "he-kasre", idx, m.group(0), f"هکسره error: «{m.group(1)}ه {m.group(2)}» → «{m.group(1)} {m.group(2)}» (ezafe is never written as ـه)")

        for m in RE_SPACED_SILENT_HE_YE.finditer(line):
            add_issue("error", "spaced-ezafe-ye", idx, m.group(0), f"Use ZWNJ or hamza for ezafe: «{m.group(1)}{ZWNJ}ی {m.group(2)}» or «{m.group(1)}ٔ {m.group(2)}»")

        # 7. Punctuation & typography
        if is_persian_dominant(line) and ("—" in line or " -- " in line):
            add_issue("error", "em-dash", idx, "—", "Em-dash is an English AI tell in Persian; use «،», «؛», parentheses, or a period")

        # ASCII comma/question/semicolon adjacent to Persian characters
        for m in re.finditer(rf"[{FA_LETTERS}]\s*([,;?])", line):
            rep = {",": "،", ";": "؛", "?": "؟"}[m.group(1)]
            add_issue("error", "ascii-punct", idx, m.group(0), f"Use Persian punctuation «{rep}» instead of ASCII «{m.group(1)}»")

        # ASCII digits adjacent to Persian words (outside Latin tokens like ESP32, v2, 4G/5G)
        if is_persian_dominant(line):
            for m in re.finditer(rf"(?<![A-Za-z0-9_/-])([0-9]+)(?![A-Za-z0-9_/-])", line):
                add_issue("warning", "ascii-digit", idx, m.group(1), f"Use Persian digits «{m.group(1).translate(ASCII_TO_FA_DIGITS)}» in Persian prose")

    # 8. Document-level Register Consistency Check (outside quotes)
    unquoted = strip_quotations(cleaned)
    formal_hits: List[str] = []
    spoken_hits: List[str] = []
    full_colloq_hits: List[str] = []

    for pat, label in FORMAL_ONLY_MARKERS:
        for m in re.finditer(FA_BOUND_L + f"(?:{pat})" + FA_BOUND_R, unquoted):
            formal_hits.append(m.group(0))
    for pat, label in SPOKEN_VERBS_AND_PARTICLES:
        for m in re.finditer(FA_BOUND_L + f"(?:{pat})" + FA_BOUND_R, unquoted):
            spoken_hits.append(m.group(0))
    for pat, label in FULL_COLLOQUIAL_ONLY:
        for m in re.finditer(FA_BOUND_L + f"(?:{pat})" + FA_BOUND_R, unquoted):
            full_colloq_hits.append(m.group(0))

    if expected_register in ("formal-human", "formal-admin", "semi-formal", "formal"):
        if spoken_hits or full_colloq_hits:
            sample = ", ".join(sorted(set(spoken_hits + full_colloq_hits))[:5])
            add_issue("error", "register-leak-spoken", 1, sample, f"Spoken/colloquial forms leaked into {expected_register} register: {sample}")
    elif expected_register == "light-colloquial":
        if formal_hits:
            sample = ", ".join(sorted(set(formal_hits))[:5])
            add_issue("error", "register-leak-formal", 1, sample, f"Formal written verbs leaked into light-colloquial register: {sample}")
        if full_colloq_hits:
            sample = ", ".join(sorted(set(full_colloq_hits))[:5])
            add_issue("warning", "register-leak-slang", 1, sample, f"Heavy colloquial markers («رو/اون/واسه») used in light-colloquial UI register: {sample}")
    elif expected_register == "full-colloquial":
        if formal_hits:
            sample = ", ".join(sorted(set(formal_hits))[:5])
            add_issue("error", "register-leak-formal", 1, sample, f"Formal written forms leaked into full-colloquial register: {sample}")
    else:
        # Auto mode: flag if BOTH formal-only verb/particle markers and spoken verb/particle markers appear
        if formal_hits and (spoken_hits or full_colloq_hits):
            f_sample = ", ".join(sorted(set(formal_hits))[:4])
            s_sample = ", ".join(sorted(set(spoken_hits + full_colloq_hits))[:4])
            add_issue(
                "error",
                "register-mix",
                1,
                f"{f_sample} vs {s_sample}",
                f"Register mixing detected! Written forms ({f_sample}) mixed with spoken forms ({s_sample})",
            )

    # 9. Sentence Rhythm & که-chain check
    sentences = [s.strip() for s in re.split(r"[.؟!\n]+", unquoted) if len(s.split()) >= 3]
    sent_lengths = [len(s.split()) for s in sentences]
    cv: Optional[float] = None
    if len(sent_lengths) >= 5:
        mean = sum(sent_lengths) / len(sent_lengths)
        if mean > 0:
            std = math.sqrt(sum((x - mean) ** 2 for x in sent_lengths) / len(sent_lengths))
            cv = round(std / mean, 2)
            if sum(sent_lengths) >= 120 and cv < 0.30:
                add_issue("warning", "flat-rhythm", 1, f"CV={cv}", f"Monotonous sentence length (CV={cv} < 0.30); vary short and medium sentences")

    for s in sentences:
        ke_count = len(re.findall(FA_BOUND_L + r"که" + FA_BOUND_R, s))
        if ke_count >= 3:
            add_issue("warning", "ke-chain", 1, s[:55] + "...", f"Sentence chains {ke_count} «که» clauses; split into shorter sentences")

    error_count = sum(1 for i in issues if i["severity"] == "error")
    warn_count = sum(1 for i in issues if i["severity"] == "warning")
    word_count = len(cleaned.split())

    return {
        "ok": error_count == 0,
        "error_count": error_count,
        "warning_count": warn_count,
        "word_count": word_count,
        "sentence_count": len(sent_lengths),
        "rhythm_cv": cv,
        "detected_formal_markers": sorted(set(formal_hits))[:8],
        "detected_spoken_markers": sorted(set(spoken_hits + full_colloq_hits))[:8],
        "issues": issues,
    }


def safe_fix_text(raw_text: str, convert_digits: bool = True) -> str:
    """Apply safe, deterministic orthographic fixes without altering tone or meaning."""
    text, tokens = strip_protected_regions(raw_text)

    # 1. Arabic characters & digits
    for ar_ch, (fa_ch, _) in ARABIC_CHARS.items():
        text = text.replace(ar_ch, fa_ch)
    for ar_dig, fa_dig in ARABIC_INDIC_DIGITS.items():
        text = text.replace(ar_dig, fa_dig)

    # 2. Fake tanvin & missing required tanvin
    for bad, good in FAKE_TANVIN.items():
        text = re.sub(FA_BOUND_L + re.escape(bad) + FA_BOUND_R, good, text)
    for bare, req in REQUIRED_TANVIN.items():
        text = re.sub(FA_BOUND_L + re.escape(bare) + FA_BOUND_R, req, text)

    # 3. ZWNJ fixes
    def _fix_mi(m: re.Match) -> str:
        if m.group(2) in MI_NON_VERBS:
            return m.group(0)
        return f"{m.group(1)}{ZWNJ}{m.group(2)}"

    text = RE_SPACED_MI.sub(_fix_mi, text)
    text = RE_ATTACHED_MI_FORMAL.sub(rf"\1{ZWNJ}\2", text)
    text = RE_DROPPED_SILENT_HE.sub(lambda m: f"{m.group(1)}ه{ZWNJ}{'ست' if m.group(2) in ('س', 'ست') else m.group(2)}", text)

    def _fix_ha(m: re.Match) -> str:
        if m.group(1) in HA_EXCLUDE_PREV:
            return m.group(0)
        return f"{m.group(1)}{ZWNJ}{m.group(2)}"

    text = RE_SPACED_HA.sub(_fix_ha, text)

    def _fix_tar(m: re.Match) -> str:
        if m.group(1) in TAR_EXCLUDE_PREV:
            return m.group(0)
        return f"{m.group(1)}{ZWNJ}{m.group(2)}"

    text = RE_SPACED_TAR.sub(_fix_tar, text)
    text = RE_SPACED_BI_HAM.sub(rf"\1{ZWNJ}\2", text)
    text = RE_SILENT_HE_CLITIC.sub(rf"\1{ZWNJ}\2", text)
    text = RE_SPACED_SILENT_HE_YE.sub(rf"\1{ZWNJ}ی \2", text)
    text = RE_HE_KASRE.sub(r"\1 \2", text)

    # 4. Punctuation fixes next to Persian characters
    text = re.sub(rf"([{FA_LETTERS}])\s*,", r"\1،", text)
    text = re.sub(rf"([{FA_LETTERS}])\s*;", r"\1؛", text)
    text = re.sub(rf"([{FA_LETTERS}])\s*\?", r"\1؟", text)
    text = re.sub(r"\s*—\s*", "، ", text)

    # 5. Optional Persian digits on lines containing Persian script
    if convert_digits:
        fixed_lines = []
        for line in text.splitlines(keepends=True):
            if re.search(rf"[{FA_LETTERS}]", line):
                line = re.sub(
                    r"(?<![A-Za-z0-9_/-])([0-9]+)(?![A-Za-z0-9_/-])",
                    lambda m: m.group(1).translate(ASCII_TO_FA_DIGITS),
                    line,
                )
            fixed_lines.append(line)
        text = "".join(fixed_lines)

    return restore_protected_regions(text, tokens)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic Persian writing linter and safe auto-fixer.")
    parser.add_argument("files", nargs="*", default=["-"], help="Files to check/fix, or '-' for stdin")
    parser.add_argument("--check", action="store_true", default=True, help="Report issues (default)")
    parser.add_argument("--fix", action="store_true", help="Apply safe orthographic fixes in place (or to stdout for '-')")
    parser.add_argument(
        "--register",
        default="auto",
        choices=["auto", "formal", "formal-human", "formal-admin", "semi-formal", "light-colloquial", "full-colloquial"],
        help="Expected register for consistency enforcement",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    overall_ok = True
    reports = {}

    for fpath in args.files:
        if fpath == "-":
            content = sys.stdin.read()
        else:
            content = Path(fpath).read_text(encoding="utf-8")

        if args.fix:
            fixed = safe_fix_text(content)
            if fpath == "-":
                sys.stdout.write(fixed)
            else:
                Path(fpath).write_text(fixed, encoding="utf-8")
            content = fixed

        rep = analyze_text(content, expected_register=args.register)
        reports[fpath] = rep
        if not rep["ok"]:
            overall_ok = False

        if not args.json and not (args.fix and fpath == "-"):
            status = "PASS" if rep["ok"] else "FAIL"
            print(f"[{status}] {fpath} — {rep['error_count']} error(s), {rep['warning_count']} warning(s) ({rep['word_count']} words, CV={rep['rhythm_cv']})")
            for iss in rep["issues"]:
                icon = "🔴" if iss["severity"] == "error" else "🟡"
                print(f"  {icon} L{iss['line']} [{iss['category']}] «{iss['match']}» → {iss['message']}")

    if args.json:
        out = reports["-"] if len(reports) == 1 and "-" in reports else reports
        print(json.dumps(out, ensure_ascii=False, indent=2))

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
