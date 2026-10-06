import os
import re
import unittest

class TestJsLogic(unittest.TestCase):
    def setUp(self):
        self.js_path = "assets/js/main.js"
        self.css_path = "assets/css/website.css"

    def test_main_js_functions(self):
        """Verify essential function and selector definitions exist in main.js."""
        self.assertTrue(os.path.exists(self.js_path), f"{self.js_path} does not exist")
        with open(self.js_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("formatRupiah", content)
        self.assertIn("carousel-layanan", content)
        self.assertIn("carousel-informasi", content)
        self.assertIn("antiFraudModal", content)

    def test_aos_and_news_truncation(self):
        """Verify AOS initialization and news card truncation logic exist in main.js."""
        self.assertTrue(os.path.exists(self.js_path), f"{self.js_path} does not exist")
        with open(self.js_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("AOS.init", content)
        self.assertIn("AOS.refresh", content)
        self.assertIn("news-card", content)
        self.assertIn("text-limit", content)
        self.assertIn("15", content)

    def test_format_rupiah_algorithm(self):
        """Verify the Python counterpart of formatRupiah produces expected output."""
        def py_format_rupiah(angka, prefix=None):
            if not angka:
                return ""
            number_string = re.sub(r"[^,\d]", "", str(angka))
            split = number_string.split(",")
            sisa = len(split[0]) % 3
            plafond = split[0][:sisa]
            ribuan = re.findall(r"\d{3}", split[0][sisa:])
            if ribuan:
                separator = "." if sisa else ""
                plafond += separator + ".".join(ribuan)
            if len(split) > 1:
                plafond = plafond + "," + split[1]
            if prefix is None:
                return plafond
            return f"{prefix}{plafond}" if plafond else ""

        self.assertEqual(py_format_rupiah("1000000"), "1.000.000")
        self.assertEqual(py_format_rupiah("50000000", "Rp. "), "Rp. 50.000.000")
        self.assertEqual(py_format_rupiah("1250000,50", "Rp. "), "Rp. 1.250.000,50")
        self.assertEqual(py_format_rupiah(""), "")

    def test_website_css_asset_paths(self):
        """Verify all url() references in website.css are local relative paths and files exist."""
        self.assertTrue(os.path.exists(self.css_path), f"{self.css_path} does not exist")
        with open(self.css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # website.css should not have any external http/https url links
        self.assertNotIn("http://", css_content)
        self.assertNotIn("https://", css_content)

        # Extract url(...) targets
        urls = re.findall(r"url\(['\"]?([^'\")]+)['\"]?\)", css_content)
        self.assertGreater(len(urls), 0, "No url() references found in website.css")

        css_dir = os.path.dirname(self.css_path)
        for u in urls:
            clean_u = u.replace("\\ ", " ")
            file_path = os.path.normpath(os.path.join(css_dir, clean_u))
            self.assertTrue(
                os.path.exists(file_path),
                f"Referenced asset does not exist: {clean_u} (resolved to {file_path})"
            )

if __name__ == "__main__":
    unittest.main()
