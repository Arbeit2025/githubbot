import unittest
from bot.label_logic import triage_issue, triage_pr, size_label

class TestIssue(unittest.TestCase):
    def test_bug_jp(self):
        p = triage_issue("ログインでエラーが出る", "再現手順: ログインすると500エラーになります")
        self.assertIn("bug", p.labels)
    def test_feature(self):
        p = triage_issue("機能の要望", "ダークモードを追加したいです。よろしくお願いします")
        self.assertIn("enhancement", p.labels)
    def test_needs_info_short_body(self):
        p = triage_issue("動きません", "")
        self.assertTrue(p.needs_info); self.assertIn("needs-info", p.labels)
    def test_question_no_needs_info(self):
        p = triage_issue("使い方の質問", "短い")
        self.assertFalse(p.needs_info)

class TestPR(unittest.TestCase):
    def test_file_labels(self):
        p = triage_pr("fix", ["docs/guide.md", ".github/workflows/ci.yml"], 30)
        self.assertIn("documentation", p.labels); self.assertIn("ci", p.labels)
        self.assertIn("size/S", p.labels)
    def test_size(self):
        self.assertEqual(size_label(10), "size/S")
        self.assertEqual(size_label(300), "size/L")
        self.assertEqual(size_label(9999), "size/XL")
    def test_deps(self):
        p = triage_pr("bump", ["requirements.txt"], 5)
        self.assertIn("dependencies", p.labels)

if __name__ == "__main__":
    unittest.main()
