import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("select_tag", Path(__file__).with_name("select-upstream-tag.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SelectUpstreamTagTest(unittest.TestCase):
    def release(self, tag, **extra):
        return {"tagName": tag, **extra}

    def test_numeric_order_and_prerelease_tags(self):
        tags = ["v1.9.9", "v1.10.0", "v1.99.0-rc1", "v2.0", "v03.0.0"]
        self.assertEqual("v1.10.0", module.select(tags, [self.release("v1.9.9-shizuku-clipboard")]))

    def test_equal_and_older_are_not_selected(self):
        self.assertIsNone(module.select(["v1.37.2"], [self.release("v1.37.2-shizuku-clipboard")]))
        self.assertIsNone(module.select(["v1.37.1"], [self.release("v1.37.2-shizuku-clipboard")]))

    def test_drafts_and_prereleases_do_not_count(self):
        releases = [self.release("v2.0.0-shizuku-clipboard", isDraft=True),
                    self.release("v3.0.0-shizuku-clipboard", isPrerelease=True)]
        self.assertEqual("v1.0.0", module.select(["v1.0.0"], releases))

    def test_missing_stable_upstream_fails_closed(self):
        with self.assertRaises(ValueError):
            module.select(["v1.0.0-rc1"], [])


if __name__ == "__main__":
    unittest.main()
