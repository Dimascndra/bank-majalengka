import os
import unittest
import re
from html.parser import HTMLParser

class TestSecondaryPages(unittest.TestCase):
    def setUp(self):
        self.pages = [
            "pages/tentang/sejarah.html",
            "pages/tentang/visi-misi.html",
            "pages/tentang/dewan-direktur.html",
            "pages/tentang/arti-logo.html",
            "pages/simpanan.html",
            "pages/kredit.html",
            "pages/simulasi-kredit.html",
            "pages/informasi.html",
            "pages/kontak.html",
            "pages/pengaduan-nasabah.html"
        ]

    def test_secondary_pages_structure(self):
        """Verify existence and core components of all secondary pages."""
        for p in self.pages:
            self.assertTrue(os.path.exists(p), f"Missing page: {p}")
            with open(p, "r", encoding="utf-8") as f:
                c = f.read()
            self.assertIn("navbar", c, f"Page {p} missing navbar")
            self.assertIn("Bank Majalengka", c, f"Page {p} missing 'Bank Majalengka'")
            self.assertIn("bg-footer", c, f"Page {p} missing footer 'bg-footer'")
            self.assertIn("copyright", c, f"Page {p} missing copyright element")
            self.assertIn("overlay-header", c, f"Page {p} missing banner 'overlay-header'")

    def test_relative_asset_paths(self):
        """Verify CSS, JS, and image asset paths are valid relative paths."""
        for p in self.pages:
            self.assertTrue(os.path.exists(p), f"Missing page: {p}")
            page_dir = os.path.dirname(p)
            with open(p, "r", encoding="utf-8") as f:
                c = f.read()

            # Find all stylesheet links
            css_matches = re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', c)
            for css in css_matches:
                clean_css = css.split('?')[0]
                target_path = os.path.normpath(os.path.join(page_dir, clean_css))
                self.assertTrue(os.path.exists(target_path), f"In {p}, CSS file not found: {clean_css} -> {target_path}")

            # Find all script src
            js_matches = re.findall(r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)["\']', c)
            for js in js_matches:
                clean_js = js.split('?')[0]
                target_path = os.path.normpath(os.path.join(page_dir, clean_js))
                self.assertTrue(os.path.exists(target_path), f"In {p}, JS file not found: {clean_js} -> {target_path}")

            # Find local img src
            img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', c)
            for img in img_matches:
                if img.startswith('http') or img.startswith('data:'):
                    continue
                clean_img = img.split('?')[0]
                target_path = os.path.normpath(os.path.join(page_dir, clean_img))
                self.assertTrue(os.path.exists(target_path), f"In {p}, image file not found: {clean_img} -> {target_path}")

    def test_page_specific_content(self):
        """Verify each page has appropriate content and title."""
        expected_content = {
            "pages/tentang/sejarah.html": ["Sejarah", "Perumda BPR Majalengka"],
            "pages/tentang/visi-misi.html": ["Visi", "Misi"],
            "pages/tentang/dewan-direktur.html": ["Dewan Direktur", "Direksi"],
            "pages/tentang/arti-logo.html": ["Arti Logo", "Makna"],
            "pages/simpanan.html": ["Simpanan", "Tabungan", "Deposito"],
            "pages/kredit.html": ["Kredit", "Pinjaman"],
            "pages/simulasi-kredit.html": ["Simulasi Kredit", "frmSimulasi", "Hitung Simulasi"],
            "pages/informasi.html": ["Informasi", "Berita"],
            "pages/kontak.html": ["Kontak", "Hubungi Kami", "Peta"]
        }

        for p, keywords in expected_content.items():
            with open(p, "r", encoding="utf-8") as f:
                c = f.read()
            for kw in keywords:
                self.assertIn(kw.lower(), c.lower(), f"Keyword '{kw}' not found in {p}")

if __name__ == "__main__":
    unittest.main()
