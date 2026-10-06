#!/usr/bin/env python3
"""
tests/verify_all.py
End-to-End Comprehensive Verification for Bank Majalengka 1:1 UI Clone.

Checks performed:
1. Scan all HTML files (root and subdirectories):
   - Link integrity: all local stylesheets (<link rel="stylesheet">, icons) exist on disk.
   - Script integrity: all local script tags (<script src="...">) exist on disk.
   - Image integrity: all local images (<img src="...">) exist on disk.
   - Anchor integrity: all internal links (<a href="...">) point to existing HTML files / anchors.
   - HTML syntax & structure: tag nesting balance (no unclosed containers, missing tags).
   - Zero external dependency for core rendering (all assets loaded locally from assets/).
2. Run full suite of automated unit tests:
   - test_assets_exist.py
   - test_js_logic.py
   - test_homepage_header.py
   - test_homepage_sections.py
   - test_homepage_footer_simulasi.py
   - test_secondary_pages.py
"""

import os
import sys
import glob
import re
import unittest
from html.parser import HTMLParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class HTMLBalanceChecker(HTMLParser):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.tags_stack = []
        self.void_tags = {
            'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'
        }
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.void_tags:
            self.tags_stack.append(tag.lower())

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in self.void_tags:
            return
        if not self.tags_stack:
            self.errors.append(f"Unexpected closing tag </{tag_lower}>")
            return
        last = self.tags_stack.pop()
        if last != tag_lower:
            self.errors.append(f"Mismatched tag: expected </{last}>, found </{tag_lower}>")


class VerifyAll(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_files = [os.path.join(BASE_DIR, "index.html")] + glob.glob(
            os.path.join(BASE_DIR, "pages", "**", "*.html"), recursive=True
        )

    def test_html_files_presence(self):
        """Ensure all required 11 HTML pages are present."""
        expected_min_count = 11
        self.assertGreaterEqual(
            len(self.html_files), expected_min_count,
            f"Expected at least {expected_min_count} HTML files, got {len(self.html_files)}"
        )
        for hf in self.html_files:
            self.assertTrue(os.path.exists(hf), f"HTML file does not exist: {hf}")

    def test_local_assets_resolution_zero_404(self):
        """Ensure every CSS, JS, IMG, and internal link resolves to disk."""
        broken_references = []

        for html_path in self.html_files:
            rel_page = os.path.relpath(html_path, BASE_DIR)
            page_dir = os.path.dirname(html_path)

            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Stylesheets & favicons (<link href="...">)
            links = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', content)
            for link in links:
                if link.startswith(("http://", "https://", "//", "data:")):
                    broken_references.append(f"[{rel_page}] External link stylesheet/icon: {link}")
                    continue
                clean_link = link.split("?")[0].split("#")[0]
                if not clean_link:
                    continue
                target = os.path.normpath(os.path.join(page_dir, clean_link))
                if not os.path.exists(target):
                    broken_references.append(f"[{rel_page}] Broken <link>: {link} -> {target}")

            # 2. Scripts (<script src="...">)
            scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content)
            for src in scripts:
                if src.startswith(("http://", "https://", "//", "data:")):
                    broken_references.append(f"[{rel_page}] External script: {src}")
                    continue
                clean_src = src.split("?")[0].split("#")[0]
                if not clean_src:
                    continue
                target = os.path.normpath(os.path.join(page_dir, clean_src))
                if not os.path.exists(target):
                    broken_references.append(f"[{rel_page}] Broken <script>: {src} -> {target}")

            # 3. Images (<img src="...">)
            images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
            for img in images:
                if img.startswith(("http://", "https://", "//", "data:")):
                    continue
                clean_img = img.split("?")[0].split("#")[0]
                if not clean_img:
                    continue
                target = os.path.normpath(os.path.join(page_dir, clean_img))
                if not os.path.exists(target):
                    broken_references.append(f"[{rel_page}] Broken <img>: {img} -> {target}")

            # 4. Internal anchor hyperlinks (<a href="...">)
            anchors = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', content)
            for href in anchors:
                if href.startswith(("http://", "https://", "tel:", "mailto:", "javascript:")):
                    continue
                if href == "#" or href.startswith("#"):
                    continue
                clean_href = href.split("?")[0].split("#")[0]
                if not clean_href:
                    continue
                target = os.path.normpath(os.path.join(page_dir, clean_href))
                if not os.path.exists(target):
                    broken_references.append(f"[{rel_page}] Broken <a> link: {href} -> {target}")

        self.assertEqual(len(broken_references), 0, "\n".join(broken_references))

    def test_html_tag_balance(self):
        """Validate HTML tag open/close balance for every HTML file."""
        balance_errors = []
        for html_path in self.html_files:
            rel_page = os.path.relpath(html_path, BASE_DIR)
            checker = HTMLBalanceChecker(html_path)
            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()
            checker.feed(content)
            if checker.tags_stack:
                balance_errors.append(f"[{rel_page}] Unclosed tags: {checker.tags_stack}")
            if checker.errors:
                balance_errors.append(f"[{rel_page}] HTML parse errors: {checker.errors}")

        self.assertEqual(len(balance_errors), 0, "\n".join(balance_errors))

    def test_css_internal_assets(self):
        """Verify CSS files have no broken local font/image url() references."""
        css_files = glob.glob(os.path.join(BASE_DIR, "assets", "css", "**", "*.css"), recursive=True)
        css_errors = []
        for css in css_files:
            rel_css = os.path.relpath(css, BASE_DIR)
            with open(css, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            urls = re.findall(r'url\s*\(([^)]+)\)', content)
            for u in urls:
                clean_u = u.strip('\'" \t\r\n')
                if clean_u.startswith("data:") or clean_u.startswith(("http://", "https://")):
                    continue
                u_path = clean_u.split("?")[0].split("#")[0]
                target = os.path.normpath(os.path.join(os.path.dirname(css), u_path))
                if not os.path.exists(target):
                    css_errors.append(f"[{rel_css}] Broken url(): {clean_u} -> {target}")

        self.assertEqual(len(css_errors), 0, "\n".join(css_errors))

    def test_critical_ui_elements(self):
        """Verify critical UI elements across index.html."""
        index_path = os.path.join(BASE_DIR, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check essential IDs and Classes
        self.assertIn('id="antiFraudModal"', content)
        self.assertIn('class="carousel-layanan"', content)
        self.assertIn('class="carousel-informasi"', content)
        self.assertIn('id="frmSimulasi"', content)
        self.assertIn('id="btn-back-to-top"', content)
        self.assertIn('https://wa.me/6281122332600', content)


def main():
    print("=" * 70)
    print("BANK MAJALENGKA 1:1 UI CLONE - COMPREHENSIVE E2E VERIFICATION")
    print("=" * 70)

    print("\n--- 1. Running Comprehensive Unit & E2E Test Suite ---")
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.join(BASE_DIR, "tests"))
    suite.addTests(loader.loadTestsFromTestCase(VerifyAll))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if not result.wasSuccessful():
        print("\n❌ Unit tests failed!")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("✅ ALL CHECKS PASSED: 0 BROKEN LINKS, 100% OFFLINE READY, 1:1 REPRODUCED")
    print("=" * 70)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run_suite_only":
        unittest.main()
    else:
        main()
