import os
import unittest

class TestAssetsExist(unittest.TestCase):
    def test_essential_assets_exist(self):
        required_files = [
            "assets/css/bootstrap.min.css",
            "assets/css/website.css",
            "assets/css/slick.css",
            "assets/css/slick-theme.css",
            "assets/css/aos.css",
            "assets/js/jquery-3.7.0.min.js",
            "assets/js/bootstrap.bundle.min.js",
            "assets/js/slick.min.js",
            "assets/js/aos.js",
            "assets/js/fslightbox.js",
            "assets/img/Logo-Bank-Majalengka.png",
        ]
        for rel_path in required_files:
            assert os.path.exists(rel_path), f"Missing asset: {rel_path}"
            assert os.path.getsize(rel_path) > 0, f"Asset is empty: {rel_path}"

    def test_additional_offline_assets_exist(self):
        additional_files = [
            # Fonts
            "assets/fonts/Bai Jamjuree Regular 400.ttf",
            "assets/fonts/Bai Jamjuree SemiBold 600.ttf",
            "assets/fonts/Bai Jamjuree Bold 700.ttf",
            "assets/fonts/Poppins-Regular.otf",
            "assets/fonts/Poppins-Bold.otf",
            # Slick assets
            "assets/css/ajax-loader.gif",
            "assets/css/fonts/slick.ttf",
            "assets/css/fonts/slick.woff",
            # UI Icons and Images
            "assets/img/Kantor-circle-min.png",
            "assets/img/Kantor-min.png",
            "assets/img/Group-92@2x.png",
            "assets/img/Group-88@2x.png",
            "assets/img/Group-133@2x.png",
            "assets/img/whatsapp.png",
            "assets/img/phone-receiver-silhouette.png",
            "assets/img/email.png",
            "assets/img/maps-and-flags.png",
            # Sample product and news images
            "assets/img/produk/tahara.png",
            "assets/img/news/post_1731047288_.jpeg",
        ]
        for rel_path in additional_files:
            assert os.path.exists(rel_path), f"Missing additional asset: {rel_path}"
            assert os.path.getsize(rel_path) > 0, f"Asset is empty: {rel_path}"

if __name__ == "__main__":
    unittest.main()
