/**
 * assets/js/main.js
 * Bank Majalengka UI Interactive Scripts & Core Helpers
 * 
 * Features:
 * - formatRupiah: Currency formatting for Indonesian Rupiah
 * - angka: Keypress filter allowing numeric input only
 * - Slick Carousel initialization (.carousel-layanan & .carousel-informasi)
 * - Anti-Fraud Modal popup initialization (#antiFraudModal)
 * - News card description truncation (max 15 words)
 * - AOS (Animate on Scroll) initialization & refresh
 * - Back-to-top button handler (#btn-back-to-top)
 * - Dynamic copyright year update (#copyright)
 * - Plafond real-time input formatting (#plafond)
 */

(function (window, document, $) {
    'use strict';

    /**
     * Format a string or number into Indonesian Rupiah format.
     * @param {string|number} angka - Raw numeric value or string
     * @param {string|boolean} [prefix] - Optional prefix (e.g. "Rp. " or boolean true)
     * @returns {string} Formatted rupiah string
     */
    function formatRupiah(angka, prefix) {
        if (angka === undefined || angka === null) {
            return '';
        }

        var number_string = angka.toString().replace(/[^,\d]/g, '');
        var split = number_string.split(',');
        var sisa = split[0].length % 3;
        var plafond = split[0].substr(0, sisa);
        var ribuan = split[0].substr(sisa).match(/\d{3}/gi);

        if (ribuan) {
            var separator = sisa ? '.' : '';
            plafond += separator + ribuan.join('.');
        }

        plafond = split[1] !== undefined ? plafond + ',' + split[1] : plafond;

        if (prefix === undefined) {
            return plafond;
        }

        var prefixStr = (typeof prefix === 'string') ? prefix : (prefix ? 'Rp. ' : '');
        return plafond ? prefixStr + plafond : '';
    }

    /**
     * Filter input event to only allow numeric key codes.
     * @param {KeyboardEvent} evt
     * @returns {boolean}
     */
    function angka(evt) {
        var charCode = evt.which ? evt.which : (evt.keyCode || (window.event ? window.event.keyCode : 0));
        if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
        return true;
    }

    /**
     * Truncate news card descriptions to a maximum number of words.
     * @param {number} maxWords - Maximum words to retain (default: 15)
     */
    function truncateNewsDescriptions(maxWords) {
        maxWords = maxWords || 15;
        var newsItems = document.getElementsByClassName('news-card');

        Array.from(newsItems).forEach(function (item) {
            var description = item.querySelector('.text-limit');
            if (description && description.textContent) {
                var text = description.textContent.trim();
                var words = text.split(/\s+/);

                if (words.length > maxWords) {
                    var truncatedText = words.slice(0, maxWords).join(' ');
                    description.textContent = truncatedText + '...';
                }
            }
        });
    }

    /**
     * Initialize Slick Carousels for layanan and informasi sections.
     */
    function initCarousels() {
        if (!$ || !$.fn || !$.fn.slick) {
            return;
        }

        if ($('.carousel-layanan').length > 0 && !$('.carousel-layanan').hasClass('slick-initialized')) {
            $('.carousel-layanan').slick({
                infinite: true,
                slidesToShow: 4,
                slidesToScroll: 1,
                arrows: true,
                dots: false,
                responsive: [
                    {
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1
                        }
                    },
                    {
                        breakpoint: 992,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1
                        }
                    }
                ]
            });
        }

        if ($('.carousel-informasi').length > 0 && !$('.carousel-informasi').hasClass('slick-initialized')) {
            $('.carousel-informasi').slick({
                infinite: true,
                slidesToShow: 4,
                slidesToScroll: 1,
                arrows: false,
                dots: true,
                responsive: [
                    {
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1
                        }
                    },
                    {
                        breakpoint: 992,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 1
                        }
                    }
                ]
            });
        }
    }

    /**
     * Show Anti-Fraud Modal on initial page load if element exists.
     */
    function initAntiFraudModal() {
        var modalEl = document.getElementById('antiFraudModal');
        if (modalEl && typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            try {
                var modalInstance = bootstrap.Modal.getOrCreateInstance 
                    ? bootstrap.Modal.getOrCreateInstance(modalEl) 
                    : new bootstrap.Modal(modalEl);
                modalInstance.show();
            } catch (err) {
                console.warn('Could not initialize antiFraudModal:', err);
            }
        }
    }

    /**
     * Initialize Back-to-Top smooth scrolling button.
     */
    function initBackToTop() {
        var mybutton = document.getElementById('btn-back-to-top');
        if (mybutton) {
            mybutton.addEventListener('click', function (e) {
                if (e && e.preventDefault) {
                    e.preventDefault();
                }
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    }

    /**
     * Automatically update footer copyright year to current year.
     */
    function initCopyrightYear() {
        var copyrightEl = document.getElementById('copyright');
        if (copyrightEl) {
            copyrightEl.textContent = new Date().getFullYear();
        }
    }

    /**
     * Calculate loan installments for flat or decreasing interest.
     * @param {number} plafond - Loan amount in Rupiah
     * @param {number} tenorBulan - Loan duration in months
     * @param {number|string} tipe - 1 for Flat, 2 for Menurun (effective/decreasing)
     * @param {number} [annualRate] - Annual interest rate (default: 12% / 0.12)
     * @returns {Object} { pokok, bunga, total }
     */
    function calculateLoanSimulation(plafond, tenorBulan, tipe, annualRate) {
        if (!plafond || !tenorBulan || tenorBulan <= 0 || plafond <= 0) {
            return { pokok: 0, bunga: 0, total: 0 };
        }

        annualRate = annualRate !== undefined ? annualRate : 0.12; // 12% per year
        var monthlyRate = annualRate / 12;
        var pokokPerBulan = Math.round(plafond / tenorBulan);
        var bungaPerBulan = 0;

        if (String(tipe) === '1') {
            // Bunga Flat: bunga tetap per bulan dihitung dari total plafond awal
            bungaPerBulan = Math.round(plafond * monthlyRate);
        } else {
            // Bunga Menurun: bulan pertama dihitung dari sisa plafond penuh
            bungaPerBulan = Math.round(plafond * monthlyRate);
        }

        var totalPerBulan = pokokPerBulan + bungaPerBulan;

        return {
            pokok: pokokPerBulan,
            bunga: bungaPerBulan,
            total: totalPerBulan
        };
    }

    /**
     * Bind dynamic currency formatting to #plafond loan input.
     */
    function initPlafondFormatting() {
        if ($) {
            $('#plafond').on('keyup', function () {
                var val = $(this).val();
                $(this).val(formatRupiah(val));
            });
        } else {
            var plafondInput = document.getElementById('plafond');
            if (plafondInput) {
                plafondInput.addEventListener('keyup', function () {
                    this.value = formatRupiah(this.value);
                });
            }
        }
    }

    /**
     * Initialize interactive loan simulation form submission (#frmSimulasi).
     */
    function initLoanSimulation() {
        var form = document.getElementById('frmSimulasi');
        if (!form) return;

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            var plafondEl = document.getElementById('plafond');
            var tenorEl = document.getElementById('jangka_waktu');
            var tipeEls = document.getElementsByName('tipe');

            var rawPlafond = plafondEl ? plafondEl.value.replace(/[^0-9]/g, '') : '0';
            var plafond = parseFloat(rawPlafond) || 0;
            var tenor = parseInt(tenorEl ? tenorEl.value : '0', 10) || 0;

            var tipe = '2'; // Default Menurun
            for (var i = 0; i < tipeEls.length; i++) {
                if (tipeEls[i].checked) {
                    tipe = tipeEls[i].value;
                    break;
                }
            }

            if (plafond <= 0 || tenor <= 0) {
                return;
            }

            var btnSubmit = document.getElementById('btnSubmitSimulasi');
            var originalBtnText = btnSubmit ? btnSubmit.innerHTML : 'Hitung Simulasi';

            if (btnSubmit) {
                btnSubmit.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Menghitung...';
                btnSubmit.disabled = true;
            }

            setTimeout(function () {
                var result = calculateLoanSimulation(plafond, tenor, tipe);

                var fmtPokok = formatRupiah(result.pokok, 'Rp. ');
                var fmtBunga = formatRupiah(result.bunga, 'Rp. ');
                var fmtTotal = formatRupiah(result.total, 'Rp. ');

                var tipeNama = String(tipe) === '1' ? 'Flat' : 'Menurun (Bulan ke-1)';

                var textHasilEl = document.getElementById('text-hasil');
                var pokokEl = document.getElementById('angsuran-pokok');
                var bungaEl = document.getElementById('angsuran-bunga');
                var totalEl = document.getElementById('total-angsuran');

                if (textHasilEl) textHasilEl.textContent = 'Hasil Simulasi Angsuran Bunga (' + tipeNama + ') :';
                if (pokokEl) pokokEl.textContent = 'Angsuran Pokok : ' + fmtPokok;
                if (bungaEl) bungaEl.textContent = 'Angsuran Bunga : ' + fmtBunga;
                if (totalEl) totalEl.textContent = 'Total Angsuran : ' + fmtTotal;

                if (btnSubmit) {
                    btnSubmit.innerHTML = originalBtnText;
                    btnSubmit.disabled = false;
                }
            }, 200);
        });
    }

    /**
     * Initialize AOS animation library.
     */
    function initAOS() {
        if (typeof AOS !== 'undefined') {
            AOS.init();
        }
    }

    /**
     * Refresh AOS animation library on window load.
     */
    function refreshAOS() {
        if (typeof AOS !== 'undefined') {
            AOS.refresh();
        }
    }

    // Expose helpers globally for inline HTML attributes (e.g. onkeypress="return angka(event)")
    window.formatRupiah = formatRupiah;
    window.angka = angka;
    window.truncateNewsDescriptions = truncateNewsDescriptions;
    window.initCarousels = initCarousels;
    window.initAntiFraudModal = initAntiFraudModal;
    window.calculateLoanSimulation = calculateLoanSimulation;
    window.initLoanSimulation = initLoanSimulation;

    // DOM Ready initialization
    function onReady() {
        initAntiFraudModal();
        initCarousels();
        truncateNewsDescriptions(15);
        initBackToTop();
        initCopyrightYear();
        initPlafondFormatting();
        initLoanSimulation();
        initAOS();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', onReady);
    } else {
        onReady();
    }

    // Window load handler
    window.addEventListener('load', function () {
        refreshAOS();
    });

})(typeof window !== 'undefined' ? window : this, typeof document !== 'undefined' ? document : null, typeof jQuery !== 'undefined' ? jQuery : null);
