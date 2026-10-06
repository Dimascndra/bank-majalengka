#!/usr/bin/env python3
"""
tools/download_assets.py
Asset downloader and organizer for Bank Majalengka UI 1:1 clone.
Downloads CSS, JS, fonts, logos, and images from original site and vendor CDNs
so the website can run fully offline.
"""

import os
import shutil
import urllib.parse
import urllib.request
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ASSETS_TO_DOWNLOAD = [
    # --- CSS ---
    {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
        "dest": "assets/css/bootstrap.min.css"
    },
    {
        "url": "https://bankmajalengka.com/assets/css/website.css?v=1.0.2",
        "dest": "assets/css/website.css"
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.css",
        "dest": "assets/css/slick.css"
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick-theme.css",
        "dest": "assets/css/slick-theme.css"
    },
    {
        "url": "https://unpkg.com/aos@next/dist/aos.css",
        "dest": "assets/css/aos.css"
    },
    # Slick CSS auxiliary files (fonts & loader)
    {
        "url": "https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/ajax-loader.gif",
        "dest": "assets/css/ajax-loader.gif"
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/fonts/slick.eot",
        "dest": "assets/css/fonts/slick.eot"
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/fonts/slick.woff",
        "dest": "assets/css/fonts/slick.woff"
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/fonts/slick.ttf",
        "dest": "assets/css/fonts/slick.ttf"
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/fonts/slick.svg",
        "dest": "assets/css/fonts/slick.svg"
    },

    # --- JS ---
    {
        "url": "https://code.jquery.com/jquery-3.7.0.min.js",
        "dest": "assets/js/jquery-3.7.0.min.js"
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",
        "dest": "assets/js/bootstrap.bundle.min.js"
    },
    {
        "url": "https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.min.js",
        "dest": "assets/js/slick.min.js"
    },
    {
        "url": "https://unpkg.com/aos@next/dist/aos.js",
        "dest": "assets/js/aos.js"
    },
    {
        "url": "https://bankmajalengka.com/assets/fslightbox/fslightbox.js",
        "dest": "assets/js/fslightbox.js"
    },

    # --- FONTS (referenced in website.css) ---
    {
        "url": "https://bankmajalengka.com/assets/fonts/Bai%20Jamjuree%20Regular%20400.ttf",
        "dest": "assets/fonts/Bai Jamjuree Regular 400.ttf"
    },
    {
        "url": "https://bankmajalengka.com/assets/fonts/Bai%20Jamjuree%20SemiBold%20600.ttf",
        "dest": "assets/fonts/Bai Jamjuree SemiBold 600.ttf"
    },
    {
        "url": "https://bankmajalengka.com/assets/fonts/Bai%20Jamjuree%20Bold%20700.ttf",
        "dest": "assets/fonts/Bai Jamjuree Bold 700.ttf"
    },
    {
        "url": "https://bankmajalengka.com/assets/fonts/Poppins-Regular.otf",
        "dest": "assets/fonts/Poppins-Regular.otf"
    },
    {
        "url": "https://bankmajalengka.com/assets/fonts/Poppins-Bold.otf",
        "dest": "assets/fonts/Poppins-Bold.otf"
    },

    # --- CORE IMAGES & ICONS ---
    {
        "url": "https://bankmajalengka.com/favicon.ico",
        "dest": "assets/img/favicon.ico"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/Logo-Bank-Majalengka.png",
        "dest": "assets/img/Logo-Bank-Majalengka.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/Kantor-circle-min.png",
        "dest": "assets/img/Kantor-circle-min.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/Kantor-min.png",
        "dest": "assets/img/Kantor-min.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/Group-92@2x.png",
        "dest": "assets/img/Group-92@2x.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/Group-88@2x.png",
        "dest": "assets/img/Group-88@2x.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/Group-133@2x.png",
        "dest": "assets/img/Group-133@2x.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/chevron-top.png",
        "dest": "assets/img/chevron-top.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/chevron-left.png",
        "dest": "assets/img/chevron-left.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/chevron-right.png",
        "dest": "assets/img/chevron-right.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/whatsapp.png",
        "dest": "assets/img/whatsapp.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/phone-receiver-silhouette.png",
        "dest": "assets/img/phone-receiver-silhouette.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/email.png",
        "dest": "assets/img/email.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/maps-and-flags.png",
        "dest": "assets/img/maps-and-flags.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/facebook-app-symbol.png",
        "dest": "assets/img/facebook-app-symbol.png"
    },
    {
        "url": "https://bankmajalengka.com/assets/img/instagram.png",
        "dest": "assets/img/instagram.png"
    },
]

# Product images
PRODUCT_IMAGES = [
    "tahara.png",
    "IMG_2909.jpeg",
    "IMG_2911.jpeg",
    "WhatsApp_Image_2026-06-08_at_13.43.08-removebg-preview.png",
    "design_tabungan_tapaqur-removebg-preview.png",
    "tadabur.png",
    "IMG_2914.jpeg",
    "IMG_2922.jpeg",
    "IMG_2926.jpeg",
    "IMG_2928.jpeg",
    "ChatGPT Image 24 Jul 2026, 11.48.02.png",
    "ChatGPT Image 24 Jul 2026, 15.09.13.png",
    "ChatGPT Image 31 Jul 2026, 08.47.14.png",
    "ChatGPT Image 31 Jul 2026, 09.08.23.png",
    "ChatGPT Image 31 Jul 2026, 10.11.00.png",
    "KAN.png",
    "KAPESTA.png",
    "KSG.png",
    "multiguna.png",
    "non asn.png",
    "pensiunan.png",
    "perak.png",
]

# Post / News images
POST_IMAGES = [
    "post_1731047288_.jpeg",
    "post_1745206659_.jpeg",
    "post_1748954599_.jpeg",
    "post_1756347585_.png",
    "post_1761016082_.jpeg",
    "post_1761792240_.jpg",
    "post_1788166987_.png",
    "post_1789982976_.png",
]

for p in PRODUCT_IMAGES:
    encoded_p = urllib.parse.quote(p)
    ASSETS_TO_DOWNLOAD.append({
        "url": f"https://bankmajalengka.com/storage/products/{encoded_p}",
        "dest": f"assets/img/produk/{p}",
    })

for p in POST_IMAGES:
    encoded_p = urllib.parse.quote(p)
    ASSETS_TO_DOWNLOAD.append({
        "url": f"https://bankmajalengka.com/storage/post/{encoded_p}",
        "dest": f"assets/img/news/{p}",
    })


def download_file(url: str, dest_path: str, max_retries: int = 3) -> bool:
    full_dest = os.path.join(BASE_DIR, dest_path)
    os.makedirs(os.path.dirname(full_dest), exist_ok=True)

    if os.path.exists(full_dest) and os.path.getsize(full_dest) > 0:
        print(f"[EXISTS] {dest_path} ({os.path.getsize(full_dest):,} bytes)")
        return True

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)

    for attempt in range(1, max_retries + 1):
        try:
            print(f"[DOWNLOADING] {url} -> {dest_path} (Attempt {attempt})...")
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
                if len(content) == 0:
                    raise ValueError("Received 0 bytes")
                with open(full_dest, "wb") as f:
                    f.write(content)
            print(f"[SUCCESS] Saved {dest_path} ({len(content):,} bytes)")
            return True
        except Exception as e:
            print(f"[WARN] Attempt {attempt} failed for {url}: {e}")
            if attempt < max_retries:
                time.sleep(1.5)
            else:
                print(f"[ERROR] Failed to download {url} after {max_retries} attempts.")
                return False


def setup_storage_symlinks():
    """Create symlinks so /storage/products and /storage/post point to assets/img."""
    storage_dir = os.path.join(BASE_DIR, "storage")
    os.makedirs(storage_dir, exist_ok=True)

    products_link = os.path.join(storage_dir, "products")
    if not os.path.lexists(products_link):
        os.symlink("../assets/img/produk", products_link)

    post_link = os.path.join(storage_dir, "post")
    if not os.path.lexists(post_link):
        os.symlink("../assets/img/news", post_link)


def main():
    print(f"=== Starting Asset Download in {BASE_DIR} ===")
    total = len(ASSETS_TO_DOWNLOAD)
    success = 0
    failed = []

    for idx, item in enumerate(ASSETS_TO_DOWNLOAD, 1):
        print(f"[{idx}/{total}] Processing {item['dest']}...")
        if download_file(item["url"], item["dest"]):
            success += 1
        else:
            failed.append(item["url"])

    setup_storage_symlinks()

    # Also copy favicon to root if exists
    favicon_src = os.path.join(BASE_DIR, "assets/img/favicon.ico")
    if os.path.exists(favicon_src):
        shutil.copy2(favicon_src, os.path.join(BASE_DIR, "favicon.ico"))

    print("\n=== Download Summary ===")
    print(f"Total: {total}")
    print(f"Success: {success}")
    print(f"Failed: {len(failed)}")
    if failed:
        print("Failed URLs:")
        for f in failed:
            print(" -", f)
        exit(1)
    print("All assets successfully downloaded and verified!")


if __name__ == "__main__":
    main()
