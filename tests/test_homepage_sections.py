import os
import unittest


class TestHomepageSections(unittest.TestCase):
    def setUp(self):
        self.html_file = "index.html"

    def test_services_and_banner(self):
        self.assertTrue(os.path.exists(self.html_file), f"{self.html_file} does not exist")
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("Mitra Kerja Membangun Ekonomi Rakyat", html)
        self.assertIn("carousel-layanan", html)
        self.assertIn("Tabungan", html)
        self.assertIn("Deposito", html)
        self.assertIn("Kredit", html)
        self.assertIn("MITRA USAHA ANDA", html)

    def test_hero_section_structure(self):
        """Verify hero headline, description, CTA button, and circle image."""
        self.assertTrue(os.path.exists(self.html_file), f"{self.html_file} does not exist")
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn("Mitra Kerja Membangun Ekonomi Rakyat", html)
        self.assertIn("Bank BPR Majalengka merupakan Bank Perkreditan Rakyat Milik Pemerintah Kabupaten Majalengka", html)
        self.assertIn("Tentang Kami", html)
        self.assertIn("assets/img/Kantor-circle-min.png", html)

    def test_carousel_layanan_products(self):
        """Verify Tabungan products inside .carousel-layanan with local assets."""
        self.assertTrue(os.path.exists(self.html_file), f"{self.html_file} does not exist")
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()

        products = [
            "TAHARA",
            "TIARA",
            "KOTAK MAS",
            "SIDASI",
            "TAPAQUR",
            "TADABUR",
            "T-ASMARA",
            "CIREMAIKU",
            "SIMPEL",
            "SIMARMAS GO",
        ]
        for prod in products:
            self.assertIn(prod, html, f"Product {prod} not found in Layanan carousel")

        self.assertIn("assets/img/produk/tahara.png", html)
        self.assertIn("assets/img/produk/IMG_2909.jpeg", html)

    def test_deposito_and_mitra_usaha_sections(self):
        """Verify Deposito section and Mitra Usaha banner section with local images."""
        self.assertTrue(os.path.exists(self.html_file), f"{self.html_file} does not exist")
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()

        # Deposito
        self.assertIn("Deposito", html)
        self.assertIn("assets/img/Group-92@2x.png", html)
        self.assertIn("Pastikan uang Anda diinvestasikan di tempat yang aman", html)

        # Kredit / Mitra Usaha Anda
        self.assertIn("Kredit", html)
        self.assertIn("MITRA USAHA ANDA", html)
        self.assertIn("assets/img/Group-88@2x.png", html)
        self.assertIn("Kredit Bank BPR Majalengka dengan bunga bersaing", html)


def test_services_and_banner():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "Mitra Kerja Membangun Ekonomi Rakyat" in html
    assert "carousel-layanan" in html
    assert "Tabungan" in html
    assert "Deposito" in html
    assert "Kredit" in html
    assert "MITRA USAHA ANDA" in html


if __name__ == "__main__":
    unittest.main()
