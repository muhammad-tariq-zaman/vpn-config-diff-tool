import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import parse, diff

class TestVpnConfigDiff(unittest.TestCase):
    def test_changed_detected(self):
        r = diff({"cipher": "AES-256-GCM"}, {"cipher": "AES-128-GCM"})
        self.assertEqual(r, [("CHANGED", "cipher", "AES-256-GCM", "AES-128-GCM")])

    def test_added_detected(self):
        r = diff({}, {"auth-user-pass": ""})
        self.assertEqual(r, [("ADDED", "auth-user-pass", "", "")])

    def test_removed_detected(self):
        r = diff({"comp-lzo": "no"}, {})
        self.assertEqual(r, [("REMOVED", "comp-lzo", "no", "")])

    def test_identical_no_diff(self):
        self.assertEqual(diff({"proto": "udp"}, {"proto": "udp"}), [])

    def test_comments_and_blanks_ignored(self):
        self.assertEqual(parse("# comment\n\nproto udp\n"), {"proto": "udp"})

    def test_key_value_syntax(self):
        self.assertEqual(parse("cipher=AES-256-GCM\n"), {"cipher": "AES-256-GCM"})

    def test_flag_key_has_empty_value(self):
        self.assertEqual(parse("auth-user-pass\n"), {"auth-user-pass": ""})

    def test_sorted_by_key(self):
        r = diff({"zebra": "1", "apple": "1"}, {"zebra": "2", "apple": "2"})
        self.assertEqual([x[1] for x in r], ["apple", "zebra"])

    def test_empty_files(self):
        self.assertEqual(diff(parse(""), parse("")), [])
