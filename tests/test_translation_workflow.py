import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "translate_post.py"
SPEC = importlib.util.spec_from_file_location("translate_post", SCRIPT)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)
TICK = chr(96)

class TranslationHelpersTests(unittest.TestCase):
    def test_front_matter_split_preserves_markdown_body(self):
        front, body = module.split_front_matter('---\ntitle: "Hello"\nlang: fa\n---\n\n## متن\n')
        self.assertIn('title: "Hello"', front)
        self.assertEqual(body, '\n## متن\n')

    def test_rejects_missing_front_matter(self):
        with self.assertRaises(ValueError):
            module.split_front_matter("# no front matter")

    def test_code_blocks_and_inline_code_are_restored_exactly(self):
        source = "Run " + TICK + "make test" + TICK + ":\n\n" + TICK*3 + "bash\nmake test\n# exact command\n" + TICK*3
        masked, tokens = module.mask_code(source)
        self.assertNotIn("make test", masked)
        self.assertEqual(module.restore_code(masked, tokens), source)

    def test_restore_rejects_missing_placeholder(self):
        _, tokens = module.mask_code(TICK + "secret_command" + TICK)
        with self.assertRaises(ValueError):
            module.restore_code("lost", tokens)

    def test_front_matter_value_update_does_not_duplicate_key(self):
        updated = module.set_front_matter_value('title: "Hello"\nlang: fa\n', "lang", "en")
        self.assertEqual(updated.count("lang:"), 1)
        self.assertIn('lang: "en"', updated)

    def test_layout_has_canonical_and_bilingual_alternates(self):
        layout = (SCRIPT.parents[2] / "_layouts" / "default.html").read_text(encoding="utf-8")
        self.assertIn('rel="canonical"', layout)
        self.assertIn('hreflang="fa"', layout)
        self.assertIn('hreflang="en"', layout)
        self.assertIn('hreflang="x-default"', layout)

    def test_sitemap_contains_bilingual_alternates_for_translated_posts(self):
        sitemap = (SCRIPT.parents[2] / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("post.translation_url", sitemap)
        self.assertIn('hreflang="fa"', sitemap)
        self.assertIn('hreflang="en"', sitemap)

if __name__ == "__main__":
    unittest.main()
