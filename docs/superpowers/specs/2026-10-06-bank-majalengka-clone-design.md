# Rancangan Desain Spesifikasi: Kloning UI Bank Majalengka (1:1)

- **Tanggal**: 2026-10-06
- **Status**: Disetujui
- **Target URL**: https://bankmajalengka.com/
- **Tujuan**: Membangun kloning UI website Bank Majalengka secara presisi 1:1 menggunakan teknologi yang sama, aset tersimpan lokal (offline-ready), dan struktur modular siap dikembangkan.

---

## 1. Lingkup Proyek (Scope)

1. **Halaman Utama (Beranda / `index.html`)**:
   - Replikasi 1:1 dari halaman utama `bankmajalengka.com`.
   - Meliputi Header/Logo, Navbar responsif (`bg-blue`), Modal Anti-Fraud otomatis, Hero Banner, Carousel Layanan (Tabungan, Deposito, Kredit), Banner Promo Mitra Usaha, Carousel Berita & Informasi, Kalkulator Simulasi Kredit interaktif, dan Footer lengkap.
2. **Struktur Halaman Turunan (`pages/`)**:
   - Penyiapan kerangka halaman modular yang terhubung dengan link navigasi:
     - `pages/tentang/sejarah.html`
     - `pages/tentang/visi-misi.html`
     - `pages/tentang/dewan-direktur.html`
     - `pages/tentang/arti-logo.html`
     - `pages/simpanan.html`
     - `pages/kredit.html`
     - `pages/simulasi-kredit.html`
     - `pages/informasi.html`
     - `pages/kontak.html`
3. **Kemandirian Aset (Self-Contained / Offline Support)**:
   - Seluruh pustaka CSS/JS, gambar, logo, ikon, dan styling disimpan di folder `assets/` tanpa ketergantungan wajib ke server luar.

---

## 2. Arsitektur Teknologi & Dependensi

Sesuai dengan analisis teknologi situs asli Bank Majalengka:
- **Markup**: HTML5 semantik.
- **Styling**:
  - Bootstrap v5.3.0
  - Custom Stylesheet Bank Majalengka (`assets/css/website.css`)
  - Slick Carousel Stylesheet (`assets/css/slick.css`, `assets/css/slick-theme.css`)
  - AOS (Animate on Scroll) Stylesheet (`assets/css/aos.css`)
- **JavaScript & Interaktivitas**:
  - jQuery v3.7.0
  - Bootstrap v5.3.0 Bundle (termasuk Popper.js)
  - Slick Carousel v1.8.1
  - AOS v2.3.4
  - FSLightbox
  - `assets/js/main.js` (Logika spesifik: format mata uang Rupiah, kalkulator simulasi kredit, popup modal otomatis, text truncation 15 kata, dan inisialisasi carousel).

---

## 3. Struktur Direktori Proyek

```text
bank-majalengka/
├── index.html                           # Beranda 1:1
├── pages/                               # Kerangka halaman modular
│   ├── tentang/
│   │   ├── sejarah.html
│   │   ├── visi-misi.html
│   │   ├── dewan-direktur.html
│   │   └── arti-logo.html
│   ├── simpanan.html
│   ├── kredit.html
│   ├── simulasi-kredit.html
│   ├── informasi.html
│   └── kontak.html
├── assets/
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   ├── website.css
│   │   ├── slick.css
│   │   ├── slick-theme.css
│   │   └── aos.css
│   ├── js/
│   │   ├── jquery-3.7.0.min.js
│   │   ├── bootstrap.bundle.min.js
│   │   ├── slick.min.js
│   │   ├── aos.js
│   │   ├── fslightbox.js
│   │   └── main.js
│   └── img/
│       ├── Logo-Bank-Majalengka.png
│       ├── banners/
│       ├── produk/
│       ├── news/
│       └── icons/
├── tools/
│   └── download_assets.py               # Script downloader & parser aset asli
└── docs/
    └── superpowers/specs/
        └── 2026-10-06-bank-majalengka-clone-design.md
```

---

## 4. Rincian Komponen UI Beranda (`index.html`)

1. **Top Bar**:
   - Kontainer putih dengan logo resmi `Logo-Bank-Majalengka.png`.
2. **Navigasi Utama (`.bg-blue`)**:
   - Header biru dengan collapsible hamburger menu untuk layar mobile/tablet.
   - Menu item: Beranda (active), Tentang (dropdown), Simpanan, Kredit, Informasi, Simulasi Kredit, Laporan (dropdown), Kontak, Pengaduan Nasabah.
3. **Modal Anti-Fraud (`#antiFraudModal`)**:
   - Dialog modal terpusat (centered) yang otomatis muncul via `bootstrap.Modal(el).show()`.
   - Mengingatkan nasabah agar tidak melayani pungutan liar atau pihak mencurigakan.
4. **Hero Banner & Slogan**:
   - Banner utama dengan tagline *"Mitra Kerja Membangun Ekonomi Rakyat"*.
5. **Section Layanan (`.carousel-layanan`)**:
   - Tab / slider produk perbankan: Tabungan, Deposito, Kredit.
   - Konfigurasi Slick slider 4 kolom (desktop) dan 2 kolom (mobile/tablet).
6. **Banner Mitra Usaha**:
   - Tagline visual *"MITRA USAHA ANDA"*.
7. **Section Berita & Informasi (`.carousel-informasi`)**:
   - Slider berita terkini dengan card visual.
   - Pembatasan teks ringkasan (15 kata) dengan script otomatis.
8. **Simulasi Kredit Interaktif**:
   - Input Plafond Pinjaman dengan pemformatan otomatis "Rp. xxx.xxx.xxx".
   - Pilihan Jangka Waktu (bulan/tahun) dan suku bunga.
   - Kalkulasi otomatis rincian angsuran per bulan.
9. **Footer Area**:
   - Informasi alamat kantor pusat, telepon, email, jam pelayanan.
   - Tautan eksternal resmi (OJK, LPS).
   - Ikon media sosial dan hak cipta.

---

## 5. Rencana Pengujian & Verifikasi

1. **Aset Offline**: Memastikan semua link gambar, file CSS, dan JS tidak ada yang broken (status 404) ketika dijalankan secara lokal.
2. **Interaktivitas**:
   - Verifikasi popup Anti-Fraud tampil dan dapat ditutup.
   - Verifikasi kedua carousel (Layanan & Informasi) dapat digeser/navigasi.
   - Verifikasi form simulasi kredit menghitung angka dengan benar dan format Rupiah berfungsi realtime.
3. **Responsivitas**:
   - Tampilan desktop (lebar > 1200px)
   - Tampilan tablet (768px - 1024px)
   - Tampilan mobile (< 768px) dengan fungsi navbar toggle bekerja baik.
