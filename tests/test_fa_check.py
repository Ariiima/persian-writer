#!/usr/bin/env python3
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from fa_check import analyze_text, safe_fix_text


class TestFaCheck(unittest.TestCase):
    def test_clean_formal_text_passes(self):
        text = "این دستگاه هم درِ ورودی و هم جک پارکینگ را از روی گوشی باز می‌کند. نصب آن کمتر از ۳۰ دقیقه زمان می‌برد."
        rep = analyze_text(text, expected_register="formal-human")
        self.assertTrue(rep["ok"], msg=rep["issues"])
        self.assertEqual(rep["error_count"], 0)

    def test_clean_full_colloquial_passes(self):
        text = "اون فایل رو فرستادم، ببین دستت رسید؟ اگه مشکلی داره بگو تا همین الان درستش کنم."
        rep = analyze_text(text, expected_register="full-colloquial")
        self.assertTrue(rep["ok"], msg=rep["issues"])
        self.assertEqual(rep["error_count"], 0)

    def test_detects_banned_fossils(self):
        text = "در دنیای امروز، این سامانه از اهمیت ویژه‌ای برخوردار می‌باشد و در راستای اهداف شرکت طراحی گردید."
        rep = analyze_text(text)
        self.assertFalse(rep["ok"])
        cats = [i["category"] for i in rep["issues"]]
        self.assertGreaterEqual(cats.count("banned-fossil"), 4)

    def test_detects_register_mixing(self):
        text = "این قابلیت به شما کمک می‌کند تا کارها رو خیلی سریع‌تر انجام بدید و نتیجه را ببینید."
        rep = analyze_text(text, expected_register="auto")
        self.assertFalse(rep["ok"])
        cats = [i["category"] for i in rep["issues"]]
        self.assertIn("register-mix", cats)

    def test_detects_he_kasre_and_fake_tanvin(self):
        text = "گاهاً کتابه من و خانه ی ما در لیست دیده می شود."
        rep = analyze_text(text)
        self.assertFalse(rep["ok"])
        cats = {i["category"] for i in rep["issues"]}
        self.assertIn("fake-tanvin", cats)
        self.assertIn("he-kasre", cats)
        self.assertIn("spaced-ezafe-ye", cats)
        self.assertIn("zwnj-mi", cats)

    def test_safe_fix_repairs_orthography(self):
        raw = "لطفا كتاب ها و بزرگ ترين خانه ی ما را در 3 روز بررسی می كنيد?"
        fixed = safe_fix_text(raw)
        self.assertIn("لطفاً", fixed)
        self.assertIn("کتاب‌ها", fixed)
        self.assertIn("بزرگ‌ترین", fixed)
        self.assertIn("خانه‌ی ما", fixed)
        self.assertIn("۳", fixed)
        self.assertIn("می‌کنید؟", fixed)
        rep = analyze_text(fixed)
        self.assertTrue(rep["ok"], msg=rep["issues"])


if __name__ == "__main__":
    unittest.main()
