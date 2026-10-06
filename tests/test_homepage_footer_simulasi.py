import os
import unittest


class TestHomepageFooterSimulasi(unittest.TestCase):
    def setUp(self):
        self.html_file = "index.html"

    def test_simulasi_and_footer(self):
        """Standard requirement test from specification brief."""
        self.assertTrue(os.path.exists(self.html_file), f"{self.html_file} does not exist")
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("carousel-informasi", html, "carousel-informasi not found")
        self.assertIn("SIMULASI KREDIT", html, "SIMULASI KREDIT section not found")
        self.assertIn("Kontak Kami", html, "Kontak Kami section not found")
        self.assertTrue(
            "Pemerintah Daerah Kabupaten Majalengka" in html or "Otoritas Jasa Keuangan" in html,
            "Official authority reference not found in footer"
        )
        self.assertIn("copyright", html, "copyright element/id not found")

    def test_news_carousel_details(self):
        """Verify news carousel has news cards, images, and text limits."""
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("news-card", html, "news-card class not found")
        self.assertIn("text-limit", html, "text-limit class not found")
        self.assertIn("assets/img/news/post_", html, "Local news images not found")

    def test_loan_calculator_elements(self):
        """Verify loan calculator form inputs and calculation outputs."""
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn('id="frmSimulasi"', html, "Form frmSimulasi not found")
        self.assertIn('id="plafond"', html, "Input plafond not found")
        self.assertIn('id="jangka_waktu"', html, "Input jangka_waktu not found")
        self.assertIn('id="btnSubmitSimulasi"', html, "Submit button not found")
        self.assertIn('id="hasil"', html, "Result container id=hasil not found")
        self.assertIn('id="angsuran-pokok"', html, "angsuran-pokok element not found")
        self.assertIn('id="angsuran-bunga"', html, "angsuran-bunga element not found")
        self.assertIn('id="total-angsuran"', html, "total-angsuran element not found")

    def test_footer_and_floating_buttons(self):
        """Verify footer contacts, official links, back to top, and copyright."""
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn('id="btn-back-to-top"', html, "Back to top button not found")
        self.assertIn('manajemenpusat@bprmajalengka.com', html, "Contact email not found")
        self.assertIn('+62811-1111-6526', html, "Contact phone not found")
        self.assertIn('id="copyright"', html, "Element id=copyright not found")
        self.assertIn('Lembaga Penjamin Simpanan', html, "LPS reference not found")


def test_simulasi_and_footer():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "carousel-informasi" in html
    assert "SIMULASI KREDIT" in html
    assert "Kontak Kami" in html
    assert "Pemerintah Daerah Kabupaten Majalengka" in html or "Otoritas Jasa Keuangan" in html
    assert "copyright" in html


if __name__ == "__main__":
    unittest.main()
