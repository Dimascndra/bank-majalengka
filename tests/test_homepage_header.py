import os
import unittest
from html.parser import HTMLParser

class TestHomepageHeader(unittest.TestCase):
    def setUp(self):
        self.html_file = "index.html"

    def test_navbar_and_modal(self):
        """Verify navbar and anti-fraud modal elements are present in index.html."""
        self.assertTrue(os.path.exists(self.html_file), f"{self.html_file} does not exist")
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()
        self.assertTrue(
            'class="logo-bank"' in html or 'Logo-Bank-Majalengka.png' in html,
            "Bank logo not found in index.html"
        )
        self.assertIn('id="navbarNav"', html, "Navbar collapse ID 'navbarNav' not found")
        self.assertIn('id="antiFraudModal"', html, "Modal ID 'antiFraudModal' not found")
        self.assertIn('LARANGAN', html, "Modal header 'LARANGAN' not found")

    def test_header_topbar_structure(self):
        """Verify topbar, navbar styling and offline local asset links."""
        self.assertTrue(os.path.exists(self.html_file), f"{self.html_file} does not exist")
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()

        # Topbar & nav container
        self.assertIn('id="top"', html, "Top container id='top' not found")
        self.assertIn('bg-blue', html, "Navbar blue background class 'bg-blue' not found")
        self.assertIn('assets/img/Logo-Bank-Majalengka.png', html, "Local logo asset path not found")
        self.assertIn('assets/css/bootstrap.min.css', html, "Bootstrap CSS path not found")
        self.assertIn('assets/css/website.css', html, "Custom website CSS path not found")
        self.assertIn('assets/js/bootstrap.bundle.min.js', html, "Bootstrap JS bundle path not found")
        self.assertIn('assets/js/main.js', html, "Main JS path not found")

    def test_nav_links_and_dropdowns(self):
        """Verify navigation items and dropdown menus are present."""
        self.assertTrue(os.path.exists(self.html_file), f"{self.html_file} does not exist")
        with open(self.html_file, "r", encoding="utf-8") as f:
            html = f.read()

        nav_links = [
            "Beranda",
            "Tentang",
            "Simpanan",
            "Kredit",
            "Informasi",
            "Simulasi Kredit",
            "Laporan",
            "Kontak",
            "Pengaduan Nasabah",
        ]
        for link_text in nav_links:
            self.assertIn(link_text, html, f"Nav item '{link_text}' not found")

        dropdown_sublinks = [
            "Sejarah",
            "Visi & Misi",
            "Dewan Direktur",
            "Logo & Arti Logo",
            "Laporan Publikasi",
            "Laporan Tahunan",
            "Laporan Tata Kelola",
        ]
        for sublink in dropdown_sublinks:
            self.assertIn(sublink, html, f"Dropdown sublink '{sublink}' not found")


if __name__ == "__main__":
    unittest.main()
