# Bank Majalengka UI 1:1 Clone Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Membangun klon antarmuka (UI) 1:1 dari situs resmi Bank Majalengka (https://bankmajalengka.com/) menggunakan teknologi yang sama (HTML5, Bootstrap 5.3, custom CSS, jQuery, Slick Carousel, AOS, FSLightbox) dengan aset tersimpan lokal (offline-capable) dan struktur modular siap dikembangkan.

**Architecture:** Menggunakan arsitektur multi-halaman statis modular di mana `index.html` berperan sebagai halaman utama beranda 1:1, didukung aset lokal (`assets/css/`, `assets/js/`, `assets/img/`), skrip kalkulator simulasi kredit dan popup interaktif di `assets/js/main.js`, serta kerangka halaman sekunder di folder `pages/`.

**Tech Stack:** HTML5, CSS3, Bootstrap 5.3.0, jQuery 3.7.0, Slick Carousel 1.8.1, AOS 2.3.4, FSLightbox, Python 3 (untuk tooling asset fetcher & testing server).

**Spec:** `docs/superpowers/specs/2026-10-06-bank-majalengka-clone-design.md`

## Global Constraints

- Halaman Beranda (`index.html`) harus identik secara visual dan fungsional (1:1) dengan `https://bankmajalengka.com/`.
- Semua stylesheet (`bootstrap.min.css`, `website.css`, `slick.css`, `slick-theme.css`, `aos.css`) dan skrip (`bootstrap.bundle.min.js`, `jquery-3.7.0.min.js`, `slick.min.js`, `aos.js`, `fslightbox.js`) harus tersedia secara lokal di `assets/`.
- Gambar dan logo Bank Majalengka disimpan di `assets/img/`.
- Form kalkulator simulasi kredit harus bekerja real-time menghitung angsuran pokok & bunga dengan format mata uang Rupiah.
- Modal anti-fraud otomatis muncul saat halaman dimuat.

## Review Focus

1. **Broken image/asset links (404)**: Semua gambar, icon font, dan script harus mengarah ke path lokal yang valid tanpa bergantung pada koneksi internet.
2. **Kalkulasi simulasi kredit tanpa input valid**: Kalkulator harus menangani input kosong atau karakter non-numerik tanpa menimbulkan crash atau error NaN.
3. **Responsivitas Navbar mobile**: Hamburger menu pada resolusi mobile (< 768px) harus dapat membuka dan menutup dropdown tanpa gangguan layout.
4. **Perilaku Slick Carousel**: Slider produk layanan dan informasi berita harus berjalan mulus dengan breakpoint responsif sesuai situs aslinya.
5. **Modal Anti-Fraud**: Modal harus memiliki backdrop yang tepat, z-index sesuai, dan tombol tutup yang menutup dialog secara mulus.

---

### Task 1: Setup Asset Fetcher & Unduh Semua Aset Lokal

**Files:**
- Create: `tools/download_assets.py`
- Test: `tests/test_assets_exist.py`

**Interfaces:**
- Consumes: URL `https://bankmajalengka.com/` dan file-file aset eksternal.
- Produces: Seluruh berkas CSS, JS, dan Gambar di folder `assets/css/`, `assets/js/`, dan `assets/img/`.

- [ ] **Step 1: Write test for local assets existence**

```python
# tests/test_assets_exist.py
import os

def test_essential_assets_exist():
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_assets_exist.py`
Expected: FAIL (No files exist yet)

- [ ] **Step 3: Implement asset fetcher script `tools/download_assets.py` and run it**

Script Python mengunduh stylesheet asli, pustaka vendor (jQuery, Bootstrap, Slick, AOS), file gambar dan logo langsung dari server asli ke direktori `assets/`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_assets_exist.py`
Expected: PASS

- [ ] **Step 5: Commit assets**

```bash
git add assets/ tools/download_assets.py tests/test_assets_exist.py
git commit -m "feat(assets): download and organize local assets for offline support"
```

---

### Task 2: Implementasi Custom CSS & Inisialisasi JS Dasar

**Files:**
- Create: `assets/js/main.js`
- Modify: `assets/css/website.css` (jika ada perbaikan path URL font/gambar ke path lokal relatif)
- Test: `tests/test_js_logic.py`

**Interfaces:**
- Consumes: Input nilai angka mentah / string untuk format Rupiah.
- Produces: `formatRupiah(angka, prefix)`, inisialisasi Slick Carousel, AOS, dan Modal Anti-Fraud.

- [ ] **Step 1: Write unit test for JavaScript logic in Python**

```python
# tests/test_js_logic.py
import os
import re

def test_main_js_functions():
    with open("assets/js/main.js", "r") as f:
        content = f.read()
    assert "formatRupiah" in content
    assert "carousel-layanan" in content
    assert "carousel-informasi" in content
    assert "antiFraudModal" in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_js_logic.py`
Expected: FAIL (File assets/js/main.js not created yet)

- [ ] **Step 3: Implement `assets/js/main.js`**

Implementasikan:
- `formatRupiah(angka, prefix)`
- Inisialisasi Slick Carousel `.carousel-layanan` & `.carousel-informasi`
- Inisialisasi modal `#antiFraudModal` saat DOMContentLoaded
- Script pemangkas kata deskripsi kartu berita maksimal 15 kata
- Inisialisasi `AOS.init()` dan `AOS.refresh()`

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_js_logic.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add assets/js/main.js tests/test_js_logic.py
git commit -m "feat(js): implement main interactive scripts and helper functions"
```

---

### Task 3: Implementasi Struktur Header, Topbar, Navbar, & Modal Anti-Fraud

**Files:**
- Create: `index.html` (bagian Topbar, Navbar, dan Modal Anti-Fraud)
- Test: `tests/test_homepage_header.py`

**Interfaces:**
- Consumes: Aset `Logo-Bank-Majalengka.png`, `bootstrap.min.css`, `website.css`.
- Produces: Struktur navigasi responsif dan dialog modal popup anti-fraud.

- [ ] **Step 1: Write test for header and modal elements**

```python
# tests/test_homepage_header.py
from html.parser import HTMLParser

def test_navbar_and_modal():
    with open("index.html", "r") as f:
        html = f.read()
    assert 'class="logo-bank"' in html or 'Logo-Bank-Majalengka.png' in html
    assert 'id="navbarNav"' in html
    assert 'id="antiFraudModal"' in html
    assert 'LARANGAN' in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_homepage_header.py`
Expected: FAIL (index.html doesn't exist yet)

- [ ] **Step 3: Implement topbar, navbar, and anti-fraud modal in `index.html`**

Replikasi markup HTML asli dari `https://bankmajalengka.com/` untuk elemen `#top`, navbar `.bg-blue`, dan `#antiFraudModal`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_homepage_header.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_homepage_header.py
git commit -m "feat(ui): implement header, navbar, and anti-fraud modal in index.html"
```

---

### Task 4: Implementasi Hero Section, Carousel Layanan, & Banner Mitra Usaha

**Files:**
- Modify: `index.html`
- Test: `tests/test_homepage_sections.py`

**Interfaces:**
- Consumes: Kartu layanan (Tabungan, Deposito, Kredit) dan banner.
- Produces: Section Hero, Section Layanan dengan `.carousel-layanan`, dan Section Slogan *"MITRA USAHA ANDA"*.

- [ ] **Step 1: Write test for services and banner sections**

```python
# tests/test_homepage_sections.py
def test_services_and_banner():
    with open("index.html", "r") as f:
        html = f.read()
    assert "Mitra Kerja Membangun Ekonomi Rakyat" in html
    assert "carousel-layanan" in html
    assert "Tabungan" in html
    assert "Deposito" in html
    assert "Kredit" in html
    assert "MITRA USAHA ANDA" in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_homepage_sections.py`
Expected: FAIL

- [ ] **Step 3: Implement Hero, Layanan Carousel, and Mitra Usaha section**

Tambahkan markup lengkap untuk hero tagline, tabungan/deposito/kredit cards dengan Slick slider markup, dan visual banner mitra usaha.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_homepage_sections.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html tests/test_homepage_sections.py
git commit -m "feat(ui): add hero section, service carousels, and promotional banner"
```

---

### Task 5: Implementasi Berita & Informasi, Kalkulator Simulasi Kredit, & Footer

**Files:**
- Modify: `index.html`
- Modify: `assets/js/main.js` (perhitungan kalkulator kredit simulasi)
- Test: `tests/test_homepage_footer_simulasi.py`

**Interfaces:**
- Consumes: Input plafond, tenor, bunga di form simulasi.
- Produces: Kartu informasi `.carousel-informasi`, kalkulasi simulasi kredit, dan footer lengkap.

- [ ] **Step 1: Write test for news carousel, loan calculator, and footer**

```python
# tests/test_homepage_footer_simulasi.py
def test_simulasi_and_footer():
    with open("index.html", "r") as f:
        html = f.read()
    assert "carousel-informasi" in html
    assert "SIMULASI KREDIT" in html
    assert "Kontak Kami" in html
    assert "Pemerintah Daerah Kabupaten Majalengka" in html or "Otoritas Jasa Keuangan" in html
    assert "copyright" in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_homepage_footer_simulasi.py`
Expected: FAIL

- [ ] **Step 3: Implement News carousel, interactive credit calculator, and footer in `index.html`**

Tambahkan markup berita terkini, form kalkulator kredit lengkap beserta logika perhitungan simulasi, dan footer multi-kolom identik dengan aslinya.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_homepage_footer_simulasi.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add index.html assets/js/main.js tests/test_homepage_footer_simulasi.py
git commit -m "feat(ui): add news carousel, interactive loan simulation, and footer"
```

---

### Task 6: Penyiapan Kerangka Halaman Sekunder (`pages/`)

**Files:**
- Create: `pages/tentang/sejarah.html`
- Create: `pages/tentang/visi-misi.html`
- Create: `pages/tentang/dewan-direktur.html`
- Create: `pages/tentang/arti-logo.html`
- Create: `pages/simpanan.html`
- Create: `pages/kredit.html`
- Create: `pages/simulasi-kredit.html`
- Create: `pages/informasi.html`
- Create: `pages/kontak.html`
- Test: `tests/test_secondary_pages.py`

**Interfaces:**
- Consumes: Header, navbar, dan footer terstandar.
- Produces: Kerangka halaman modular lengkap yang terhubung dengan link navigasi di `index.html`.

- [ ] **Step 1: Write test for secondary pages existence and structure**

```python
# tests/test_secondary_pages.py
import os

def test_secondary_pages_structure():
    pages = [
        "pages/tentang/sejarah.html",
        "pages/tentang/visi-misi.html",
        "pages/tentang/dewan-direktur.html",
        "pages/tentang/arti-logo.html",
        "pages/simpanan.html",
        "pages/kredit.html",
        "pages/simulasi-kredit.html",
        "pages/informasi.html",
        "pages/kontak.html"
    ]
    for p in pages:
        assert os.path.exists(p), f"Missing page: {p}"
        with open(p, "r") as f:
            c = f.read()
        assert "navbar" in c
        assert "Bank Majalengka" in c
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests/test_secondary_pages.py`
Expected: FAIL

- [ ] **Step 3: Create secondary pages with matching layout header & footer**

Buat berkas-berkas halaman dengan template header, navbar aktif, konten placeholder yang relevan, dan footer yang konsisten.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests/test_secondary_pages.py`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pages/ tests/test_secondary_pages.py
git commit -m "feat(pages): scaffold secondary pages with consistent layout"
```

---

### Task 7: Verifikasi Menyeluruh 1:1 & Server Preview

**Files:**
- Create: `tests/verify_all.py`
- Test: `tests/verify_all.py`

**Interfaces:**
- Consumes: Seluruh berkas proyek di root.
- Produces: Laporan verifikasi bebas broken link aset lokal dan pengecekan integritas HTML5.

- [ ] **Step 1: Write end-to-end verification script**

Script mengecek:
- Tidak ada URL gambar/CSS/JS yang merujuk ke server eksternal tanpa fallback lokal.
- Semua file lokal yang dirujuk di `index.html` dan `pages/` benar-benar ada di disk.
- HTML valid tanpa tag unclosed kritis.

- [ ] **Step 2: Run verification script**

Run: `python3 tests/verify_all.py`
Expected: ALL CHECKS PASS (0 broken links, 100% offline ready).

- [ ] **Step 3: Final commit and summary documentation**

```bash
git add .
git commit -m "chore: complete 1:1 UI clone verification and documentation"
```
