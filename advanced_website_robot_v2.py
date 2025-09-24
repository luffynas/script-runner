# -*- coding: utf-8 -*-
import random
import time
import logging
import sys
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


def setup_logging():
    """
    Setup logging mengikuti pattern cookie_robot.py
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s'))
    logging.getLogger(name='advanced_website_robot').addHandler(console_handler)


class Configuration:
    """Advanced configuration management"""
    def __init__(self):
        self.config = {
            'timing': {
                'min_delay': random.uniform(0.3, 4.0),  # Variasi yang lebih extreme
                'max_delay': random.uniform(3.0, 30.0),  # Range yang lebih extreme
                'page_load_timeout': 30,
                'element_wait_timeout': 10,
                'long_pause_chance': random.uniform(0.02, 0.35),  # Variasi chance lebih extreme
                'long_pause_min': random.uniform(2.0, 10.0),  # Variasi minimum pause lebih extreme
                'long_pause_max': random.uniform(15.0, 60.0),  # Variasi maximum pause lebih extreme
                'human_typing_delay_range': (random.uniform(0.05, 0.5), random.uniform(0.3, 2.0)),  # Variasi typing delays lebih extreme
                'human_scroll_delay_range': (random.uniform(0.5, 5.0), random.uniform(3.0, 20.0)),  # Variasi scroll delays lebih extreme
                'human_click_delay_range': (random.uniform(0.2, 3.0), random.uniform(1.5, 15.0)),  # Variasi click delays lebih extreme
                'random_timing_variation': True,  # Enable random timing variation
                'natural_hesitation': True,  # Enable natural hesitation
                'reading_pause_chance': random.uniform(0.05, 0.50),  # Variasi reading pause lebih extreme
                'natural_timing_factor': random.uniform(0.5, 2.0),  # Natural timing factor lebih extreme
                'hesitation_variation': random.uniform(0.4, 2.0),  # Hesitation variation lebih extreme
                'micro_pause_chance': random.uniform(0.1, 0.4),  # 10-40% chance micro pause
                'macro_pause_chance': random.uniform(0.02, 0.15),  # 2-15% chance macro pause
                'distraction_pause_chance': random.uniform(0.05, 0.25),  # 5-25% chance distraction pause
                'natural_rhythm_factor': random.uniform(0.6, 1.8),  # Natural rhythm factor
                'timing_chaos_factor': random.uniform(0.1, 0.3)  # 10-30% timing chaos
            },
            'stealth': {
                'enable_stealth_scripts': True,
                'advanced_evasion': True,
                'behavioral_randomization': True
            },
            'behavior': {
                'mouse_movement': True,
                'random_delays': True,
                'behavioral_profiles': ['exploratory', 'focused', 'wandering', 'hesitant', 'reading', 'distracted']
            },
            'reading': {
                'min_reading_time': random.uniform(3.0, 5.0),  # 3-5 minutes minimum
                'max_reading_time': random.uniform(8.0, 12.0),  # 8-12 minutes maximum
                'default_reading_time': random.uniform(4.0, 6.0),  # 4-6 minutes default
                'content_type_detection': True,  # Enable content type detection
                'language_detection': True,  # Enable language detection
                'reading_speed_technical': (100, 150),  # WPM for technical content
                'reading_speed_news': (150, 200),  # WPM for news content
                'reading_speed_general': (150, 250),  # WPM for general content
                'indonesian_speed_multiplier': 0.8,  # 20% slower for Indonesian
                'english_speed_multiplier': 1.0,  # Normal speed for English
                'mood_change_chance': 0.03,  # 3% chance to change reading mood
                'micro_movement_chance': 0.3,  # 30% chance for micro-movements
                're_read_chance': 0.15,  # 15% chance to re-read
                'ad_check_interval_min': 120,  # 2 minutes minimum
                'ad_check_interval_max': 300,  # 5 minutes maximum
                'natural_reading_pauses': True,  # Enable natural reading pauses
                'comprehension_time': True,  # Enable comprehension time
                'mood_transitions': True,  # Enable mood transition behavior
                'pause_timing': {
                    'focused_pause_min': 1.0,  # 1-3 seconds for focused reading
                    'focused_pause_max': 3.0,
                    'distracted_pause_min': 2.0,  # 2-6 seconds for distracted reading
                    'distracted_pause_max': 6.0,
                    'careful_pause_min': 2.5,  # 2.5-5 seconds for careful reading
                    'careful_pause_max': 5.0,
                    'quick_pause_min': 0.5,  # 0.5-2 seconds for quick reading
                    'quick_pause_max': 2.0,
                    'distraction_chance': 0.15,  # 15% chance for distraction pause
                    'distraction_pause_min': 3.0,  # 3-8 seconds for distraction
                    'distraction_pause_max': 8.0,
                    'comprehension_chance': 0.20,  # 20% chance for comprehension pause
                    'comprehension_pause_min': 2.0,  # 2-6 seconds for comprehension
                    'comprehension_pause_max': 6.0,
                    're_read_pause_min': 0.5,  # 0.5-2 seconds for re-reading
                    're_read_pause_max': 2.0,
                    'micro_pause_chance': 0.25,  # 25% chance for micro-pause
                    'micro_pause_min': 0.2,  # 0.2-1 second for micro-pause
                    'micro_pause_max': 1.0
                },
                'thinking': {
                    'enable_thinking': True,  # Enable thinking behavior
                    'thinking_types': {
                        'quick_processing': {
                            'chance': 0.15,  # 15% chance for quick processing
                            'pause_min': 0.5,  # 0.5-2 seconds
                            'pause_max': 2.0,
                            'triggers': ['simple_content', 'familiar_topic']
                        },
                        'analytical_thinking': {
                            'chance': 0.20,  # 20% chance for analytical thinking
                            'pause_min': 2.0,  # 2-6 seconds
                            'pause_max': 6.0,
                            'triggers': ['complex_content', 'technical_topic']
                        },
                        'deep_contemplation': {
                            'chance': 0.08,  # 8% chance for deep contemplation
                            'pause_min': 4.0,  # 4-10 seconds
                            'pause_max': 10.0,
                            'triggers': ['important_content', 'new_concept']
                        },
                        'processing_information': {
                            'chance': 0.25,  # 25% chance for processing
                            'pause_min': 1.5,  # 1.5-4 seconds
                            'pause_max': 4.0,
                            'triggers': ['new_information', 'complex_sentence']
                        }
                    },
                    'thinking_context': {
                        'content_complexity_detection': True,  # Detect content complexity
                        'topic_familiarity_detection': True,  # Detect topic familiarity
                        'concept_importance_detection': True,  # Detect concept importance
                        'sentence_complexity_detection': True  # Detect sentence complexity
                    },
                    'thinking_patterns': {
                        'sequential_thinking': True,  # Enable sequential thinking
                        'parallel_thinking': True,  # Enable parallel thinking
                        'recursive_thinking': True,  # Enable recursive thinking
                        'associative_thinking': True  # Enable associative thinking
                    },
                    'thinking_behavior': {
                        'mouse_movement_during_thinking': True,  # Mouse movement during thinking
                        'eye_tracking_simulation': True,  # Simulate eye tracking
                        'micro_movements': True,  # Micro-movements during thinking
                        'breathing_pattern_simulation': True  # Simulate breathing patterns
                    }
                }
            },
            'risk': {
                'max_requests_per_minute': 30,
                'detection_threshold': 0.7,
                'cooldown_period': 60,
                'emergency_protocol_threshold': 0.9,
                'slow_down_threshold': 0.6
            },
            'ad_clicking': {
                'enabled': True,
                # 'click_chance': random.uniform(0.01, 0.25),  # Variasi chance 1-25% (lebih extreme)
                # 'max_clicks_per_session': random.randint(0, 8),  # Variasi jumlah 0-8 (termasuk 0)
                'click_chance': random.uniform(0.005, 0.15),  # Dikurangi ke 0.5-15% untuk menghindari invalid traffic
                'max_clicks_per_session': random.randint(0, 3),  # Dikurangi ke 0-3 untuk lebih konservatif
                'conservative_mode': True,
                'ad_types': ['google_adsense', 'google_vignette', 'google_afs', 'google_discovery'],  # Support multiple AdSense formats including Discovery
                # 'rate_limit_window': random.randint(900, 4800),  # Variasi window 15-80 menit (lebih extreme)
                # 'max_clicks_per_window': random.randint(0, 5),  # Variasi max clicks 0-5 (termasuk 0)
                'rate_limit_window': random.randint(1800, 7200),  # Ditingkatkan ke 30-120 menit untuk lebih aman
                'max_clicks_per_window': random.randint(0, 2),  # Dikurangi ke 0-2 untuk lebih konservatif
                'human_like_hesitation': True,  # Add human hesitation
                'random_click_timing': True,  # Randomize click timing
                'natural_reading_before_click': True,  # Read before clicking
                'random_skip_ads': True,  # Skip ads secara random
                'natural_hesitation': True,  # Tambahkan hesitation
                # 'variation_factor': random.uniform(0.5, 1.8),  # Variasi factor lebih extreme
                # 'session_skip_chance': random.uniform(0.1, 0.4),  # 10-40% chance skip entire session
                # 'ad_avoidance_pattern': random.choice(['conservative', 'moderate', 'aggressive']),  # Avoidance pattern
                # 'click_hesitation_factor': random.uniform(0.3, 2.0),  # Hesitation factor
                'variation_factor': random.uniform(0.3, 1.2),  # Dikurangi untuk lebih konservatif
                'session_skip_chance': random.uniform(0.2, 0.6),  # Ditingkatkan ke 20-60% untuk lebih aman
                'ad_avoidance_pattern': random.choice(['conservative', 'moderate']),  # Hapus 'aggressive' untuk lebih aman
                'click_hesitation_factor': random.uniform(0.5, 3.0),  # Ditingkatkan hesitation
                'invalid_traffic_protection': True,  # Tambahkan proteksi invalid traffic
                'min_session_duration': random.uniform(30, 120),  # Minimal 30-120 detik session
                'max_daily_clicks': random.randint(5, 15),  # Maksimal 5-15 klik per hari
                'natural_bounce_rate': random.uniform(0.3, 0.7),  # Bounce rate natural 30-70%
                'reading_time_before_click': random.uniform(3, 15),  # Baca 3-15 detik sebelum klik
                'natural_error_rate': random.uniform(0.05, 0.25)  # 5-25% natural error rate
            },
            'navigation': {
                'enabled': True,
                'max_navigation_depth': 3,
                'same_domain_preference': 0.8,
                'random_link_clicking': True
            },
            'article': {
                'default_urls': [
                    # 'https://rexdl.biz.id/cloud-computing-cost-optimization-how-us-companies-cut-expenses/',
                    # 'https://rexdl.biz.id/why-cloud-computing-is-the-backbone-of-us-healthcare-industry/',
                    # 'https://rexdl.biz.id/best-cloud-hosting-providers-for-small-businesses-in-america/',
                    # 'https://rexdl.biz.id/top-10-cloud-computing-services-for-businesses-in-the-united-states/',
                    # 'https://rexdl.biz.id/personal-loans-vs-private-student-loans-comparing-cost-interest-and-repayment-options/',
                    # 'https://rexdl.biz.id/quick-cash-loans-explained-how-they-work-what-they-really-cost-safer-alternatives/',
                    # 'https://rexdl.biz.id/life-insurance-rates-comparison-the-complete-guide-for-u-s-families-in-2025/',
                    # 'https://rexdl.biz.id/how-to-find-cheap-auto-insurance-quotes-in-the-u-s-the-complete-practical-guide/',
                    # 'https://rexdl.biz.id/ai-for-small-business-the-ultimate-guide-to-growth-efficiency-and-profit-in-2025/',

                    'https://tokenomics.web.id/tokenomics-bitcoin-btc-apakah-fixed-supply-selalu-aman/',
                    'https://tokenomics.web.id/bagaimana-tokenomics-solana-sol-mendorong-skalabilitas/',
                    'https://tokenomics.web.id/tokenomics-polygon-matic-layer-2-yang-menjanjikan/',
                    'https://tokenomics.web.id/tokenomics-shiba-inu-shib-apakah-burn-rate-mampu-naikkan-harga/',
                    'https://tokenomics.web.id/cara-membaca-tokenomics-sebelum-investasi-kripto-panduan-2025/',
                    'https://tokenomics.web.id/peran-bappebti-dalam-mengawasi-aset-kripto-di-indonesia/',

                    'https://primecapitalaid.web.id/cara-mendapatkan-bantuan-modal-usaha-umkm-tahun-2025-ulasan-teknis-uji-lapangan-dan-tips-lolos-seleksi/',
                    'https://primecapitalaid.web.id/bantuan-modal-umkm-khusus-perempuan-program-dan-syaratnya/',
                    'https://primecapitalaid.web.id/apa-itu-pinjaman-legal-ini-ciri-cirinya-yang-harus-anda-ketahui/',
                    'https://primecapitalaid.web.id/pinjaman-untuk-umkm-usaha-kecil-rekomendasi-pinjaman-legal-terdaftar-ojk-2025/',

                    # 'https://maxgaming.biz.id/how-to-open-a-bank-account-with-crypto-funds-in-the-united-states-2025-guide/',
                    # 'https://maxgaming.biz.id/online-mortgage-banking-with-bitcoin-the-future-of-real-estate-in-the-united-states/',
                    # 'https://maxgaming.biz.id/artificial-intelligence-in-healthcare-transforming-us-medicine/',
                    # 'https://maxgaming.biz.id/how-ai-automation-saves-time-and-money-for-us-businesses/',

                    # 'https://tokenomics.web.id/tokenomics-bitcoin-btc-apakah-fixed-supply-selalu-aman/',
                    # 'https://tokenomics.web.id/bagaimana-tokenomics-solana-sol-mendorong-skalabilitas/',
                    # 'https://tokenomics.web.id/tokenomics-polygon-matic-layer-2-yang-menjanjikan/',
                    # 'https://tokenomics.web.id/7-langkah-analisis-token-yang-wajib-kamu-lakukan-sebelum-membeli-panduan-2025/',
                    # 'https://tokenomics.web.id/cara-menilai-proyek-kripto-dari-distribusi-token-nya-panduan-2025/',

                    # 'https://gradua.web.id/bunga-0-3-bulan-pertama-untuk-pendaftar-baru',
                    # 'https://gradua.web.id/pinjaman-darurat-ojk-cair-5-menit-ke-rekening-tanpa-jaminan',
                    # 'https://gradua.web.id/cara-meminjam-uang-di-bank-untuk-modal-usaha-panduan-lengkap-dan-praktis',
                    # 'https://gradua.web.id/syarat-pinjaman-kur-2025-terbaru-panduan-lengkap-dan-lengkap-untuk-pengusaha',
                    # 'https://gradua.web.id/prediksi-pakar-ai-coin-ini-bisa-tembus-rp754-juta-per-koin-di-2030-simulasi-portofolio-2025',
                    # 'https://gradua.web.id/gila-roi-7-598-5-ai-coin-terbaik-2025-bittensor-render-network-paling-moncer',
                    # 'https://gradua.web.id/dari-rp500-ribu-jadi-milyaran-blueprint-investasi-ai-coin-untuk-pemula-2025',

                    # 'https://primecapitalaid.web.id/cara-mendapatkan-bantuan-modal-usaha-umkm-tahun-2025-ulasan-teknis-uji-lapangan-dan-tips-lolos-seleksi',
                    # 'https://primecapitalaid.web.id/program-bantuan-modal-untuk-usaha-mikro-kecil-syarat-cara-pengajuan/',
                    # 'https://primecapitalaid.web.id/bantuan-modal-umkm-khusus-perempuan-program-dan-syaratnya/',
                    # 'https://primecapitalaid.web.id/apa-itu-pinjaman-legal-ini-ciri-cirinya-yang-harus-anda-ketahui/',
                    # 'https://primecapitalaid.web.id/pinjaman-untuk-umkm-usaha-kecil-rekomendasi-pinjaman-legal-terdaftar-ojk-2025/',
                    # 'https://primecapitalaid.web.id/program-pinjaman-legal-dari-pemerintah-untuk-umkm-2025/',
                    # 'https://primecapitalaid.web.id/apa-itu-investasi-panduan-lengkap-untuk-pemula-yang-ingin-merdeka-finansial-di-2025/',
                    # 'https://primecapitalaid.web.id/apa-itu-literasi-keuangan-dan-mengapa-penting-panduan-komprehensif-melek-finansial-di-era-digital/',
                    
                    # 'https://setiap.zonagamegratisan.com/11-aplikasi-penghasil-uang-100-ribu-perhari/',
                    # 'https://setiap.zonagamegratisan.com/aplikasi-penghasil-uang-2025-yougov/',
                    # 'https://setiap.zonagamegratisan.com/aplikasi-penghasil-uang-tahun-2025/',
                    # 'https://setiap.zonagamegratisan.com/dana-mudah-cair-julo-kredit-digital/',
                    # 'https://setiap.zonagamegratisan.com/aplikasi-yang-langsung-memberikan-saldo-dana-gratis/',
                    # 'https://setiap.zonagamegratisan.com/dana-mudah-cair-online-aman-terdaftar-ojk/',
                ],
                'default_referers': [
                    # High CPC referers (Business/Finance/Tech)
                    # 'https://google.com', 'https://bing.com',
                    # 'https://linkedin.com', 'https://github.com', 'https://stackoverflow.com',
                    # 'https://medium.com', 'https://quora.com', 'https://forbes.com',
                    # 'https://bloomberg.com', 'https://reuters.com', 'https://wsj.com',
                    # 'https://techcrunch.com', 'https://wired.com', 'https://arstechnica.com',
                    # 'https://hbr.org', 'https://mckinsey.com', 'https://pwc.com',
                    # 'https://deloitte.com', 'https://kpmg.com', 'https://ey.com',
                    # 'https://ibm.com', 'https://microsoft.com', 'https://oracle.com',
                    # 'https://salesforce.com', 'https://adobe.com', 'https://intel.com',
                    # 'https://nvidia.com', 'https://amd.com', 'https://cisco.com',
                    # 'https://aws.amazon.com', 'https://cloud.google.com', 'https://azure.microsoft.com',
                    # 'https://hubspot.com',
                    
                    # # Additional Business/Finance referers
                    # 'https://cnbc.com', 'https://marketwatch.com', 'https://investing.com',
                    # 'https://yahoo.com/finance', 'https://finance.yahoo.com', 'https://seekingalpha.com',
                    # 'https://benzinga.com', 'https://fool.com', 'https://morningstar.com',
                    # 'https://nasdaq.com', 'https://nyse.com', 'https://sec.gov',
                    # 'https://federalreserve.gov', 'https://treasury.gov', 'https://irs.gov',
                    # 'https://sba.gov', 'https://ftc.gov', 'https://sec.gov',
                    # 'https://finra.org', 'https://cftc.gov', 'https://fdic.gov',
                    # 'https://occ.gov', 'https://federalreserve.gov', 'https://treasury.gov',
                    
                    # # Financial Services & Banking
                    # 'https://jpmorgan.com', 'https://bankofamerica.com', 'https://wellsfargo.com',
                    # 'https://citigroup.com', 'https://goldmansachs.com', 'https://morganstanley.com',
                    # 'https://blackrock.com', 'https://vanguard.com', 'https://fidelity.com',
                    # 'https://schwab.com', 'https://etrade.com', 'https://tdameritrade.com',
                    # 'https://interactivebrokers.com', 'https://robinhood.com', 'https://webull.com',
                    # 'https://sofi.com', 'https://chase.com', 'https://capitalone.com',
                    # 'https://americanexpress.com', 'https://visa.com', 'https://mastercard.com',
                    # 'https://paypal.com', 'https://square.com', 'https://stripe.com',
                    
                    # # Investment & Trading Platforms
                    # 'https://etrade.com', 'https://schwab.com', 'https://fidelity.com',
                    # 'https://vanguard.com', 'https://blackrock.com', 'https://goldmansachs.com',
                    # 'https://morganstanley.com', 'https://jpmorgan.com', 'https://citigroup.com',
                    # 'https://wellsfargo.com', 'https://bankofamerica.com', 'https://chase.com',
                    # 'https://robinhood.com', 'https://webull.com', 'https://sofi.com',
                    # 'https://interactivebrokers.com', 'https://tdameritrade.com', 'https://etrade.com',
                    # 'https://trading212.com', 'https://plus500.com', 'https://ig.com',
                    # 'https://oanda.com', 'https://forex.com', 'https://fxcm.com',
                    
                    # # Business News & Media
                    # 'https://businesswire.com', 'https://prnewswire.com', 'https://globenewswire.com',
                    # 'https://marketwatch.com', 'https://investing.com', 'https://benzinga.com',
                    # 'https://seekingalpha.com', 'https://fool.com', 'https://morningstar.com',
                    # 'https://nasdaq.com', 'https://nyse.com', 'https://otcmarkets.com',
                    # 'https://sec.gov', 'https://federalreserve.gov', 'https://treasury.gov',
                    # 'https://irs.gov', 'https://sba.gov', 'https://ftc.gov',
                    # 'https://finra.org', 'https://cftc.gov', 'https://fdic.gov',
                    
                    # # Technology & Innovation
                    # 'https://apple.com', 'https://google.com', 'https://microsoft.com',
                    # 'https://amazon.com', 'https://meta.com', 'https://netflix.com',
                    # 'https://tesla.com', 'https://spacex.com', 'https://openai.com',
                    # 'https://anthropic.com', 'https://deepmind.com', 'https://nvidia.com',
                    # 'https://amd.com', 'https://intel.com', 'https://qualcomm.com',
                    # 'https://broadcom.com', 'https://cisco.com', 'https://juniper.net',
                    # 'https://vmware.com', 'https://redhat.com', 'https://canonical.com',
                    # 'https://docker.com', 'https://kubernetes.io', 'https://terraform.io',
                    
                    # # Cloud & Enterprise Software
                    # 'https://aws.amazon.com', 'https://cloud.google.com', 'https://azure.microsoft.com',
                    # 'https://salesforce.com', 'https://oracle.com', 'https://sap.com',
                    # 'https://workday.com', 'https://servicenow.com', 'https://atlassian.com',
                    # 'https://slack.com', 'https://zoom.us', 'https://teams.microsoft.com',
                    # 'https://dropbox.com', 'https://box.com', 'https://onedrive.com',
                    # 'https://sharepoint.com', 'https://office.com', 'https://adobe.com',
                    # 'https://autodesk.com', 'https://ansys.com', 'https://solidworks.com',
                    # 'https://tableau.com', 'https://powerbi.com', 'https://qlik.com',
                    
                    # # Cybersecurity & Data
                    # 'https://crowdstrike.com', 'https://paloaltonetworks.com', 'https://fortinet.com',
                    # 'https://checkpoint.com', 'https://symantec.com', 'https://mcafee.com',
                    # 'https://trendmicro.com', 'https://kaspersky.com', 'https://bitdefender.com',
                    # 'https://splunk.com', 'https://elastic.co', 'https://databricks.com',
                    # 'https://snowflake.com', 'https://mongodb.com', 'https://redis.com',
                    # 'https://postgresql.org', 'https://mysql.com', 'https://oracle.com',
                    # 'https://ibm.com', 'https://hpe.com', 'https://dell.com',
                    
                    # # Consulting & Professional Services
                    # 'https://mckinsey.com', 'https://bain.com', 'https://bcg.com',
                    # 'https://pwc.com', 'https://deloitte.com', 'https://kpmg.com',
                    # 'https://ey.com', 'https://accenture.com', 'https://cognizant.com',
                    # 'https://infosys.com', 'https://tcs.com', 'https://wipro.com',
                    # 'https://capgemini.com', 'https://atos.net', 'https://dxc.com',
                    # 'https://hcl.com', 'https://techmahindra.com', 'https://mindtree.com',
                    # 'https://ltts.com', 'https://mphasis.com', 'https://hexaware.com',
                    
                    # # Venture Capital & Startups
                    # 'https://a16z.com', 'https://sequoiacap.com', 'https://accel.com',
                    # 'https://greylock.com', 'https://benchmark.com', 'https://kleinerperkins.com',
                    # 'https://firstround.com', 'https://foundersfund.com', 'https://union.vc',
                    # 'https://insightpartners.com', 'https://generalcatalyst.com', 'https://bessemer.com',
                    # 'https://lightspeed.com', 'https://matrixpartners.com', 'https://redpoint.com',
                    # 'https://nea.com', 'https://battery.com', 'https://ivp.com',
                    # 'https://ggv.com', 'https://dcm.com', 'https://sapphire.com',
                    
                    # # Medium CPC referers (General/Social)
                    # 'https://reddit.com', 'https://twitter.com', 'https://facebook.com',
                    # 'https://instagram.com', 'https://youtube.com', 'https://tiktok.com',
                    # 'https://pinterest.com', 'https://snapchat.com', 'https://discord.com',
                    # 'https://slack.com', 'https://zoom.us', 'https://teams.microsoft.com',
                    
                    # # Educational/Research referers
                    # 'https://wikipedia.org', 'https://scholar.google.com', 'https://researchgate.net',
                    # 'https://academia.edu', 'https://coursera.org', 'https://edx.org',
                    # 'https://udemy.com', 'https://khanacademy.org', 'https://mit.edu',
                    # 'https://stanford.edu', 'https://harvard.edu', 'https://berkeley.edu',
                    
                    # # News/Media referers
                    # 'https://cnn.com', 'https://bbc.com', 'https://nytimes.com',
                    # 'https://washingtonpost.com', 'https://usatoday.com', 'https://npr.org',
                    # 'https://ap.org', 'https://aljazeera.com', 'https://theguardian.com',
                    # 'https://independent.co.uk', 'https://telegraph.co.uk', 'https://ft.com',

                    'https://www.coindesk.com/markets/2025/09/15/dogecoin-inches-closer-to-wall-street-with-first-meme-coin-etf',
                    'https://www.coindesk.com/business/2025/09/18/ripple-franklin-templeton-and-dbs-to-offer-token-lending-and-trading',
                    'https://coinledger.io/tools/best-crypto-wallet',
                    'https://money.com/best-crypto-wallets/',
                    'https://shop.ledger.com/products/ledger-flex/graphite',
                    'https://hellopebl.com/resources/blog/best-crypto-wallets/',
                    'https://www.forbes.com/advisor/investing/cryptocurrency/best-crypto-wallets/',
                    'https://www.nerdwallet.com/p/best/investing/crypto-bitcoin-wallets',
                    'https://www.ig.com/en-ch/trading-strategies/the-5-crypto-trading-strategies-that-every-trader-needs-to-know-221123',
                    'https://www.gemini.com/cryptopedia/day-trading-crypto',
                    'https://www.avatrade.com/education/online-trading-strategies/crypto-trading-strategies',
                    'https://coindcx.com/blog/cryptocurrency/top-crypto-day-trading-strategies/',
                    'https://bravenewcoin.com/insights/ethereum-eth-price-prediction-ethereum-eyes-5000-as-bullish-cross-meets-fed-rate-cut-speculation',
                    'https://cointelegraph.com/news/price-predictions-917-btc-eth-xrp-bnb-sol-doge-ada-hype-link-sui',
                    'https://coinledger.io/tools/best-crypto-portfolio-tracker',
                    'https://www.litrg.org.uk/savings-property/cryptoassets-and-tax',

                    #insurance
                    'https://www.usnews.com/insurance/auto/geico-vs-progressive',
                    'https://www.cnbc.com/select/geico-vs-progressive-car-insurance-which-is-better/',
                    'https://www.bankrate.com/insurance/reviews/geico-vs-progressive/#is-geico-cheaper-than-progressive',
                    'https://www.forbes.com/advisor/car-insurance/geico-vs-progressive-car-insurance/',
                    'https://ca.trustpilot.com/review/www.statefarm.com',
                    'https://www.usnews.com/insurance/auto/state-farm-car-insurance-review',
                    'https://www.bankrate.com/insurance/reviews/state-farm/#car-insurance',
                    'https://www.allstate.ca/car-insurance',
                    'https://www.allstate.com/auto-insurance',
                    'https://www.farmers.com/home/',
                    'https://www.farmers.com/insurance/',
                    'https://www.usaa.com/inet/wc/insurance-products?akredirect=true',
                ],
                'high_cpc_weight': 0.9  # 70% chance to select high CPC referers
            }
        }
    
    def get(self, key_path, default=None):
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value


class TimingSystem:
    """Advanced timing system with human-like behavior"""
    def __init__(self):
        self.config = Configuration()
        self.last_action_time = 0
        self.action_history = []
        self.base_delay = 1.0
        self.delay_variability = 0.7
        self.long_pause_chance = self.config.get('timing.long_pause_chance', 0.05)
        self.long_pause_min = self.config.get('timing.long_pause_min', 3.0)
        self.long_pause_max = self.config.get('timing.long_pause_max', 8.0)
    
    def advanced_random_delay(self, base_delay=None, variability=None):
        """Generate advanced random delay with more natural variation"""
        if base_delay is None:
            base_delay = self.base_delay
        if variability is None:
            variability = self.delay_variability
        
        # Check for long pause chance with more natural variation
        if random.random() < self.long_pause_chance:
            long_pause = random.uniform(self.long_pause_min, self.long_pause_max)
            # Add random micro-pauses within long pause
            if random.random() < 0.3:  # 30% chance of micro-pause
                long_pause += random.uniform(0.5, 2.0)
            return long_pause
        
        # Generate delay with more natural distribution
        delay = random.normalvariate(base_delay, base_delay * variability)
        
        # Add natural hesitation patterns with extreme config variation
        hesitation_variation = self.config.get('timing.hesitation_variation', random.uniform(0.4, 2.0))
        if random.random() < 0.35:  # 35% chance of hesitation
            delay += random.uniform(0.2, 3.0) * hesitation_variation
        
        # Add natural timing factor from config
        natural_timing_factor = self.config.get('timing.natural_timing_factor', random.uniform(0.5, 2.0))
        delay *= natural_timing_factor
        
        # Add micro-pause chance
        micro_pause_chance = self.config.get('timing.micro_pause_chance', random.uniform(0.1, 0.4))
        if random.random() < micro_pause_chance:
            delay += random.uniform(0.1, 0.8)
        
        # Add macro-pause chance
        macro_pause_chance = self.config.get('timing.macro_pause_chance', random.uniform(0.02, 0.15))
        if random.random() < macro_pause_chance:
            delay += random.uniform(2.0, 8.0)
        
        # Add distraction pause chance
        distraction_pause_chance = self.config.get('timing.distraction_pause_chance', random.uniform(0.05, 0.25))
        if random.random() < distraction_pause_chance:
            delay += random.uniform(1.0, 5.0)
        
        # Add natural rhythm factor
        natural_rhythm_factor = self.config.get('timing.natural_rhythm_factor', random.uniform(0.6, 1.8))
        delay *= natural_rhythm_factor
        
        # Add timing chaos factor
        timing_chaos_factor = self.config.get('timing.timing_chaos_factor', random.uniform(0.1, 0.3))
        if random.random() < timing_chaos_factor:
            delay *= random.uniform(0.3, 3.0)  # Extreme chaos
        
        # Add micro-variations for more natural feel
        micro_variation = random.uniform(0.6, 1.6)
        delay *= micro_variation
        
        # Ensure minimum delay
        delay = max(0.2, delay)
        
        return delay
    
    def human_like_delay(self, delay_type="normal"):
        """Generate more human-like delays with imperfections"""
        if delay_type == "typing":
            # Add typing mistakes and corrections
            if random.random() < 0.15:  # 15% chance of hesitation
                return random.uniform(0.5, 2.0)  # Longer pause for thinking
            if random.random() < 0.08:  # 8% chance of typing mistake
                return random.uniform(0.8, 1.5)  # Time to correct mistake
            delay_range = (0.08, 0.4)  # More variation in typing speed
            delay = random.uniform(*delay_range)
            
        elif delay_type == "scrolling":
            # Add reading pauses
            if random.random() < 0.3:  # 30% chance of reading pause
                return random.uniform(3, 8)  # Reading pause
            if random.random() < 0.1:  # 10% chance of distraction
                return random.uniform(5, 15)  # Distraction pause
            delay_range = (0.8, 6.0)  # More variation in scroll timing
            delay = random.uniform(*delay_range)
            
        elif delay_type == "clicking":
            # Add hesitation before clicking
            if random.random() < 0.2:  # 20% chance of hesitation
                return random.uniform(1.5, 4.0)  # Hesitation pause
            if random.random() < 0.05:  # 5% chance of double-click attempt
                return random.uniform(0.1, 0.3)  # Quick double-click timing
            delay_range = (0.3, 2.5)  # More variation in click timing
            delay = random.uniform(*delay_range)
            
        elif delay_type == "reading":
            # Reading-specific delays
            if random.random() < 0.4:  # 40% chance of reading pause
                return random.uniform(2, 6)  # Reading content
            if random.random() < 0.15:  # 15% chance of re-reading
                return random.uniform(1, 3)  # Re-reading pause
            delay_range = (0.5, 3.0)  # General reading timing
            delay = random.uniform(*delay_range)
            
        else:
            # Add random human imperfections
            base_delay = random.uniform(0.5, 3.0)
            if random.random() < 0.1:  # 10% chance of long pause
                return random.uniform(5, 15)  # Distraction pause
            if random.random() < 0.05:  # 5% chance of very short pause
                return random.uniform(0.1, 0.3)  # Quick action
            delay = base_delay
        
        return delay
    
    def get_human_delay(self, base_delay=None):
        if base_delay is None:
            base_delay = random.uniform(
                self.config.get('timing.min_delay', 0.5),
                self.config.get('timing.max_delay', 3.0)
            )
        
        # Add variation based on action history
        if len(self.action_history) > 3:
            recent_avg = sum(self.action_history[-3:]) / 3
            variation = random.uniform(0.8, 1.2)
            base_delay = recent_avg * variation
        
        self.action_history.append(base_delay)
        if len(self.action_history) > 10:
            self.action_history.pop(0)
        
        return base_delay
    
    def wait_between_actions(self, min_delay=0.5, max_delay=3.0):
        delay = self.get_human_delay(random.uniform(min_delay, max_delay))
        time.sleep(delay)
        return delay


class DetectionPatterns:
    """Advanced detection patterns for various elements"""
    def __init__(self):
        self.ad_detection_patterns = {
            'google_adsense': [
                'ins[data-ad-client]',
                'ins[data-ad-slot]',
                '.adsbygoogle',
                '[data-ad-client]',
                '[data-ad-slot]',
                'ins[data-ad-format]',
                'ins[data-ad-layout]',
                'ins[data-ad-layout-key]',
                'ins[data-ad-test]',
                'ins[data-ad-status]',
                'ins[data-ad-type]',
                'ins[data-ad-version]',
                'ins[data-ad-region]',
                'ins[data-ad-provider]',
                'ins[data-ad-network]',
                'ins[data-ad-unit]',
                'ins[data-ad-placement]',
                'ins[data-ad-targeting]',
                'ins[data-ad-custom]',
                'ins[data-ad-responsive]',
                'ins[data-ad-auto]',
                'ins[data-ad-manual]',
                'ins[data-ad-optimized]',
                'ins[data-ad-enhanced]',
                'ins[data-ad-advanced]',
                'ins[data-ad-premium]',
                'ins[data-ad-pro]',
                'ins[data-ad-enterprise]',
                'ins[data-ad-business]',
                'ins[data-ad-commercial]',
                'ins[data-ad-sponsored]',
                'ins[data-ad-promoted]',
                'ins[data-ad-featured]',
                'ins[data-ad-highlighted]',
                'ins[data-ad-recommended]',
                'ins[data-ad-suggested]',
                'ins[data-ad-related]',
                'ins[data-ad-similar]',
                'ins[data-ad-matching]',
                'ins[data-ad-relevant]',
                'ins[data-ad-targeted]',
                'ins[data-ad-personalized]',
                'ins[data-ad-customized]',
                'ins[data-ad-tailored]'
            ],
            'google_vignette': [
                'ins[data-ad-format="vignette"]',
                'ins[data-ad-format*="vignette"]',
                '.adsbygoogle[data-ad-format="vignette"]',
                '[data-ad-format="vignette"]',
                'ins[data-ad-type="vignette"]',
                '.vignette-ad',
                '.fullscreen-ad',
                '.popup-ad',
                'ins[data-ad-layout="vignette"]',
                'ins[data-ad-placement="vignette"]',
                'ins[data-ad-targeting*="vignette"]',
                'ins[data-ad-custom*="vignette"]',
                'ins[data-ad-responsive="vignette"]',
                'ins[data-ad-auto="vignette"]',
                'ins[data-ad-manual="vignette"]',
                'ins[data-ad-optimized="vignette"]',
                'ins[data-ad-enhanced="vignette"]',
                'ins[data-ad-advanced="vignette"]',
                'ins[data-ad-premium="vignette"]',
                'ins[data-ad-pro="vignette"]',
                'ins[data-ad-enterprise="vignette"]',
                'ins[data-ad-business="vignette"]',
                'ins[data-ad-commercial="vignette"]',
                'ins[data-ad-sponsored="vignette"]',
                'ins[data-ad-promoted="vignette"]',
                'ins[data-ad-featured="vignette"]',
                'ins[data-ad-highlighted="vignette"]',
                'ins[data-ad-recommended="vignette"]',
                'ins[data-ad-suggested="vignette"]',
                'ins[data-ad-related="vignette"]',
                'ins[data-ad-similar="vignette"]',
                'ins[data-ad-matching="vignette"]',
                'ins[data-ad-relevant="vignette"]',
                'ins[data-ad-targeted="vignette"]',
                'ins[data-ad-personalized="vignette"]',
                'ins[data-ad-customized="vignette"]',
                'ins[data-ad-tailored="vignette"]'
            ],
            'google_discovery': [
                # Discovery in Content Widget
                '.autors-widget',
                '#autors-container-0',
                'iframe[src*="syndicatedsearch.goog/afs/ads"]',
                'iframe[name*="master-1"]',
                'iframe[id*="master-1"]',
                
                # Discovery Popup Drawer
                '#hd-drawer-container',
                '.hd-revealed',
                '#hd-drawer',
                '#hd-control-bar',
                '#hd-close-button',
                '#hd-back-arrow-button',
                '#hd-content-container',
                '#prose-iframe',
                'iframe[src*="gstatic.com/prose"]',
                
                # Discovery Popup Ads List
                '.gsc-results-wrapper-nooverlay',
                '.gsc-results-wrapper-visible',
                '.gsc-adBlock',
                'iframe[name*="master-2"]',
                'iframe[id*="master-2"]',
                'iframe[name*="master-a-2"]',
                'iframe[name*="master-b-2"]',
                'iframe[src*="syndicatedsearch.goog/cse_v2/ads"]',
                'iframe[src*="syndicatedsearch.goog/afs/ads/i/iframe.html"]',
                
                # Generic Discovery patterns
                'ins[data-ad-format="discovery"]',
                'ins[data-ad-format*="discovery"]',
                '.adsbygoogle[data-ad-format="discovery"]',
                '[data-ad-format="discovery"]',
                'ins[data-ad-type="discovery"]',
                '.discovery-ad',
                '.feed-ad',
                '.content-ad',
                'ins[data-ad-layout="discovery"]',
                'ins[data-ad-placement="discovery"]',
                'ins[data-ad-targeting*="discovery"]',
                'ins[data-ad-custom*="discovery"]',
                'ins[data-ad-responsive="discovery"]',
                'ins[data-ad-auto="discovery"]',
                'ins[data-ad-manual="discovery"]',
                'ins[data-ad-optimized="discovery"]',
                'ins[data-ad-enhanced="discovery"]',
                'ins[data-ad-advanced="discovery"]',
                'ins[data-ad-premium="discovery"]',
                'ins[data-ad-pro="discovery"]',
                'ins[data-ad-enterprise="discovery"]',
                'ins[data-ad-business="discovery"]',
                'ins[data-ad-commercial="discovery"]',
                'ins[data-ad-sponsored="discovery"]',
                'ins[data-ad-promoted="discovery"]',
                'ins[data-ad-featured="discovery"]',
                'ins[data-ad-highlighted="discovery"]',
                'ins[data-ad-recommended="discovery"]',
                'ins[data-ad-suggested="discovery"]',
                'ins[data-ad-related="discovery"]',
                'ins[data-ad-similar="discovery"]',
                'ins[data-ad-matching="discovery"]',
                'ins[data-ad-relevant="discovery"]',
                'ins[data-ad-targeted="discovery"]',
                'ins[data-ad-personalized="discovery"]',
                'ins[data-ad-customized="discovery"]',
                'ins[data-ad-tailored="discovery"]'
            ],
            'google_afs': [
                # AFS Side Rail (In Page) - ACTUAL STRUCTURE
                '#google-anno-sa',
                '[google-side-rail-overlap="true"]',
                '.google-anno-sa-qtx',
                '.google-anno-skip',
                '#gda',
                '[data-google-vignette="false"]',
                '[data-google-interstitial="false"]',
                '.google-anno-sa-intent-icon',
                
                # AFS Popup Drawer - ACTUAL STRUCTURE
                '#hd-drawer-container',
                '.hd-revealed',
                '#hd-drawer',
                '#hd-control-bar',
                '#hd-close-button',
                '#hd-back-arrow-button',
                '.hd-control-button',
                '#hd-content-container',
                'iframe[srcdoc*="gda-search-term"]',
                'iframe[srcdoc*="display-slot-container"]',
                'iframe[srcdoc*="adsbygoogle"]',
                
                # AFS Search Results - ACTUAL STRUCTURE
                '#gda-search-term',
                '#display-slot-container',
                '#display-slot',
                'ins[data-ad-intent-query]',
                'ins[data-ad-intent-qetid]',
                'ins[data-ad-intents-format]',
                'ins[data-ad-intent-rs-token]',
                'ins[data-query-targeted="true"]',
                'ins[data-ad-client*="ca-pub-"]',
                
                # AFS Side Rail Specific
                '[aria-label*="Buka opsi belanja"]',
                '[aria-label*="Tutup anchor belanja"]',
                '[role="link"][tabindex="0"]',
                '[role="button"][aria-label*="Tutup"]',
                
                # Generic AFS patterns
                'ins[data-ad-format="search"]',
                'ins[data-ad-format*="search"]',
                '.adsbygoogle[data-ad-format="search"]',
                '[data-ad-format="search"]',
                'ins[data-ad-type="search"]',
                '.search-ad',
                '.afs-ad',
                'ins[data-ad-layout="search"]',
                'ins[data-ad-placement="search"]',
                'ins[data-ad-targeting*="search"]',
                'ins[data-ad-custom*="search"]',
                'ins[data-ad-responsive="search"]',
                'ins[data-ad-auto="search"]',
                'ins[data-ad-manual="search"]',
                'ins[data-ad-optimized="search"]',
                'ins[data-ad-enhanced="search"]',
                'ins[data-ad-advanced="search"]',
                'ins[data-ad-premium="search"]',
                'ins[data-ad-pro="search"]',
                'ins[data-ad-enterprise="search"]',
                'ins[data-ad-business="search"]',
                'ins[data-ad-commercial="search"]',
                'ins[data-ad-sponsored="search"]',
                'ins[data-ad-promoted="search"]',
                'ins[data-ad-featured="search"]',
                'ins[data-ad-highlighted="search"]',
                'ins[data-ad-recommended="search"]',
                'ins[data-ad-suggested="search"]',
                'ins[data-ad-related="search"]',
                'ins[data-ad-similar="search"]',
                'ins[data-ad-matching="search"]',
                'ins[data-ad-relevant="search"]',
                'ins[data-ad-targeted="search"]',
                'ins[data-ad-personalized="search"]',
                'ins[data-ad-customized="search"]',
                'ins[data-ad-tailored="search"]'
            ]
        }
        
        self.captcha_patterns = [
            '#captcha', '.captcha', '.g-recaptcha', '[data-sitekey]',
            '.recaptcha', '[data-testid*="captcha"]'
        ]
        
        self.navigation_patterns = {
            'next': [
                'a[rel="next"]',
                '.next',
                '.next-page',
                '[aria-label*="next"]',
                'a:contains("Next")',
                'a:contains(">")'
            ],
            'previous': [
                'a[rel="prev"]',
                '.prev',
                '.previous',
                '.previous-page',
                '[aria-label*="previous"]',
                'a:contains("Previous")',
                'a:contains("<")'
            ]
        }
        
        self.behavioral_anomaly_patterns = [
            'webdriver',
            'selenium',
            'phantomjs',
            'headless',
            'automation'
        ]


class MouseMovementSimulator:
    """Advanced mouse movement simulation"""
    def __init__(self, driver):
        self.driver = driver
        self.config = Configuration()
        self.movement_history = []
    
    def human_like_movement(self, start_pos, end_pos, steps=None):
        """More human-like mouse movement with natural imperfections"""
        if steps is None:
            distance = ((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)**0.5
            # More natural step calculation with extreme random variation
            base_steps = max(3, min(120, int(distance / 12)))  # Base steps dengan range extreme
            steps = base_steps + random.randint(-15, 35)  # Add extreme random variation
            steps = max(2, min(150, steps))  # Ensure reasonable range dengan variasi extreme
        
        points = []
        for i in range(steps + 1):
            t = i / steps
            
            # Add more realistic human imperfections
            imperfection_x = random.uniform(-5, 5)  # Increased micro-tremors
            imperfection_y = random.uniform(-5, 5)
            
            # Add natural overshoot and correction
            if random.random() < 0.15:  # 15% chance of overshoot
                overshoot_x = random.uniform(-8, 8)
                overshoot_y = random.uniform(-8, 8)
                imperfection_x += overshoot_x
                imperfection_y += overshoot_y
            
            # More natural bezier curve with extreme variation and randomness
            # Control point 1 with extreme natural variation
            control1_factor_x = random.uniform(0.02, 1.0)  # Extreme variation
            control1_factor_y = random.uniform(0.02, 1.0)  # Independent extreme variation
            control1_x = start_pos[0] + (end_pos[0] - start_pos[0]) * control1_factor_x + random.randint(-150, 150)
            control1_y = start_pos[1] + (end_pos[1] - start_pos[1]) * control1_factor_y + random.randint(-150, 150)
            
            # Control point 2 with extreme natural variation
            control2_factor_x = random.uniform(0.1, 1.5)  # Extreme variation
            control2_factor_y = random.uniform(0.1, 1.5)  # Independent extreme variation
            control2_x = start_pos[0] + (end_pos[0] - start_pos[0]) * control2_factor_x + random.randint(-130, 130)
            control2_y = start_pos[1] + (end_pos[1] - start_pos[1]) * control2_factor_y + random.randint(-130, 130)
            
            x = (1-t)**3 * start_pos[0] + 3*(1-t)**2*t * control1_x + 3*(1-t)*t**2 * control2_x + t**3 * end_pos[0]
            y = (1-t)**3 * start_pos[1] + 3*(1-t)**2*t * control1_y + 3*(1-t)*t**2 * control2_y + t**3 * end_pos[1]
            
            # Add imperfections
            x += imperfection_x
            y += imperfection_y
            
            # Add occasional micro-corrections (like human adjusting)
            if random.random() < 0.35:  # 35% chance
                x += random.uniform(-8, 8)
                y += random.uniform(-8, 8)
            
            # Add natural jitter
            if random.random() < 0.60:  # 60% chance of jitter
                x += random.uniform(-3, 3)
                y += random.uniform(-3, 3)
            
            # Add occasional hesitation
            if random.random() < 0.18:  # 18% chance of hesitation
                x += random.uniform(-12, 12)
                y += random.uniform(-12, 12)
            
            # Add natural tremor
            if random.random() < 0.50:  # 50% chance of tremor
                x += random.uniform(-2.5, 2.5)
                y += random.uniform(-2.5, 2.5)
            
            # Add occasional overshoot
            if random.random() < 0.15:  # 15% chance of overshoot
                x += random.uniform(-15, 15)
                y += random.uniform(-15, 15)
            
            # Add natural drift
            if random.random() < 0.30:  # 30% chance of drift
                x += random.uniform(-5, 5)
                y += random.uniform(-5, 5)
            
            # Add natural fatigue
            if random.random() < 0.08:  # 8% chance of fatigue
                x += random.uniform(-20, 20)
                y += random.uniform(-20, 20)
            
            # Add natural distraction
            if random.random() < 0.05:  # 5% chance of distraction
                x += random.uniform(-25, 25)
                y += random.uniform(-25, 25)
            
            # Add natural muscle memory
            if random.random() < 0.12:  # 12% chance of muscle memory
                x += random.uniform(-6, 6)
                y += random.uniform(-6, 6)
            
            # Add natural anticipation
            if random.random() < 0.10:  # 10% chance of anticipation
                x += random.uniform(-8, 8)
                y += random.uniform(-8, 8)
            
            points.append((int(x), int(y)))
        
        return points
    
    def move_to_element(self, element, smooth=True):
        try:
            # Check if element is still valid
            try:
                # Test if element is still attached to DOM
                element.is_displayed()
            except Exception as e:
                logging.warning(f"Element is stale, skipping mouse movement: {e}")
                return False
            
            if smooth:
                try:
                    # Get element position safely
                    location = element.location_once_scrolled_into_view
                    size = element.size
                    center_x = location['x'] + size['width'] // 2
                    center_y = location['y'] + size['height'] // 2
                    
                    # Get current mouse position (approximate)
                    current_pos = (random.randint(0, 1920), random.randint(0, 1080))
                    target_pos = (center_x, center_y)
                    
                    # Generate movement path
                    movement_points = self.human_like_movement(current_pos, target_pos)
                    
                    # Execute movement with error handling
                    for point in movement_points:
                        try:
                            self.driver.execute_script(f"""
                                try {{
                                    var event = new MouseEvent('mousemove', {{
                                        clientX: {point[0]},
                                        clientY: {point[1]},
                                        bubbles: true
                                    }});
                                    document.dispatchEvent(event);
                                }} catch(e) {{
                                    // Ignore mouse movement errors
                                }}
                            """)
                        except Exception as e:
                            # Ignore individual mouse movement errors
                            pass
                        time.sleep(random.uniform(0.01, 0.05))
                except Exception as e:
                    logging.warning(f"Smooth mouse movement failed: {e}")
            
            # Move to element using ActionChains with error handling
            try:
                ActionChains(self.driver).move_to_element(element).perform()
                return True
            except Exception as e:
                logging.warning(f"ActionChains mouse movement failed: {e}")
                return False
                
        except Exception as e:
            logging.warning(f"Mouse movement failed: {e}")
            return False
    
    def random_mouse_movement(self, duration=1.0):
        """Enhanced random mouse movement with more natural human-like patterns"""
        # Check if mouse movement is enabled in config
        if not self.config.get('behavior.mouse_movement', True):
            return True
            
        try:
            # Get viewport size safely
            try:
                viewport_size = self.driver.execute_script("return {width: window.innerWidth, height: window.innerHeight}")
            except Exception as e:
                # Fallback viewport size
                viewport_size = {'width': 1920, 'height': 1080}
            
            start_time = time.time()
            current_pos = (random.randint(50, viewport_size['width']-50),
                          random.randint(50, viewport_size['height']-50))
            
            # Use behavioral profiles from config
            behavioral_profiles = self.config.get('behavior.behavioral_profiles', ['exploratory', 'focused', 'wandering', 'hesitant', 'reading', 'distracted'])
            movement_pattern = random.choice(behavioral_profiles)
            
            # Add natural micro-movements based on config
            random_delays_enabled = self.config.get('behavior.random_delays', True)
            micro_movement_chance = 0.3 if random_delays_enabled else 0.1  # Reduced chance if random delays disabled
            
            while time.time() - start_time < duration:
                try:
                    if movement_pattern == "exploratory":
                        # Large movements exploring the page
                        target_pos = (random.randint(100, viewport_size['width']-100),
                                     random.randint(100, viewport_size['height']-100))
                        movement_speed = random.uniform(0.02, 0.08)
                        
                    elif movement_pattern == "focused":
                        # Small movements around current area
                        target_pos = (current_pos[0] + random.randint(-100, 100),
                                     current_pos[1] + random.randint(-100, 100))
                        target_pos = (max(50, min(viewport_size['width']-50, target_pos[0])),
                                     max(50, min(viewport_size['height']-50, target_pos[1])))
                        movement_speed = random.uniform(0.01, 0.04)
                        
                    elif movement_pattern == "wandering":
                        # Medium movements with pauses
                        target_pos = (random.randint(200, viewport_size['width']-200),
                                     random.randint(200, viewport_size['height']-200))
                        movement_speed = random.uniform(0.03, 0.06)
                        
                    else:  # hesitant
                        # Small movements with frequent pauses
                        target_pos = (current_pos[0] + random.randint(-50, 50),
                                     current_pos[1] + random.randint(-50, 50))
                        target_pos = (max(50, min(viewport_size['width']-50, target_pos[0])),
                                     max(50, min(viewport_size['height']-50, target_pos[1])))
                        movement_speed = random.uniform(0.01, 0.03)
                    
                    movement_points = self.human_like_movement(current_pos, target_pos)
                    
                    for point in movement_points:
                        if time.time() - start_time >= duration:
                            break
                        
                        try:
                            # Safe mouse movement with error handling
                            self.driver.execute_script(f"""
                                try {{
                                    var event = new MouseEvent('mousemove', {{
                                        clientX: {point[0]},
                                        clientY: {point[1]},
                                        bubbles: true
                                    }});
                                    document.dispatchEvent(event);
                                }} catch(e) {{
                                    // Ignore mouse movement errors
                                }}
                            """)
                        except Exception as e:
                            # Ignore individual mouse movement errors
                            pass
                        
                        time.sleep(movement_speed)
                        
                        # Add occasional pauses (like human hesitation)
                        if random.random() < 0.1:  # 10% chance
                            time.sleep(random.uniform(0.1, 0.3))
                    
                    current_pos = target_pos
                    
                    # Human-like pause between movements
                    if movement_pattern == "hesitant":
                        time.sleep(random.uniform(0.3, 1.0))  # Longer pauses
                    else:
                        time.sleep(random.uniform(0.1, 0.5))
                    
                    # Occasionally change movement pattern
                    if random.random() < 0.2:  # 20% chance
                        movement_pattern = random.choice(["exploratory", "focused", "wandering", "hesitant"])
                    
                except Exception as e:
                    # If there's an error in the movement loop, break out
                    break
                    
        except Exception as e:
            # Ignore mouse movement errors completely
            pass


class RiskMonitor:
    """Advanced risk monitoring system"""
    def __init__(self, driver):
        self.driver = driver
        self.config = Configuration()
        self.request_history = []
        self.detection_events = []
        self.risk_level = "low"
        self.request_count = 0
        self.last_request_time = 0
    
    def can_make_request(self) -> bool:
        current_time = time.time()
        max_requests = self.config.get('risk.max_requests_per_minute', 30)
        
        # Remove requests older than 1 minute
        self.request_history = [req_time for req_time in self.request_history 
                              if current_time - req_time < 60]
        
        return len(self.request_history) < max_requests
    
    def record_request(self):
        self.request_history.append(time.time())
        self.request_count += 1
        self.last_request_time = time.time()
    
    def check_detection_signals(self):
        signals = {
            'captcha_detected': False,
            'unusual_requests': False,
            'behavioral_anomalies': False,
            'automation_flags': False
        }
        
        try:
            # Check for CAPTCHA
            captcha_selectors = [
                "iframe[src*='recaptcha']",
                ".g-recaptcha",
                "#captcha",
                ".captcha"
            ]
            
            for selector in captcha_selectors:
                try:
                    if self.driver.find_element(By.CSS_SELECTOR, selector):
                        signals['captcha_detected'] = True
                        break
                except NoSuchElementException:
                    continue
            
            # Check for unusual requests
            if not self.can_make_request():
                signals['unusual_requests'] = True
            
            # Check for behavioral anomalies
            signals['behavioral_anomalies'] = self._detect_behavioral_anomalies()
            
            # Check for automation flags
            automation_indicators = [
                "webdriver",
                "selenium",
                "phantomjs",
                "headless"
            ]
            
            user_agent = self.driver.execute_script("return navigator.userAgent;")
            for indicator in automation_indicators:
                if indicator.lower() in user_agent.lower():
                    signals['automation_flags'] = True
                    break
        
        except Exception as e:
            logging.warning(f"Error checking detection signals: {e}")
        
        return signals
    
    def _detect_behavioral_anomalies(self) -> bool:
        try:
            # Check for too fast interactions
            if len(self.request_history) > 10:
                recent_requests = self.request_history[-10:]
                avg_interval = sum(recent_requests[i+1] - recent_requests[i] 
                                 for i in range(len(recent_requests)-1)) / (len(recent_requests)-1)
                if avg_interval < 1.0:  # Less than 1 second between requests
                    return True
            
            return False
        except Exception:
            return False
    
    def assess_risk_level(self, signals):
        risk_score = 0
        
        if signals['captcha_detected']:
            risk_score += 0.4
        if signals['unusual_requests']:
            risk_score += 0.3
        if signals['behavioral_anomalies']:
            risk_score += 0.2
        if signals['automation_flags']:
            risk_score += 0.1
        
        if risk_score >= 0.7:
            return "high"
        elif risk_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def handle_risk(self, signals):
        risk_level = self.assess_risk_level(signals)
        self.risk_level = risk_level
        
        if risk_level == "high":
            return self._handle_high_risk()
        elif risk_level == "medium":
            return self._handle_medium_risk()
        else:
            return self._handle_low_risk()
    
    def _handle_high_risk(self):
        logging.warning("High risk detected - implementing extended cooldown")
        time.sleep(random.uniform(30, 60))
        return False
    
    def _handle_medium_risk(self):
        logging.warning("Medium risk detected - implementing short cooldown")
        time.sleep(random.uniform(10, 20))
        return True
    
    def _handle_low_risk(self):
        return True
    
    def get_risk_statistics(self):
        return {
            'current_risk_level': self.risk_level,
            'total_requests': self.request_count,
            'requests_last_minute': len(self.request_history),
            'detection_events': len(self.detection_events),
            'last_request_time': self.last_request_time
        }


class AdClickingSystem:
    """Advanced ad clicking system with conservative behavior"""
    
    def __init__(self, driver, timing_system, mouse_simulator):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.click_history = []
        self.config = Configuration()
        self.patterns = DetectionPatterns()
        
    def detect_ads(self, page_source=None):
        """Detect ads pada current page"""
        detected_ads = []
        
        try:
            # Use provided page source or get current page
            if page_source is None:
                page_source = self.driver.page_source
            
            # Check different ad patterns
            for ad_type, selectors in self.patterns.ad_detection_patterns.items():
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        for element in elements:
                            if self._is_valid_ad_element(element):
                                ad_info = {
                                    'element': element,
                                    'type': ad_type,
                                    'selector': selector,
                                    'position': element.location,
                                    'size': element.size,
                                    'is_visible': element.is_displayed(),
                                    'click_probability': self._calculate_click_probability(element, ad_type)
                                }
                                detected_ads.append(ad_info)
                                
                    except Exception as e:
                        continue
            
            return detected_ads
            
        except Exception as e:
            return []
    
    def _is_valid_ad_element(self, element):
        """Validate if element is a valid ad element"""
        try:
            # Check if element is visible and has reasonable size
            if not element.is_displayed():
                return False
            
            size = element.size
            if size['width'] < 50 or size['height'] < 50:
                return False
            
            # Check if element is in viewport
            location = element.location
            if location['x'] < 0 or location['y'] < 0:
                return False
            
            # Check for common ad attributes
            ad_attributes = ['data-ad', 'data-ad-client', 'data-ad-slot', 'data-ad-unit']
            for attr in ad_attributes:
                if element.get_attribute(attr):
                    return True
            
            # Check for ad-related classes
            class_name = element.get_attribute('class') or ''
            if any(keyword in class_name.lower() for keyword in ['ad', 'advertisement', 'adsbygoogle']):
                return True
            
            return True
            
        except Exception as e:
            return False
    
    def _calculate_click_probability(self, element, ad_type):
        """Calculate click probability with more natural randomization"""
        # Only calculate for supported Google AdSense formats
        supported_types = ['google_adsense', 'google_vignette', 'google_afs', 'google_discovery']
        if ad_type not in supported_types:
            return 0.0
        
        # Use dynamic base probability with extreme natural variation
        base_probability = self.config.get('ad_clicking.click_chance', random.uniform(0.01, 0.25))
        
        # Add natural variation factor from config
        variation_factor = self.config.get('ad_clicking.variation_factor', random.uniform(0.5, 1.8))
        base_probability *= variation_factor
        
        # Add random hesitation factor with more variation
        hesitation_factor = self.config.get('ad_clicking.click_hesitation_factor', random.uniform(0.3, 2.0))
        base_probability *= hesitation_factor
        
        # Add session skip chance
        session_skip_chance = self.config.get('ad_clicking.session_skip_chance', random.uniform(0.1, 0.4))
        if random.random() < session_skip_chance:
            base_probability *= 0.1  # Drastically reduce probability
        
        # Add natural error rate
        natural_error_rate = self.config.get('ad_clicking.natural_error_rate', random.uniform(0.05, 0.25))
        if random.random() < natural_error_rate:
            base_probability *= random.uniform(0.1, 0.5)  # Reduce due to "human error"
        
        try:
            # Adjust base probability based on ad type
            if ad_type == 'google_adsense':
                base_probability *= 1.5  # 50% higher for standard AdSense
            elif ad_type == 'google_vignette':
                base_probability *= 1.8  # 80% higher for vignette (full-screen, high value)
            elif ad_type == 'google_afs':
                base_probability *= 1.3  # 30% higher for AFS (search-based, targeted)
            elif ad_type == 'google_discovery':
                base_probability *= 1.4  # 40% higher for discovery ads (content-based, high engagement)
            
            # Adjust based on element size
            size = element.size
            area = size['width'] * size['height']
            
            if area > 100000:  # Large ads
                base_probability *= 0.8
            elif area < 10000:  # Small ads
                base_probability *= 0.4
            else:  # Medium ads
                base_probability *= 1.2
            
            # Adjust based on position
            location = element.location
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            if location['y'] > viewport_height * 0.8:  # Below fold
                base_probability *= 0.6
            elif location['y'] < viewport_height * 0.2:  # Above fold
                base_probability *= 1.3
            else:  # Middle fold
                base_probability *= 1.1
            
            # Check AdSense specific attributes
            if element.get_attribute('data-ad-client'):
                base_probability *= 1.2
            if element.get_attribute('data-ad-slot'):
                base_probability *= 1.1
            if element.get_attribute('data-ad-format'):
                base_probability *= 1.05
            
            # Ensure probability is within reasonable bounds
            return max(0.01, min(base_probability, 0.4))
            
        except Exception as e:
            return base_probability
    
    def click_ads(self, max_clicks=1, conservative=True):
        """Click ads dengan conservative behavior"""
        clicked_ads = []
        
        try:
            # Detect ads on current page
            detected_ads = self.detect_ads()
            
            if not detected_ads:
                return clicked_ads
            
            # Sort ads by click probability (highest first)
            detected_ads.sort(key=lambda x: x['click_probability'], reverse=True)
            
            # Click ads based on probability and limits
            clicks_attempted = 0
            for ad_info in detected_ads:
                if clicks_attempted >= max_clicks:
                    break
                
                if self._should_click_ad(ad_info, conservative):
                    if self._click_ad_safely(ad_info):
                        clicked_ads.append(ad_info)
                        clicks_attempted += 1
                        
                        # Add delay between clicks
                        if clicks_attempted < max_clicks:
                            delay = self.timing.human_like_delay("clicking")
                            time.sleep(delay)
            
            return clicked_ads
            
        except Exception as e:
            return clicked_ads
    
    def _should_click_ad(self, ad_info, conservative):
        """Determine if ad should be clicked - Support multiple Google AdSense formats"""
        try:
            # Only click supported Google AdSense ad types
            supported_types = ['google_adsense', 'google_vignette', 'google_afs', 'google_discovery']
            if ad_info['type'] not in supported_types:
                return False
            
            # Check click probability
            if random.random() > ad_info['click_probability']:
                return False
            
            # Conservative checks for Google AdSense
            if conservative:
                # Don't click if we've clicked too many ads recently
                rate_limit_window = self.config.get('ad_clicking.rate_limit_window', 1200)  # Default 20 minutes
                max_clicks_per_window = self.config.get('ad_clicking.max_clicks_per_window', 3)  # Default 3 clicks
                
                recent_clicks = [click for click in self.click_history 
                               if time.time() - click['timestamp'] < rate_limit_window]
                
                if len(recent_clicks) >= max_clicks_per_window:
                    return False
                
                # Don't click if ad is too small (higher threshold for AdSense)
                size = ad_info['size']
                if size['width'] < 120 or size['height'] < 60:
                    return False
                
                # Check if ad has proper AdSense attributes
                element = ad_info['element']
                if not (element.get_attribute('data-ad-client') or element.get_attribute('data-ad-slot')):
                    return False
            
            return True
            
        except Exception as e:
            return False
    
    def _click_ad_safely(self, ad_info):
        """Click ad safely dengan human-like behavior dan invalid traffic protection"""
        try:
            # Check invalid traffic protection
            if not self._check_invalid_traffic_protection():
                self.logger.info("[PROTECTION] Skipping ad click due to invalid traffic protection")
                return False
            
            element = ad_info['element']
            
            # Scroll to ad first
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            
            # Wait for element to be clickable
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable(element))
            
            # Natural reading time before clicking (3-15 detik)
            reading_time = self.config.get('ad_clicking.reading_time_before_click', random.uniform(3, 15))
            self.logger.info(f"[AD CLICK] Reading content for {reading_time:.1f}s before clicking")
            time.sleep(reading_time)
            
            # Add human-like delay before clicking
            pre_click_delay = self.timing.human_like_delay("clicking")
            time.sleep(pre_click_delay)
            
            # Use mouse simulator for human-like clicking
            if self.mouse.move_to_element(element):
                element.click()
                
                # Record click in history
                click_record = {
                    'timestamp': time.time(),
                    'ad_type': ad_info['type'],
                    'position': ad_info['position'],
                    'size': ad_info['size']
                }
                self.click_history.append(click_record)
                
                # Add post-click delay
                post_click_delay = self.timing.human_like_delay("clicking")
                time.sleep(post_click_delay)
                
                # Handle landing page after successful click
                self._handle_ad_landing_page()
                
                # Special handling for vignette ads (popup behavior)
                if ad_info['type'] == 'google_vignette':
                    self._handle_vignette_ad_behavior()
                
                # Special handling for discovery ads (popup behavior)
                if ad_info['type'] == 'google_discovery':
                    self._handle_discovery_ad_behavior()
                
                # Special handling for AFS ads (popup behavior)
                if ad_info['type'] == 'google_afs':
                    self._handle_afs_ad_behavior()
                
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def _check_invalid_traffic_protection(self):
        """Check if we should skip clicking to avoid invalid traffic detection"""
        try:
            # Check daily click limit
            max_daily_clicks = self.config.get('ad_clicking.max_daily_clicks', 15)
            today_clicks = self._get_today_click_count()
            if today_clicks >= max_daily_clicks:
                self.logger.info(f"[PROTECTION] Daily click limit reached: {today_clicks}/{max_daily_clicks}")
                return False
            
            # Check session duration
            min_session_duration = self.config.get('ad_clicking.min_session_duration', 30)
            session_duration = time.time() - getattr(self, 'session_start_time', time.time())
            if session_duration < min_session_duration:
                self.logger.info(f"[PROTECTION] Session too short: {session_duration:.1f}s < {min_session_duration}s")
                return False
            
            # Check natural bounce rate
            natural_bounce_rate = self.config.get('ad_clicking.natural_bounce_rate', 0.5)
            if random.random() < natural_bounce_rate:
                self.logger.info(f"[PROTECTION] Natural bounce rate: {natural_bounce_rate:.1%}")
                return False
            
            # Check session skip chance
            session_skip_chance = self.config.get('ad_clicking.session_skip_chance', 0.4)
            if random.random() < session_skip_chance:
                self.logger.info(f"[PROTECTION] Session skip chance: {session_skip_chance:.1%}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.warning(f"[PROTECTION] Error in invalid traffic protection: {e}")
            return True  # Allow clicking if error occurs
    
    def _get_today_click_count(self):
        """Get click count for today"""
        try:
            today = time.strftime('%Y-%m-%d')
            today_clicks = [click for click in self.click_history 
                           if time.strftime('%Y-%m-%d', time.localtime(click['timestamp'])) == today]
            return len(today_clicks)
        except:
            return 0
    
    def _handle_ad_landing_page(self):
        """Handle ad landing page after click - ALWAYS go back"""
        try:
            current_url = self.driver.current_url
            self.logger.info(f"[LANDING] Navigated to: {current_url[:60]}...")
            
            # Simulate natural behavior on landing page
            self._simulate_landing_page_behavior()
            
            # ALWAYS go back to original page (no domain checking needed)
            self.driver.back()
            time.sleep(random.uniform(2, 4))
            self.logger.info("[RETURN] Returned to original page")
            return True
        
        except Exception as e:
            self.logger.error(f"[ERROR] Error handling ad landing page: {e}")
            # Fallback: still try to go back
            try:
                self.driver.back()
                self.logger.info("[FALLBACK] Attempted to return to original page")
            except:
                pass
            return False
    
    def _simulate_landing_page_behavior(self):
        """Simulate natural user behavior on ad landing page with enhanced security"""
        try:
            # Total time on landing page (30-60 seconds) with more variation
            total_time = random.uniform(30, 60)  # 30 seconds to 1 minute
            self.logger.info(f"[TIMER] Spending {total_time:.1f} seconds on landing page with natural behavior")
            
            start_time = time.time()
            end_time = start_time + total_time
            
            # Get page dimensions for scroll calculations
            try:
                page_height = self.driver.execute_script("return document.body.scrollHeight")
                viewport_height = self.driver.execute_script("return window.innerHeight")
            except:
                page_height = 2000  # Fallback
                viewport_height = 800
            
            # Determine reading behavior type based on page characteristics
            reading_behavior = self._determine_landing_page_reading_behavior(page_height, viewport_height)
            self.logger.info(f"[BEHAVIOR] Using reading behavior: {reading_behavior}")
            
            # Variable phase timing (not fixed percentages)
            phase_timings = self._calculate_variable_phase_timings(total_time)
            
            # Phase 1: Initial page scan (variable timing)
            initial_scan_time = phase_timings['initial']
            self.logger.info(f"[SCAN] Initial page scan for {initial_scan_time:.1f} seconds")
            self._landing_page_initial_scan(initial_scan_time, page_height, viewport_height, reading_behavior)
            
            # Phase 2: Content exploration (variable timing)
            exploration_time = phase_timings['exploration']
            self.logger.info(f"[EXPLORE] Content exploration for {exploration_time:.1f} seconds")
            self._landing_page_content_exploration(exploration_time, page_height, viewport_height, reading_behavior)
            
            # Phase 3: Final review (variable timing)
            review_time = phase_timings['review']
            self.logger.info(f"[REVIEW] Final review for {review_time:.1f} seconds")
            self._landing_page_final_review(review_time, page_height, viewport_height, reading_behavior)
            
            self.logger.info("[SUCCESS] Natural landing page behavior completed")
            
        except Exception as e:
            self.logger.error(f"[ERROR] Error simulating landing page behavior: {e}")
            # Fallback to simple sleep with variation
            time.sleep(random.uniform(30, 60))
    
    def _determine_landing_page_reading_behavior(self, page_height, viewport_height):
        """Determine reading behavior based on page characteristics"""
        try:
            # Analyze page characteristics
            page_ratio = page_height / viewport_height if viewport_height > 0 else 1
            
            # Determine behavior based on page characteristics
            if page_ratio < 2:  # Short page
                behaviors = ["quick_scan", "focused_scan"]
            elif page_ratio < 4:  # Medium page
                behaviors = ["focused_scan", "careful_scan", "exploratory_scan"]
            else:  # Long page
                behaviors = ["careful_scan", "exploratory_scan", "comprehensive_scan"]
            
            # Add some randomness
            if random.random() < 0.2:  # 20% chance for different behavior
                behaviors = ["quick_scan", "focused_scan", "careful_scan", "exploratory_scan", "comprehensive_scan"]
            
            return random.choice(behaviors)
            
        except Exception as e:
            return "focused_scan"  # Default fallback
    
    def _calculate_variable_phase_timings(self, total_time):
        """Calculate variable phase timings instead of fixed percentages"""
        try:
            # Base percentages with variation
            initial_base = random.uniform(0.15, 0.25)  # 15-25% instead of fixed 20%
            exploration_base = random.uniform(0.55, 0.70)  # 55-70% instead of fixed 60%
            review_base = random.uniform(0.15, 0.25)  # 15-25% instead of fixed 20%
            
            # Normalize to ensure they sum to 1.0
            total_base = initial_base + exploration_base + review_base
            initial_base /= total_base
            exploration_base /= total_base
            review_base /= total_base
            
            return {
                'initial': total_time * initial_base,
                'exploration': total_time * exploration_base,
                'review': total_time * review_base
            }
            
        except Exception as e:
            # Fallback to original fixed percentages
            return {
                'initial': total_time * 0.2,
                'exploration': total_time * 0.6,
                'review': total_time * 0.2
            }
    
    def _landing_page_initial_scan(self, duration, page_height, viewport_height, reading_behavior="focused_scan"):
        """Initial scan of landing page content with enhanced randomness"""
        try:
            start_time = time.time()
            end_time = start_time + duration
            
            # Generate random scroll positions based on reading behavior
            scroll_positions = self._generate_random_scroll_positions(page_height, reading_behavior)
            
            # Randomize the order of scroll positions
            random.shuffle(scroll_positions)
            
            for position in scroll_positions:
                if time.time() >= end_time:
                    break
                    
                # Smooth scroll to position
                self.driver.execute_script(f"window.scrollTo({{top: {position}, behavior: 'smooth'}});")
                
                # Variable scroll delay based on reading behavior
                scroll_delay = self._get_reading_behavior_delay(reading_behavior, "scroll")
                time.sleep(scroll_delay)
                
                # Variable mouse movement probability and duration
                mouse_chance = self._get_mouse_movement_probability(reading_behavior)
                if random.random() < mouse_chance:
                    mouse_duration = self._get_mouse_movement_duration(reading_behavior)
                    self.mouse.random_mouse_movement(mouse_duration)
                
                # Variable reading pause based on behavior
                reading_pause = self._get_reading_behavior_delay(reading_behavior, "reading")
                time.sleep(reading_pause)
                
        except Exception as e:
            self.logger.warning(f"Error in initial scan: {e}")
    
    def _generate_random_scroll_positions(self, page_height, reading_behavior):
        """Generate random scroll positions based on reading behavior"""
        try:
            base_positions = [0, page_height * 0.3, page_height * 0.7, page_height * 0.5]
            
            # Add behavior-specific positions
            if reading_behavior == "quick_scan":
                # Fewer positions for quick scan
                positions = [0, page_height * 0.5]
            elif reading_behavior == "focused_scan":
                # Standard positions
                positions = base_positions
            elif reading_behavior == "careful_scan":
                # More positions for careful reading
                positions = [0, page_height * 0.2, page_height * 0.4, page_height * 0.6, page_height * 0.8]
            elif reading_behavior == "exploratory_scan":
                # Random positions for exploration
                positions = [0]
                for _ in range(random.randint(2, 4)):
                    positions.append(page_height * random.uniform(0.1, 0.9))
            else:  # comprehensive_scan
                # Many positions for comprehensive reading
                positions = [0, page_height * 0.15, page_height * 0.3, page_height * 0.45, 
                           page_height * 0.6, page_height * 0.75, page_height * 0.9]
            
            # Add some random variation to positions
            varied_positions = []
            for pos in positions:
                variation = page_height * random.uniform(-0.05, 0.05)  # ±5% variation
                varied_pos = max(0, min(page_height, pos + variation))
                varied_positions.append(varied_pos)
            
            return varied_positions
            
        except Exception as e:
            # Fallback to original positions
            return [0, page_height * 0.3, page_height * 0.7, page_height * 0.5]
    
    def _get_reading_behavior_delay(self, reading_behavior, delay_type):
        """Get delay based on reading behavior and delay type"""
        try:
            delays = {
                "quick_scan": {
                    "scroll": random.uniform(0.3, 0.8),
                    "reading": random.uniform(0.8, 1.5)
                },
                "focused_scan": {
                    "scroll": random.uniform(0.5, 1.2),
                    "reading": random.uniform(1.0, 2.0)
                },
                "careful_scan": {
                    "scroll": random.uniform(0.8, 1.5),
                    "reading": random.uniform(2.0, 4.0)
                },
                "exploratory_scan": {
                    "scroll": random.uniform(0.4, 1.0),
                    "reading": random.uniform(1.5, 3.0)
                },
                "comprehensive_scan": {
                    "scroll": random.uniform(0.6, 1.3),
                    "reading": random.uniform(2.5, 5.0)
                }
            }
            
            return delays.get(reading_behavior, delays["focused_scan"])[delay_type]
            
        except Exception as e:
            return random.uniform(0.5, 1.5)  # Default fallback
    
    def _get_mouse_movement_probability(self, reading_behavior):
        """Get mouse movement probability based on reading behavior and config"""
        # Check if mouse movement is enabled in config
        if not self.config.get('behavior.mouse_movement', True):
            return 0.0
            
        try:
            probabilities = {
                "quick_scan": random.uniform(0.3, 0.5),
                "focused_scan": random.uniform(0.5, 0.7),
                "careful_scan": random.uniform(0.6, 0.8),
                "exploratory_scan": random.uniform(0.4, 0.6),
                "comprehensive_scan": random.uniform(0.7, 0.9)
            }
            
            return probabilities.get(reading_behavior, 0.6)
            
        except Exception as e:
            return 0.6  # Default fallback
    
    def _get_mouse_movement_duration(self, reading_behavior):
        """Get mouse movement duration based on reading behavior and config"""
        # Check if mouse movement is enabled in config
        if not self.config.get('behavior.mouse_movement', True):
            return 0.0
            
        try:
            durations = {
                "quick_scan": random.uniform(0.2, 0.5),
                "focused_scan": random.uniform(0.3, 0.7),
                "careful_scan": random.uniform(0.5, 1.0),
                "exploratory_scan": random.uniform(0.4, 0.8),
                "comprehensive_scan": random.uniform(0.6, 1.2)
            }
            
            return durations.get(reading_behavior, 0.5)
            
        except Exception as e:
            return 0.5  # Default fallback
    
    def _landing_page_content_exploration(self, duration, page_height, viewport_height, reading_behavior="focused_scan"):
        """Detailed content exploration with behavior-based patterns"""
        try:
            start_time = time.time()
            end_time = start_time + duration
            
            # Determine exploration area based on reading behavior
            exploration_area = self._get_exploration_area(page_height, reading_behavior)
            max_scroll = exploration_area['max']
            min_scroll = exploration_area['min']
            
            # Get behavior-specific parameters
            scroll_frequency = self._get_scroll_frequency(reading_behavior)
            mouse_probability = self._get_mouse_movement_probability(reading_behavior)
            careful_reading_chance = self._get_careful_reading_chance(reading_behavior)
            
            iteration_count = 0
            while time.time() < end_time:
                iteration_count += 1
                
                # Variable scroll behavior based on reading type
                if reading_behavior == "quick_scan":
                    # Larger jumps for quick scanning
                    scroll_position = random.uniform(min_scroll, max_scroll)
                    self.driver.execute_script(f"window.scrollTo({{top: {scroll_position}, behavior: 'smooth'}});")
                elif reading_behavior == "careful_scan":
                    # Smaller, more precise scrolls
                    current_pos = self.driver.execute_script("return window.pageYOffset")
                    scroll_amount = random.randint(50, 150)
                    new_pos = min(max_scroll, max(min_scroll, current_pos + scroll_amount))
                    self.driver.execute_script(f"window.scrollTo({{top: {new_pos}, behavior: 'smooth'}});")
                else:
                    # Standard random scroll
                    scroll_position = random.uniform(min_scroll, max_scroll)
                    self.driver.execute_script(f"window.scrollTo({{top: {scroll_position}, behavior: 'smooth'}});")
                
                # Variable reading pause based on behavior
                reading_pause = self._get_reading_behavior_delay(reading_behavior, "reading")
                time.sleep(reading_pause)
                
                # Variable mouse movement
                if random.random() < mouse_probability:
                    mouse_duration = self._get_mouse_movement_duration(reading_behavior)
                    self.mouse.random_mouse_movement(mouse_duration)
                
                # Occasional longer pause (like reading carefully)
                if random.random() < careful_reading_chance:
                    careful_reading = self._get_reading_behavior_delay(reading_behavior, "reading") * 1.5
                    time.sleep(careful_reading)
                
                # Small scroll adjustments (behavior-dependent)
                if random.random() < scroll_frequency:
                    adjustment_range = self._get_scroll_adjustment_range(reading_behavior)
                    small_scroll = random.randint(adjustment_range['min'], adjustment_range['max'])
                    self.driver.execute_script(f"window.scrollBy(0, {small_scroll});")
                    time.sleep(random.uniform(0.3, 0.8))
                
                # Add some natural variation in iteration timing
                iteration_delay = random.uniform(0.1, 0.3)
                time.sleep(iteration_delay)
                
        except Exception as e:
            self.logger.warning(f"Error in content exploration: {e}")
    
    def _get_exploration_area(self, page_height, reading_behavior):
        """Get exploration area based on reading behavior"""
        try:
            areas = {
                "quick_scan": {"min": 0, "max": page_height * 0.6},
                "focused_scan": {"min": 0, "max": page_height * 0.7},
                "careful_scan": {"min": 0, "max": page_height * 0.8},
                "exploratory_scan": {"min": 0, "max": page_height * 0.9},
                "comprehensive_scan": {"min": 0, "max": page_height * 0.95}
            }
            
            return areas.get(reading_behavior, areas["focused_scan"])
            
        except Exception as e:
            return {"min": 0, "max": page_height * 0.7}
    
    def _get_scroll_frequency(self, reading_behavior):
        """Get scroll frequency based on reading behavior"""
        try:
            frequencies = {
                "quick_scan": random.uniform(0.3, 0.5),
                "focused_scan": random.uniform(0.4, 0.6),
                "careful_scan": random.uniform(0.5, 0.7),
                "exploratory_scan": random.uniform(0.6, 0.8),
                "comprehensive_scan": random.uniform(0.7, 0.9)
            }
            
            return frequencies.get(reading_behavior, 0.5)
            
        except Exception as e:
            return 0.5
    
    def _get_careful_reading_chance(self, reading_behavior):
        """Get careful reading chance based on reading behavior"""
        try:
            chances = {
                "quick_scan": random.uniform(0.1, 0.2),
                "focused_scan": random.uniform(0.2, 0.3),
                "careful_scan": random.uniform(0.3, 0.5),
                "exploratory_scan": random.uniform(0.25, 0.4),
                "comprehensive_scan": random.uniform(0.4, 0.6)
            }
            
            return chances.get(reading_behavior, 0.3)
            
        except Exception as e:
            return 0.3
    
    def _get_scroll_adjustment_range(self, reading_behavior):
        """Get scroll adjustment range based on reading behavior"""
        try:
            ranges = {
                "quick_scan": {"min": -150, "max": 150},
                "focused_scan": {"min": -100, "max": 100},
                "careful_scan": {"min": -80, "max": 80},
                "exploratory_scan": {"min": -120, "max": 120},
                "comprehensive_scan": {"min": -60, "max": 60}
            }
            
            return ranges.get(reading_behavior, {"min": -100, "max": 100})
            
        except Exception as e:
            return {"min": -100, "max": 100}
    
    def _landing_page_final_review(self, duration, page_height, viewport_height, reading_behavior="focused_scan"):
        """Final review before leaving with behavior-based patterns"""
        try:
            start_time = time.time()
            end_time = start_time + duration
            
            # Determine final review behavior based on reading type
            if reading_behavior == "quick_scan":
                # Quick final check
                self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
                time.sleep(random.uniform(0.5, 1.0))
                
                # Brief final pause
                final_pause = random.uniform(1.0, 2.0)
                time.sleep(final_pause)
                
            elif reading_behavior == "careful_scan" or reading_behavior == "comprehensive_scan":
                # More thorough final review
                # Scroll to key positions for final check
                review_positions = [0, page_height * 0.3, page_height * 0.7]
                for position in review_positions:
                    if time.time() >= end_time:
                        break
                    self.driver.execute_script(f"window.scrollTo({{top: {position}, behavior: 'smooth'}});")
                    time.sleep(random.uniform(0.8, 1.5))
                
                # Final pause at top
                self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
                time.sleep(random.uniform(1.0, 2.0))
                
                # Longer final pause for careful reading
                final_pause = random.uniform(2.5, 5.0)
                time.sleep(final_pause)
                
            else:  # focused_scan, exploratory_scan
                # Standard final review
                self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
                time.sleep(random.uniform(1.0, 2.0))
                
                # Standard final pause
                final_pause = random.uniform(2.0, 4.0)
                time.sleep(final_pause)
            
            # Variable mouse movement based on behavior
            mouse_probability = self._get_mouse_movement_probability(reading_behavior)
            if random.random() < mouse_probability:
                mouse_duration = self._get_mouse_movement_duration(reading_behavior)
                self.mouse.random_mouse_movement(mouse_duration)
            
            # Variable pause before leaving
            leave_pause = self._get_reading_behavior_delay(reading_behavior, "reading") * 0.5
            time.sleep(leave_pause)
            
        except Exception as e:
            self.logger.warning(f"Error in final review: {e}")
    
    def _handle_vignette_ad_behavior(self):
        """Handle special behavior for vignette ads (popup/full-screen)"""
        try:
            self.logger.info("[VIGNETTE] Handling vignette ad behavior (popup/full-screen)")
            
            # Wait for vignette ad to fully load
            time.sleep(random.uniform(2.0, 4.0))
            
            # Check if vignette ad is still visible
            try:
                # Look for vignette-specific elements
                vignette_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    'ins[data-ad-format="vignette"], .vignette-ad, .fullscreen-ad, .popup-ad')
                
                if vignette_elements:
                    self.logger.info("[VIGNETTE] Vignette ad detected, simulating full-screen interaction")
                    
                    # Simulate viewing the full-screen ad
                    viewing_time = random.uniform(8.0, 15.0)
                    self.logger.info(f"[VIGNETTE] Viewing vignette ad for {viewing_time:.1f} seconds")
                    
                    # Simulate natural viewing behavior
                    start_time = time.time()
                    end_time = start_time + viewing_time
                    
                    while time.time() < end_time:
                        # Random mouse movements within the ad
                        if random.random() < 0.3:
                            self.mouse.random_mouse_movement(random.uniform(0.5, 1.5))
                        
                        # Brief pauses
                        time.sleep(random.uniform(1.0, 3.0))
                    
                    # Simulate closing or continuing from vignette
                    if random.random() < 0.7:  # 70% chance to continue
                        self.logger.info("[VIGNETTE] Continuing from vignette ad")
                        # Vignette ads typically auto-advance or have close buttons
                        time.sleep(random.uniform(1.0, 2.0))
                    else:
                        self.logger.info("[VIGNETTE] Simulating vignette ad close")
                        # Look for close button or simulate close action
                        try:
                            close_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                                '.vignette-close, .popup-close, .ad-close, [data-close], .close-button')
                            if close_buttons:
                                close_buttons[0].click()
                                time.sleep(random.uniform(1.0, 2.0))
                        except:
                            # If no close button found, just wait
                            time.sleep(random.uniform(2.0, 4.0))
                else:
                    self.logger.info("[VIGNETTE] No vignette ad elements found, standard behavior")
                    
            except Exception as e:
                self.logger.warning(f"[VIGNETTE] Error handling vignette ad: {e}")
                
        except Exception as e:
            self.logger.warning(f"[VIGNETTE] Error in vignette ad behavior: {e}")
    
    def _handle_discovery_ad_behavior(self):
        """Handle discovery ad popup behavior - popup from right (desktop) or bottom (mobile)"""
        try:
            self.logger.info("[DISCOVERY] Handling Discovery ad popup behavior...")
            
            # Wait for discovery popup to appear
            time.sleep(random.uniform(1, 3))
            
            # Detect device type (desktop vs mobile)
            is_mobile = self._detect_mobile_device()
            
            # Check for discovery popup based on device type
            popup_found = False
            if is_mobile:
                # Mobile: popup from bottom - actual selectors
                popup_selectors = [
                    '#hd-drawer-container.hd-revealed',
                    '#hd-drawer',
                    '#hd-content-container',
                    '#prose-iframe',
                    'iframe[src*="gstatic.com/prose"]',
                    '.gsc-results-wrapper-visible',
                    '.gsc-adBlock',
                    'iframe[name*="master-2"]',
                    'iframe[id*="master-2"]'
                ]
            else:
                # Desktop: popup from right - actual selectors
                popup_selectors = [
                    '#hd-drawer-container.hd-revealed',
                    '#hd-drawer',
                    '#hd-content-container',
                    '#prose-iframe',
                    'iframe[src*="gstatic.com/prose"]',
                    '.gsc-results-wrapper-visible',
                    '.gsc-adBlock',
                    'iframe[name*="master-2"]',
                    'iframe[id*="master-2"]'
                ]
            
            # Check for popup
            for selector in popup_selectors:
                try:
                    popup = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if popup.is_displayed():
                        popup_found = True
                        self.logger.info(f"[DISCOVERY] Found popup with selector: {selector}")
                        break
                except:
                    continue
            
            if popup_found:
                # Natural behavior in discovery popup
                self._simulate_discovery_popup_interaction(is_mobile)
            else:
                # No popup found, continue normal behavior
                self.logger.info("[DISCOVERY] No popup found, continuing normal behavior")
                
        except Exception as e:
            self.logger.warning(f"[DISCOVERY] Error handling discovery popup: {e}")
    
    def _detect_mobile_device(self):
        """Detect if device is mobile based on screen size and user agent"""
        try:
            # Get screen size
            screen_size = self.driver.get_window_size()
            width = screen_size['width']
            height = screen_size['height']
            
            # Check if mobile based on screen size
            is_mobile_size = width < 768 or height < 768
            
            # Check user agent
            user_agent = self.driver.execute_script("return navigator.userAgent;")
            is_mobile_ua = any(mobile in user_agent.lower() for mobile in ['mobile', 'android', 'iphone', 'ipad'])
            
            return is_mobile_size or is_mobile_ua
            
        except:
            return False
    
    def _simulate_discovery_popup_interaction(self, is_mobile):
        """Simulate natural interaction with discovery popup"""
        try:
            self.logger.info(f"[DISCOVERY] Simulating popup interaction (mobile: {is_mobile})")
            
            # Wait for popup to fully load
            time.sleep(random.uniform(1, 3))
            
            # Natural reading behavior in popup
            reading_time = random.uniform(3, 8)  # 3-8 seconds reading
            self.logger.info(f"[DISCOVERY] Reading popup content for {reading_time:.1f}s")
            time.sleep(reading_time)
            
            # Look for clickable ads in popup - actual selectors
            ad_selectors = [
                # Discovery popup drawer ads
                '#hd-drawer-container iframe',
                '#prose-iframe',
                'iframe[src*="gstatic.com/prose"]',
                
                # Discovery popup ads list
                '.gsc-adBlock iframe',
                'iframe[name*="master-2"]',
                'iframe[id*="master-2"]',
                'iframe[name*="master-a-2"]',
                'iframe[name*="master-b-2"]',
                'iframe[src*="syndicatedsearch.goog/cse_v2/ads"]',
                'iframe[src*="syndicatedsearch.goog/afs/ads/i/iframe.html"]',
                
                # Generic discovery ad selectors
                '.discovery-ad-item',
                '.discovery-ad-card',
                '.discovery-ad-link',
                '.discovery-ad-content',
                '[data-discovery-ad]',
                '.discovery-popup .ad-item',
                '.discovery-popup .ad-card',
                '.discovery-popup .ad-link'
            ]
            
            clickable_ads = []
            for selector in ad_selectors:
                try:
                    ads = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for ad in ads:
                        if ad.is_displayed() and ad.is_enabled():
                            clickable_ads.append(ad)
                except:
                    continue
            
            if clickable_ads:
                self.logger.info(f"[DISCOVERY] Found {len(clickable_ads)} clickable ads in popup")
                
                # Natural behavior: scroll through ads
                if is_mobile:
                    # Mobile: scroll vertically
                    self._simulate_mobile_discovery_scroll(clickable_ads)
                else:
                    # Desktop: scroll horizontally
                    self._simulate_desktop_discovery_scroll(clickable_ads)
                
                # Randomly click on one of the ads
                if random.random() < 0.6:  # 60% chance to click an ad
                    selected_ad = random.choice(clickable_ads)
                    self._click_discovery_popup_ad(selected_ad)
                else:
                    self.logger.info("[DISCOVERY] Deciding not to click any ad (natural behavior)")
            else:
                self.logger.info("[DISCOVERY] No clickable ads found in popup")
            
            # Natural exit behavior
            self._simulate_discovery_popup_exit(is_mobile)
            
        except Exception as e:
            self.logger.warning(f"[DISCOVERY] Error in popup interaction: {e}")
    
    def _simulate_mobile_discovery_scroll(self, ads):
        """Simulate mobile discovery popup scrolling (vertical)"""
        try:
            self.logger.info("[DISCOVERY] Simulating mobile discovery scroll")
            
            # Scroll through ads vertically
            for i, ad in enumerate(ads[:3]):  # Limit to first 3 ads
                # Scroll to ad
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ad)
                time.sleep(random.uniform(0.5, 1.5))
                
                # Natural reading pause
                reading_pause = random.uniform(1, 3)
                time.sleep(reading_pause)
                
                # Random hover behavior
                if random.random() < 0.3:  # 30% chance
                    self.mouse.move_to_element(ad)
                    time.sleep(random.uniform(0.5, 1.0))
                
        except Exception as e:
            self.logger.warning(f"[DISCOVERY] Error in mobile scroll: {e}")
    
    def _simulate_desktop_discovery_scroll(self, ads):
        """Simulate desktop discovery popup scrolling (horizontal)"""
        try:
            self.logger.info("[DISCOVERY] Simulating desktop discovery scroll")
            
            # Scroll through ads horizontally
            for i, ad in enumerate(ads[:4]):  # Limit to first 4 ads
                # Scroll to ad
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ad)
                time.sleep(random.uniform(0.5, 1.5))
                
                # Natural reading pause
                reading_pause = random.uniform(1, 3)
                time.sleep(reading_pause)
                
                # Random hover behavior
                if random.random() < 0.4:  # 40% chance
                    self.mouse.move_to_element(ad)
                    time.sleep(random.uniform(0.5, 1.0))
                
        except Exception as e:
            self.logger.warning(f"[DISCOVERY] Error in desktop scroll: {e}")
    
    def _click_discovery_popup_ad(self, ad_element):
        """Click on an ad within discovery popup"""
        try:
            self.logger.info("[DISCOVERY] Clicking on popup ad")
            
            # Natural hesitation before clicking
            hesitation = random.uniform(0.5, 2.0)
            time.sleep(hesitation)
            
            # Check if ad is inside iframe
            if self._is_element_in_iframe(ad_element):
                self.logger.info("[DISCOVERY] Ad is inside iframe, switching context")
                self._click_ad_in_iframe(ad_element)
            else:
                # Human-like mouse movement to ad
                if self.mouse.move_to_element(ad_element):
                    # Click the ad
                    ad_element.click()
                    self.logger.info("[DISCOVERY] Successfully clicked popup ad")
                    
                    # Handle landing page
                    self._handle_ad_landing_page()
                else:
                    self.logger.warning("[DISCOVERY] Failed to move mouse to popup ad")
                
        except Exception as e:
            self.logger.warning(f"[DISCOVERY] Error clicking popup ad: {e}")
    
    def _simulate_discovery_popup_exit(self, is_mobile):
        """Simulate natural exit from discovery popup"""
        try:
            self.logger.info("[DISCOVERY] Simulating popup exit")
            
            # Natural exit behavior
            exit_delay = random.uniform(2, 5)  # 2-5 seconds
            time.sleep(exit_delay)
            
            # Look for close button or exit mechanism - actual selectors
            close_selectors = [
                # Discovery popup drawer close buttons
                '#hd-close-button',
                '#hd-back-arrow-button',
                '.hd-control-button',
                '#hd-control-bar button',
                
                # Generic close selectors
                '.discovery-popup-close',
                '.discovery-popup-exit',
                '.discovery-popup-dismiss',
                '[data-discovery-close]',
                '.discovery-popup .close',
                '.discovery-popup .exit',
                '.discovery-popup .dismiss'
            ]
            
            close_button_found = False
            for selector in close_selectors:
                try:
                    close_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if close_btn.is_displayed():
                        close_btn.click()
                        close_button_found = True
                        self.logger.info("[DISCOVERY] Clicked close button")
                        break
                except:
                    continue
            
            if not close_button_found:
                # If no close button, simulate natural exit (click outside or ESC)
                if random.random() < 0.5:  # 50% chance
                    # Click outside popup
                    self.driver.execute_script("document.body.click();")
                else:
                    # Press ESC key
                    from selenium.webdriver.common.keys import Keys
                    self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                
                self.logger.info("[DISCOVERY] Exited popup naturally")
            
            # Wait for popup to close
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            self.logger.warning(f"[DISCOVERY] Error in popup exit: {e}")
    
    def _handle_afs_ad_behavior(self):
        """Handle AFS ad popup behavior - similar to Discovery but for search results"""
        try:
            self.logger.info("[AFS] Handling AFS ad popup behavior...")
            
            # Wait for AFS popup to appear
            time.sleep(random.uniform(1, 3))
            
            # Detect device type (desktop vs mobile)
            is_mobile = self._detect_mobile_device()
            
            # Check for AFS popup based on device type
            popup_found = False
            if is_mobile:
                # Mobile: popup from bottom - ACTUAL AFS selectors
                popup_selectors = [
                    '#hd-drawer-container.hd-revealed',
                    '#hd-drawer',
                    '#hd-content-container',
                    'iframe[srcdoc*="gda-search-term"]',
                    'iframe[srcdoc*="display-slot-container"]',
                    'iframe[srcdoc*="adsbygoogle"]',
                    '#gda-search-term',
                    '#display-slot-container',
                    '#display-slot'
                ]
            else:
                # Desktop: popup from right - ACTUAL AFS selectors
                popup_selectors = [
                    '#hd-drawer-container.hd-revealed',
                    '#hd-drawer',
                    '#hd-content-container',
                    'iframe[srcdoc*="gda-search-term"]',
                    'iframe[srcdoc*="display-slot-container"]',
                    'iframe[srcdoc*="adsbygoogle"]',
                    '#gda-search-term',
                    '#display-slot-container',
                    '#display-slot'
                ]
            
            # Check for popup
            for selector in popup_selectors:
                try:
                    popup = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if popup.is_displayed():
                        popup_found = True
                        self.logger.info(f"[AFS] Found popup with selector: {selector}")
                        break
                except:
                    continue
            
            if popup_found:
                # Natural behavior in AFS popup
                self._simulate_afs_popup_interaction(is_mobile)
            else:
                # No popup found, continue normal behavior
                self.logger.info("[AFS] No popup found, continuing normal behavior")
                
        except Exception as e:
            self.logger.warning(f"[AFS] Error handling AFS popup: {e}")
    
    def _simulate_afs_popup_interaction(self, is_mobile):
        """Simulate natural interaction with AFS popup"""
        try:
            self.logger.info(f"[AFS] Simulating popup interaction (mobile: {is_mobile})")
            
            # Wait for popup to fully load
            time.sleep(random.uniform(1, 3))
            
            # Natural reading behavior in popup
            reading_time = random.uniform(3, 8)  # 3-8 seconds reading
            self.logger.info(f"[AFS] Reading popup content for {reading_time:.1f}s")
            time.sleep(reading_time)
            
            # Look for clickable ads in popup - ACTUAL AFS selectors
            ad_selectors = [
                # AFS Side Rail (In Page) - ACTUAL STRUCTURE
                '#google-anno-sa',
                '.google-anno-sa-qtx',
                '.google-anno-skip',
                '#gda',
                '[data-google-vignette="false"]',
                '[data-google-interstitial="false"]',
                '[aria-label*="Buka opsi belanja"]',
                '[role="link"][tabindex="0"]',
                
                # AFS Popup Drawer - ACTUAL STRUCTURE
                '#hd-drawer-container iframe',
                'iframe[srcdoc*="gda-search-term"]',
                'iframe[srcdoc*="display-slot-container"]',
                'iframe[srcdoc*="adsbygoogle"]',
                
                # AFS Search Results - ACTUAL STRUCTURE
                '#gda-search-term',
                '#display-slot-container',
                '#display-slot',
                'ins[data-ad-intent-query]',
                'ins[data-ad-intent-qetid]',
                'ins[data-ad-intents-format]',
                'ins[data-ad-intent-rs-token]',
                'ins[data-query-targeted="true"]',
                'ins[data-ad-client*="ca-pub-"]',
                
                # Generic AFS ad selectors
                '.search-ad-item',
                '.search-ad-card',
                '.search-ad-link',
                '.search-ad-content',
                '[data-search-ad]',
                '.afs-popup .ad-item',
                '.afs-popup .ad-card',
                '.afs-popup .ad-link'
            ]
            
            clickable_ads = []
            for selector in ad_selectors:
                try:
                    ads = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for ad in ads:
                        if ad.is_displayed() and ad.is_enabled():
                            clickable_ads.append(ad)
                except:
                    continue
            
            if clickable_ads:
                self.logger.info(f"[AFS] Found {len(clickable_ads)} clickable ads in popup")
                
                # Natural behavior: scroll through ads
                if is_mobile:
                    # Mobile: scroll vertically
                    self._simulate_mobile_afs_scroll(clickable_ads)
                else:
                    # Desktop: scroll horizontally
                    self._simulate_desktop_afs_scroll(clickable_ads)
                
                # Randomly click on one of the ads
                if random.random() < 0.6:  # 60% chance to click an ad
                    selected_ad = random.choice(clickable_ads)
                    self._click_afs_popup_ad(selected_ad)
                else:
                    self.logger.info("[AFS] Deciding not to click any ad (natural behavior)")
            else:
                self.logger.info("[AFS] No clickable ads found in popup")
            
            # Natural exit behavior
            self._simulate_afs_popup_exit(is_mobile)
            
        except Exception as e:
            self.logger.warning(f"[AFS] Error in popup interaction: {e}")
    
    def _simulate_mobile_afs_scroll(self, ads):
        """Simulate mobile AFS popup scrolling (vertical)"""
        try:
            self.logger.info("[AFS] Simulating mobile AFS scroll")
            
            # Scroll through ads vertically
            for i, ad in enumerate(ads[:3]):  # Limit to first 3 ads
                # Scroll to ad
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ad)
                time.sleep(random.uniform(0.5, 1.5))
                
                # Natural reading pause
                reading_pause = random.uniform(1, 3)
                time.sleep(reading_pause)
                
                # Random hover behavior
                if random.random() < 0.3:  # 30% chance
                    self.mouse.move_to_element(ad)
                    time.sleep(random.uniform(0.5, 1.0))
                
        except Exception as e:
            self.logger.warning(f"[AFS] Error in mobile scroll: {e}")
    
    def _simulate_desktop_afs_scroll(self, ads):
        """Simulate desktop AFS popup scrolling (horizontal)"""
        try:
            self.logger.info("[AFS] Simulating desktop AFS scroll")
            
            # Scroll through ads horizontally
            for i, ad in enumerate(ads[:4]):  # Limit to first 4 ads
                # Scroll to ad
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ad)
                time.sleep(random.uniform(0.5, 1.5))
                
                # Natural reading pause
                reading_pause = random.uniform(1, 3)
                time.sleep(reading_pause)
                
                # Random hover behavior
                if random.random() < 0.4:  # 40% chance
                    self.mouse.move_to_element(ad)
                    time.sleep(random.uniform(0.5, 1.0))
                
        except Exception as e:
            self.logger.warning(f"[AFS] Error in desktop scroll: {e}")
    
    def _click_afs_popup_ad(self, ad_element):
        """Click an ad inside the AFS popup"""
        try:
            self.logger.info("[AFS] Clicking ad in popup")
            
            # Check if ad is inside iframe
            if self._is_element_in_iframe(ad_element):
                self.logger.info("[AFS] Ad is inside iframe, switching context")
                self._click_ad_in_iframe(ad_element)
            else:
                # Scroll to ad
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ad_element)
                time.sleep(random.uniform(0.5, 1.0))
                
                # Human-like delay before clicking
                pre_click_delay = random.uniform(0.5, 2.0)
                time.sleep(pre_click_delay)
                
                # Use mouse simulator for human-like clicking
                if self.mouse.move_to_element(ad_element):
                    ad_element.click()
                    self.logger.info("[AFS] Successfully clicked ad in popup")
                    
                    # Post-click delay
                    post_click_delay = random.uniform(1, 3)
                    time.sleep(post_click_delay)
                else:
                    self.logger.warning("[AFS] Failed to move mouse to ad element")
                
        except Exception as e:
            self.logger.warning(f"[AFS] Error clicking ad in popup: {e}")
    
    def _simulate_afs_popup_exit(self, is_mobile):
        """Simulate natural exit from AFS popup"""
        try:
            self.logger.info("[AFS] Simulating popup exit")
            
            # Natural exit behavior
            exit_delay = random.uniform(2, 5)  # 2-5 seconds
            time.sleep(exit_delay)
            
            # Look for close button or exit mechanism - ACTUAL AFS selectors
            close_selectors = [
                # AFS Side Rail Close Button - ACTUAL STRUCTURE
                '#gda svg[role="button"]',
                '[aria-label*="Tutup anchor belanja"]',
                '[role="button"][aria-label*="Tutup"]',
                '#gda svg',
                
                # AFS Popup Drawer Close Buttons - ACTUAL STRUCTURE
                '#hd-close-button',
                '#hd-back-arrow-button',
                '.hd-control-button',
                '#hd-control-bar button',
                
                # Generic close selectors
                '.afs-popup-close',
                '.afs-popup-exit',
                '.afs-popup-dismiss',
                '[data-afs-close]',
                '.afs-popup .close',
                '.afs-popup .exit',
                '.afs-popup .dismiss'
            ]
            
            close_button_found = False
            for selector in close_selectors:
                try:
                    close_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if close_btn.is_displayed():
                        close_btn.click()
                        close_button_found = True
                        self.logger.info("[AFS] Clicked close button")
                        break
                except:
                    continue
            
            if not close_button_found:
                # If no close button, simulate natural exit (click outside or ESC)
                if random.random() < 0.5:  # 50% chance
                    # Click outside popup
                    self.driver.execute_script("document.body.click();")
                else:
                    # Press ESC key
                    from selenium.webdriver.common.keys import Keys
                    self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                
                self.logger.info("[AFS] Exited popup naturally")
            
            # Wait for popup to close
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            self.logger.warning(f"[AFS] Error in popup exit: {e}")
    
    def _is_element_in_iframe(self, element):
        """Check if element is inside an iframe"""
        try:
            # Check if element has iframe ancestor
            iframe = element.find_element(By.XPATH, "./ancestor::iframe")
            return iframe is not None
        except:
            return False
    
    def _click_ad_in_iframe(self, ad_element):
        """Click ad inside iframe drawer content"""
        try:
            self.logger.info("[DRAWER] Clicking ad inside iframe")
            
            # Get iframe containing the ad
            iframe = ad_element.find_element(By.XPATH, "./ancestor::iframe")
            if iframe:
                # Switch to iframe
                self.driver.switch_to.frame(iframe)
                self.logger.info("[DRAWER] Switched to iframe")
                
                # Wait for iframe content to load
                time.sleep(random.uniform(1, 2))
                
                # Find ad elements inside iframe
                iframe_ad_selectors = [
                    # Discovery iframe ads
                    'ins[data-ad-format="discovery"]',
                    'ins[data-ad-format*="discovery"]',
                    '.adsbygoogle[data-ad-format="discovery"]',
                    '[data-ad-format="discovery"]',
                    '.discovery-ad',
                    '.feed-ad',
                    '.content-ad',
                    
                    # AFS iframe ads
                    'ins[data-ad-intent-query]',
                    'ins[data-ad-intent-qetid]',
                    'ins[data-ad-intents-format]',
                    'ins[data-query-targeted="true"]',
                    '#display-slot',
                    '#display-slot-container',
                    'ins[data-ad-client*="ca-pub-"]',
                    
                    # Generic iframe ads
                    'ins[data-ad-format]',
                    '.adsbygoogle',
                    '[data-ad-client]',
                    'a[href*="googleadservices.com"]',
                    'a[href*="googlesyndication.com"]'
                ]
                
                clickable_ads = []
                for selector in iframe_ad_selectors:
                    try:
                        ads = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for ad in ads:
                            if ad.is_displayed() and ad.is_enabled():
                                clickable_ads.append(ad)
                    except:
                        continue
                
                if clickable_ads:
                    self.logger.info(f"[DRAWER] Found {len(clickable_ads)} clickable ads in iframe")
                    
                    # Randomly select an ad to click
                    selected_ad = random.choice(clickable_ads)
                    
                    # Scroll to ad
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selected_ad)
                    time.sleep(random.uniform(0.5, 1.0))
                    
                    # Human-like delay before clicking
                    pre_click_delay = random.uniform(0.5, 2.0)
                    time.sleep(pre_click_delay)
                    
                    # Click the ad
                    selected_ad.click()
                    self.logger.info("[DRAWER] Successfully clicked ad in iframe")
                    
                    # Post-click delay
                    post_click_delay = random.uniform(1, 3)
                    time.sleep(post_click_delay)
                else:
                    self.logger.info("[DRAWER] No clickable ads found in iframe")
                
                # Switch back to main content
                self.driver.switch_to.default_content()
                self.logger.info("[DRAWER] Switched back to main content")
                
        except Exception as e:
            self.logger.warning(f"[DRAWER] Error clicking ad in iframe: {e}")
            # Ensure we switch back to main content
            try:
                self.driver.switch_to.default_content()
            except:
                pass
    
    def get_click_statistics(self):
        """Get ad clicking statistics"""
        current_time = time.time()
        
        # Calculate recent click statistics (last hour)
        recent_clicks = [click for click in self.click_history 
                        if current_time - click['timestamp'] < 3600]  # Last hour
        
        # Calculate clicks in rate limiting window
        rate_limit_window = self.config.get('ad_clicking.rate_limit_window', 1200)  # Default 20 minutes
        rate_limit_clicks = [click for click in self.click_history 
                            if current_time - click['timestamp'] < rate_limit_window]
        
        return {
            'total_clicks': len(self.click_history),
            'recent_clicks': len(recent_clicks),
            'rate_limit_clicks': len(rate_limit_clicks),
            'rate_limit_remaining': max(0, self.config.get('ad_clicking.max_clicks_per_window', 3) - len(rate_limit_clicks)),
            'click_rate': len(recent_clicks) / 60,  # Clicks per minute
            'average_click_interval': self._calculate_average_interval(),
            'ad_types_clicked': self._get_clicked_ad_types()
        }
    
    def _calculate_average_interval(self):
        """Calculate average interval between clicks"""
        if len(self.click_history) < 2:
            return 0
        
        intervals = []
        for i in range(1, len(self.click_history)):
            interval = self.click_history[i]['timestamp'] - self.click_history[i-1]['timestamp']
            intervals.append(interval)
        
        return sum(intervals) / len(intervals) if intervals else 0
    
    def _get_clicked_ad_types(self):
        """Get count of clicked ad types"""
        ad_types = {}
        for click in self.click_history:
            ad_type = click['ad_type']
            ad_types[ad_type] = ad_types.get(ad_type, 0) + 1
        
        return ad_types


class HumanLikeScroller:
    """Advanced human-like scrolling system"""
    
    def __init__(self, driver, timing_system, mouse_simulator):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.scroll_history = []
        self.reading_sessions = []
        self.logger = logging.getLogger('advanced_website_robot')
    
    def smooth_scroll_to_position(self, target_position, duration=None):
        # Use random duration for more natural behavior
        if duration is None:
            duration = random.uniform(0.3, 12.0)  # Variasi duration 0.3-12 detik (extreme)
        """Natural scroll to specific position with human-like imperfections"""
        try:
            current_position = self.driver.execute_script("return window.pageYOffset")
            distance = target_position - current_position
            
            if abs(distance) < 50:  # Already close enough
                return True
            
            # More natural step calculation with extreme variation
            base_steps = max(15, min(800, int(abs(distance) / 8)))  # Extreme variation in steps
            steps = base_steps + random.randint(-80, 150)  # Add extreme variation
            steps = max(5, min(1200, steps))  # Ensure reasonable range dengan variasi extreme
            step_size = distance / steps
            step_duration = duration / steps
            
            # Add natural scroll variations
            scroll_variations = []
            for step in range(steps):
                # Add natural micro-variations
                variation = random.uniform(0.8, 1.2)
                scroll_variations.append(variation)
            
            for step in range(steps):
                # Apply natural variation to scroll
                variation = scroll_variations[step] if step < len(scroll_variations) else 1.0
                new_position = current_position + (step_size * (step + 1) * variation)
                
                # Add natural scroll jitter
                jitter = random.uniform(-2, 2)
                new_position += jitter
                
                self.driver.execute_script(f"window.scrollTo(0, {new_position});")
                
                # More natural delay variations with extreme randomness
                base_delay = step_duration * random.uniform(0.1, 8.0)  # Extreme variation
                
                # Add natural hesitation with extreme variation
                hesitation_chance = random.uniform(0.15, 0.60)  # Extreme variasi hesitation chance
                if random.random() < hesitation_chance:
                    base_delay += random.uniform(0.1, 8.0)  # Extreme variasi hesitation duration
                
                # Add natural pause chance
                pause_chance = random.uniform(0.08, 0.40)  # 8-40% chance of pause
                if random.random() < pause_chance:
                    base_delay += random.uniform(0.3, 6.0)  # Pause duration
                
                # Add natural acceleration/deceleration
                accel_factor = random.uniform(0.3, 3.0)  # Acceleration factor
                base_delay *= accel_factor
                
                # Add natural rhythm variation
                rhythm_factor = random.uniform(0.4, 2.5)  # Rhythm factor
                base_delay *= rhythm_factor
                
                # Add natural speed variation
                speed_factor = random.uniform(0.2, 4.0)  # Speed factor
                base_delay *= speed_factor
                
                time.sleep(base_delay)
                
                # Natural reading pauses with realistic variation - CONFIGURATION-BASED
                reading_pause_chance = random.uniform(0.20, 0.70)  # Realistic reading pause chance
                if random.random() < reading_pause_chance:
                    # Use micro-pause configuration for realistic variation
                    micro_pause_min = self.config.get('reading.pause_timing.micro_pause_min', 0.2)
                    micro_pause_max = self.config.get('reading.pause_timing.micro_pause_max', 1.0)
                    reading_pause = random.uniform(micro_pause_min, micro_pause_max)
                    time.sleep(reading_pause)
                
                # Add natural distraction pauses - CONFIGURATION-BASED
                distraction_chance = self.config.get('reading.pause_timing.distraction_chance', 0.15)
                if random.random() < distraction_chance:
                    distraction_pause_min = self.config.get('reading.pause_timing.distraction_pause_min', 3.0)
                    distraction_pause_max = self.config.get('reading.pause_timing.distraction_pause_max', 8.0)
                    distraction_pause = random.uniform(distraction_pause_min, distraction_pause_max)
                    time.sleep(distraction_pause)
                
                # Add natural thinking pauses - UNIFIED THINKING BEHAVIOR
                if self._simulate_thinking_behavior():
                    pass  # Thinking behavior already executed in _simulate_thinking_behavior
                
                # Add natural comprehension pauses - CONFIGURATION-BASED
                comprehension_chance = self.config.get('reading.pause_timing.comprehension_chance', 0.20)
                if random.random() < comprehension_chance:
                    comprehension_pause_min = self.config.get('reading.pause_timing.comprehension_pause_min', 2.0)
                    comprehension_pause_max = self.config.get('reading.pause_timing.comprehension_pause_max', 6.0)
                    comprehension_pause = random.uniform(comprehension_pause_min, comprehension_pause_max)
                    time.sleep(comprehension_pause)
                
                # Add natural interest pauses
                interest_chance = random.uniform(0.02, 0.15)  # 2-15% chance of interest
                if random.random() < interest_chance:
                    interest_pause = random.uniform(3.0, 18.0)  # Interest pause
                    time.sleep(interest_pause)
                
                # Add natural confusion pauses
                confusion_chance = random.uniform(0.01, 0.10)  # 1-10% chance of confusion
                if random.random() < confusion_chance:
                    confusion_pause = random.uniform(4.0, 20.0)  # Confusion pause
                    time.sleep(confusion_pause)
                
                # Add natural excitement pauses
                excitement_chance = random.uniform(0.01, 0.08)  # 1-8% chance of excitement
                if random.random() < excitement_chance:
                    excitement_pause = random.uniform(1.0, 8.0)  # Excitement pause
                    time.sleep(excitement_pause)
                
                # Add natural scroll-back behavior (like human re-reading)
                if random.random() < 0.18:  # 18% chance of scroll-back
                    scroll_back = random.randint(30, 200)
                    back_position = max(0, new_position - scroll_back)
                    self.driver.execute_script(f"window.scrollTo(0, {back_position});")
                    time.sleep(random.uniform(0.3, 4.0))
                    # Continue from back position
                    current_position = back_position
                
                # Add natural scroll-forward behavior (like human skipping)
                if random.random() < 0.08:  # 8% chance of scroll-forward
                    scroll_forward = random.randint(20, 100)
                    forward_position = min(document.body.scrollHeight, new_position + scroll_forward)
                    self.driver.execute_script(f"window.scrollTo(0, {forward_position});")
                    time.sleep(random.uniform(0.2, 2.0))
                    # Continue from forward position
                    current_position = forward_position
                
                # Add natural scroll-jump behavior (like human jumping to sections)
                if random.random() < 0.05:  # 5% chance of scroll-jump
                    jump_distance = random.randint(100, 500)
                    jump_position = max(0, min(document.body.scrollHeight, new_position + jump_distance))
                    self.driver.execute_script(f"window.scrollTo(0, {jump_position});")
                    time.sleep(random.uniform(1.0, 5.0))
                    # Continue from jump position
                    current_position = jump_position
            
            return True
            
        except Exception as e:
            return False
    
    def reading_behavior_scroll(self, content_type="article"):
        """Simulate reading behavior with natural scrolling"""
        try:
            # Get page dimensions
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            
            # Reading behavior patterns - much longer pauses for better comprehension
            reading_patterns = {
                'article': {
                    'paragraph_scrolls': (3, 8),
                    'paragraph_pause': (8, 18),  # Much longer pauses
                    'section_pause': (12, 25),   # Much longer section pauses
                    're_read_chance': 0.35,      # Increased re-read chance
                    'mouse_tracking_chance': 0.5  # Increased mouse tracking
                },
                'news': {
                    'paragraph_scrolls': (2, 5),
                    'paragraph_pause': (6, 15),  # Much longer pauses
                    'section_pause': (10, 20),   # Much longer section pauses
                    're_read_chance': 0.25,      # Increased re-read chance
                    'mouse_tracking_chance': 0.4  # Increased mouse tracking
                },
                'blog': {
                    'paragraph_scrolls': (4, 10),
                    'paragraph_pause': (10, 20), # Much longer pauses
                    'section_pause': (15, 30),   # Much longer section pauses
                    're_read_chance': 0.45,      # Increased re-read chance
                    'mouse_tracking_chance': 0.6  # Increased mouse tracking
                }
            }
            
            pattern = reading_patterns.get(content_type, reading_patterns['article'])
            
            # Simulate reading paragraphs/sections
            num_paragraphs = random.randint(*pattern['paragraph_scrolls'])
            
            for paragraph in range(num_paragraphs):
                # Check if we're near the end
                current_scroll = self.driver.execute_script("return window.pageYOffset")
                remaining_height = page_height - current_scroll - viewport_height
                
                if remaining_height < 300:  # Near end, scroll up to re-read
                    scroll_up = random.randint(200, 500)
                    self.smooth_scroll_to_position(current_scroll - scroll_up, 1.5)
                    self.logger.info("Scrolled up to re-read (near end)")
                else:
                    # Normal paragraph reading scroll
                    scroll_amount = random.randint(200, 600)
                    
                    # Add variation based on content type
                    if content_type == 'article':
                        # Articles: more careful reading
                        scroll_amount = int(scroll_amount * random.uniform(0.7, 1.2))
                    elif content_type == 'news':
                        # News: faster reading
                        scroll_amount = int(scroll_amount * random.uniform(1.0, 1.5))
                    
                    new_position = current_scroll + scroll_amount
                    self.smooth_scroll_to_position(new_position, random.uniform(1.5, 3.0))
                
                # Reading pause (like actually reading the content) - much longer
                reading_pause = random.uniform(*pattern['paragraph_pause'])
                
                # Add mouse tracking (like following text with mouse) - longer duration
                if random.random() < pattern['mouse_tracking_chance']:
                    self.mouse.random_mouse_movement(random.uniform(1.0, 3.0))  # Longer mouse movement
                
                # Occasionally re-read (like humans do) - more frequent and longer
                if random.random() < pattern['re_read_chance']:
                    re_read_pause = random.uniform(5, 12)  # Much longer re-read pause
                    reading_pause += re_read_pause
                    self.logger.info(f"Re-reading pause: {re_read_pause:.1f}s")
                    
                    # Scroll up a bit to re-read
                    current_scroll = self.driver.execute_script("return window.pageYOffset")
                    re_read_scroll = random.randint(100, 300)
                    self.smooth_scroll_to_position(current_scroll - re_read_scroll, 2.0)  # Longer scroll duration
                
                time.sleep(reading_pause)
                
                # Section break pause (like finishing a section) - more frequent and longer
                if paragraph < num_paragraphs - 1 and random.random() < 0.5:  # Increased chance
                    section_pause = random.uniform(*pattern['section_pause'])
                    self.logger.info(f"Section break pause: {section_pause:.1f}s")
                    time.sleep(section_pause)
            
            # Final reading pause - much longer
            final_pause = random.uniform(8, 20)  # Much longer final pause
            self.logger.info(f"Final reading pause: {final_pause:.1f}s")
            time.sleep(final_pause)
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Error in reading behavior scroll: {e}")
            return False
    
    def quick_scan_scroll(self):
        """Quick scanning behavior (like skimming content)"""
        try:
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Quick scan: larger scrolls with shorter pauses
            scan_sections = random.randint(3, 6)
            section_height = page_height // scan_sections
            
            for section in range(scan_sections):
                target_position = section_height * (section + 1)
                
                # Quick scroll to section
                self.driver.execute_script(f"window.scrollTo(0, {target_position});")
                
                # Short scan pause
                scan_pause = random.uniform(0.5, 2.0)
                time.sleep(scan_pause)
                
                # Quick mouse movement (like scanning)
                if random.random() < 0.6:
                    self.mouse.random_mouse_movement(random.uniform(0.2, 0.8))
            
            return True
            
        except Exception as e:
            return False


class PostNavigator:
    """Previous/Next Post Navigation System for AdSense RPM Optimization"""
    def __init__(self, driver, timing_system, mouse_simulator, risk_monitor):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.risk_monitor = risk_monitor
        self.logger = logging.getLogger('advanced_website_robot')
        
        # Post navigation patterns
        self.previous_selectors = [
            'a[rel="prev"]', 'a[rel="previous"]', '.prev', '.previous', 
            '.post-nav-prev', '.navigation-prev', '.pagination-prev',
            'a:contains("Previous")', 'a:contains("Prev")', 'a:contains("[LEFT]")',
            '.nav-previous', '.entry-nav-prev', '.single-nav-prev'
        ]
        
        self.next_selectors = [
            'a[rel="next"]', 'a[rel="next"]', '.next', '.next-post',
            '.post-nav-next', '.navigation-next', '.pagination-next',
            'a:contains("Next")', 'a:contains("[RIGHT]")', 'a:contains("Continue")',
            '.nav-next', '.entry-nav-next', '.single-nav-next'
        ]
        
        # Related posts selectors
        self.related_selectors = [
            '.related-posts', '.similar-posts', '.more-posts', '.recommended-posts',
            '.post-recommendations', '.suggested-posts', '.you-might-like',
            '.related-articles', '.similar-articles', '.more-articles'
        ]
    
    def find_navigation_links(self):
        """Find previous, next, and related post links"""
        try:
            self.logger.info("[SCAN] Searching for post navigation links")
            
            navigation_links = {
                'previous': None,
                'next': None,
                'related': []
            }
            
            # Find previous post link
            for selector in self.previous_selectors:
                try:
                    if ':contains(' in selector:
                        # Handle text-based selectors
                        text = selector.split(':contains("')[1].split('")')[0]
                        elements = self.driver.find_elements("xpath", f"//a[contains(text(), '{text}')]")
                        if elements:
                            navigation_links['previous'] = elements[0]
                            self.logger.info(f"[SUCCESS] Found previous link: {text}")
                            break
                    else:
                        elements = self.driver.find_elements("css selector", selector)
                        if elements:
                            navigation_links['previous'] = elements[0]
                            self.logger.info(f"[SUCCESS] Found previous link with selector: {selector}")
                            break
                except Exception as e:
                    continue
            
            # Find next post link
            for selector in self.next_selectors:
                try:
                    if ':contains(' in selector:
                        # Handle text-based selectors
                        text = selector.split(':contains("')[1].split('")')[0]
                        elements = self.driver.find_elements("xpath", f"//a[contains(text(), '{text}')]")
                        if elements:
                            navigation_links['next'] = elements[0]
                            self.logger.info(f"[SUCCESS] Found next link: {text}")
                            break
                    else:
                        elements = self.driver.find_elements("css selector", selector)
                        if elements:
                            navigation_links['next'] = elements[0]
                            self.logger.info(f"[SUCCESS] Found next link with selector: {selector}")
                            break
                except Exception as e:
                    continue
            
            # Find related posts
            for selector in self.related_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        # Find links within related posts section
                        links = element.find_elements("css selector", "a")
                        for link in links[:3]:  # Limit to 3 related posts
                            href = link.get_attribute('href')
                            if href and href not in [l.get_attribute('href') for l in navigation_links['related']]:
                                navigation_links['related'].append(link)
                    if navigation_links['related']:
                        self.logger.info(f"[SUCCESS] Found {len(navigation_links['related'])} related posts")
                        break
                except Exception as e:
                    continue
            
            return navigation_links
            
        except Exception as e:
            self.logger.error(f"Error finding navigation links: {e}")
            return {'previous': None, 'next': None, 'related': []}
    
    def navigate_to_post(self, link_element, post_type="unknown"):
        """Navigate to a post link with natural behavior"""
        try:
            if not link_element:
                return False
                
            self.logger.info(f"[LINK] Navigating to {post_type} post")
            
            # Get link URL for tracking
            href = link_element.get_attribute('href')
            if href:
                self.logger.info(f"[LOCATION] Post URL: {href}")
            
            # Scroll to link
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link_element)
            time.sleep(1)
            
            # Move mouse to link
            self.mouse.move_to_element(link_element)
            time.sleep(0.5)
            
            # Click the link
            link_element.click()
            self.logger.info(f"[SUCCESS] Clicked {post_type} post link")
            
            # Wait for navigation
            time.sleep(3)
            
            # Verify navigation success
            current_url = self.driver.current_url
            if href and href in current_url:
                self.logger.info(f"[SUCCESS] Successfully navigated to {post_type} post")
                return True
            else:
                self.logger.info(f"[SUCCESS] Navigated to {post_type} post (URL verification skipped)")
                return True
                
        except Exception as e:
            self.logger.error(f"Error navigating to {post_type} post: {e}")
            return False
    
    def simulate_post_reading(self, duration_minutes=2):
        """Simulate reading a post with natural behavior"""
        try:
            self.logger.info(f"[READ] Simulating post reading for {duration_minutes} minutes")
            
            # Use the existing natural article reading
            from advanced_website_robot import HumanLikeScroller
            scroller = HumanLikeScroller(self.driver, self.timing, self.mouse)
            
            # Simulate reading behavior
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while time.time() < end_time:
                # Random reading behavior
                behavior = random.choice(['scroll', 'pause', 're_read', 'scan'])
                
                if behavior == 'scroll':
                    scroller.reading_behavior_scroll()
                elif behavior == 'pause':
                    pause_duration = random.uniform(2, 8)
                    self.logger.info(f"[READ] Reading pause: {pause_duration:.1f}s")
                    time.sleep(pause_duration)
                elif behavior == 're_read':
                    scroller.quick_scan_scroll()
                elif behavior == 'scan':
                    scroller.quick_scan_scroll()
                
                # Random delay between behaviors
                time.sleep(random.uniform(1, 3))
            
            self.logger.info("[SUCCESS] Post reading simulation completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error simulating post reading: {e}")
            return False


class ArticleBrowser:
    """Advanced article browsing system with Previous/Next Post Navigation for AdSense RPM optimization"""
    def __init__(self, driver, timing_system, mouse_simulator, risk_monitor):
        self.driver = driver
        self.timing = timing_system
        self.mouse = mouse_simulator
        self.risk_monitor = risk_monitor
        self.config = Configuration()
        self.patterns = DetectionPatterns()
        self.ad_clicker = AdClickingSystem(driver, timing_system, mouse_simulator)
        self.human_scroller = HumanLikeScroller(driver, timing_system, mouse_simulator)
        self.logger = logging.getLogger('advanced_website_robot')
        
        # Previous/Next Post Navigation System
        self.post_navigator = PostNavigator(driver, timing_system, mouse_simulator, risk_monitor)
        self.visited_posts = []  # Track visited posts to avoid loops
        self.min_posts_per_session = 5  # Default 3 Minimum posts to visit per session
        self.max_posts_per_session = 10  # Default 7 Maximum posts to visit per session
    
    def open_article_with_referer_legacy(self, article_url, referer_url=None):
        """
        Legacy method for backward compatibility - use open_article_with_referer() instead
        """
        self.logger.warning("[WARNING] Using legacy method open_article_with_referer_legacy(). Please use open_article_with_referer() instead.")
        return self.open_article_with_referer(article_url, referer_url)
    
    def _simulate_referer_browsing(self):
        """Simulate natural referer browsing (bandwidth optimized)"""
        try:
            self.logger.info("Simulating natural referer browsing (bandwidth optimized)")
            
            # Quick initial wait
            time.sleep(random.uniform(0.5, 1.5))
            
            # Light scroll behavior (minimal bandwidth usage)
            scroll_count = random.randint(1, 2)  # Reduced from 2-4
            for i in range(scroll_count):
                scroll_amount = random.randint(50, 150)  # Reduced from 100-250
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.5, 1.5))  # Reduced from 2.0-4.0
            
            # Minimal mouse movement
            if random.random() < 0.4:  # 40% chance for mouse movement
                self.mouse.random_mouse_movement(random.uniform(0.5, 1.0))  # Reduced duration
            
            # Quick final pause
            time.sleep(random.uniform(5.0, 10.0))  # Reduced from 2.0-5.0
            
            # Check for ads on referer page (low chance)
            if random.random() < 0.1:  # 10% chance to check for ads on referer
                self.logger.info("[SCAN] Checking for Google AdSense ads on referer page...")
                clicked_ads = self.ad_clicker.click_ads(max_clicks=1, conservative=True)
                if clicked_ads:
                    self.logger.info(f"[SUCCESS] Clicked {len(clicked_ads)} Google AdSense ads on referer page")
                else:
                    self.logger.info("[INFO] No suitable Google AdSense ads found on referer page")
            
            self.logger.info("Referer browsing completed (bandwidth optimized)")
            
        except Exception as e:
            self.logger.warning(f"Error simulating referer browsing: {e}")
    
    def _natural_article_reading(self, duration_minutes=3):
        """More natural article reading behavior with human imperfections"""
        try:
            self.logger.info(f"Starting natural article reading for {duration_minutes} minutes")
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            # Remove rigid state machine, use more fluid behavior
            reading_mood = random.choice(["focused", "distracted", "careful", "quick"])
            last_distraction = time.time()
            reading_rhythm = random.randint(15, 35)  # Start with natural rhythm
            
            # Ad clicking integration - OPTIMIZED FOR NATURAL BEHAVIOR
            last_ad_check = time.time()
            ad_check_interval_min = self.config.get('reading.ad_check_interval_min', 120)
            ad_check_interval_max = self.config.get('reading.ad_check_interval_max', 300)
            ad_check_interval = random.uniform(ad_check_interval_min, ad_check_interval_max)
            
            # Safety counter to prevent infinite loops
            iteration_count = 0
            max_iterations = int(duration_minutes * 60 / 2)  # Max 2-second intervals
            
            while time.time() < end_time and iteration_count < max_iterations:
                try:
                    current_time = time.time()
                    iteration_count += 1
                    
                    # Random distractions (like human getting distracted)
                    if current_time - last_distraction > random.uniform(30, 120):
                        if random.random() < 0.3:  # 30% chance of distraction
                            self._simulate_distraction()
                            last_distraction = current_time
                    
                    # Check for ads periodically
                    ads_clicked_this_iteration = False
                    if current_time - last_ad_check > ad_check_interval:
                        self.logger.info("[SCAN] Checking for Google AdSense ads...")
                        try:
                            clicked_ads = self.ad_clicker.click_ads(max_clicks=1, conservative=True)
                            if clicked_ads:
                                self.logger.info(f"[SUCCESS] Clicked {len(clicked_ads)} Google AdSense ads")
                                # Post-click behavior is handled automatically in _click_ad_safely
                                ads_clicked_this_iteration = True
                                self.logger.info("[INFO] Skipping reading behavior this iteration due to ad click")
                            else:
                                self.logger.info("[INFO] No suitable Google AdSense ads found")
                        except Exception as ad_error:
                            self.logger.warning(f"[WARNING] Ad clicking failed: {ad_error}")
                        
                        last_ad_check = current_time
                        ad_check_interval = random.uniform(ad_check_interval_min, ad_check_interval_max)  # Reset interval from config
                    
                    # Reading behavior based on mood (skip if ads were clicked this iteration)
                    if not ads_clicked_this_iteration:
                        try:
                            if reading_mood == "focused":
                                self._focused_reading(reading_rhythm)
                            elif reading_mood == "distracted":
                                self._distracted_reading(reading_rhythm)
                            elif reading_mood == "careful":
                                self._careful_reading(reading_rhythm)
                            else:  # quick
                                self._quick_reading(reading_rhythm)
                        except Exception as reading_error:
                            self.logger.warning(f"[WARNING] Reading behavior failed: {reading_error}")
                            # Fallback to simple scroll
                            self.driver.execute_script("window.scrollBy(0, 100);")
                            time.sleep(random.uniform(1, 3))
                    else:
                        # Add a small pause after ad click before next iteration
                        time.sleep(random.uniform(2.0, 4.0))
                    
                    # Change mood occasionally (like human mood changes) - REDUCED FREQUENCY
                    mood_change_chance = self.config.get('reading.mood_change_chance', 0.03)
                    if random.random() < mood_change_chance:
                        old_mood = reading_mood
                        reading_mood = random.choice(["focused", "distracted", "careful", "quick"])
                        self.logger.info(f"[MOOD] Reading mood changed from {old_mood} to: {reading_mood}")
                        
                        # Add mood transition behavior
                        if old_mood != reading_mood and self.config.get('reading.mood_transitions', True):
                            self._simulate_mood_transition(old_mood, reading_mood)
                    
                    # Adjust reading rhythm naturally
                    if random.random() < 0.2:  # 20% chance to adjust rhythm
                        if reading_rhythm < 20:
                            reading_rhythm += random.randint(1, 3)  # Gradually increase speed
                        elif reading_rhythm > 50:
                            reading_rhythm -= random.randint(1, 3)  # Gradually decrease speed
                    
                    # Natural reading pause
                    time.sleep(random.uniform(0.5, 2.0))
                    
                except Exception as iteration_error:
                    self.logger.warning(f"[WARNING] Error in reading iteration: {iteration_error}")
                    # Continue with next iteration
                    time.sleep(random.uniform(1, 3))
                    continue
            
            self.logger.info("Natural article reading completed successfully")
            return True
                
        except Exception as e:
            self.logger.error(f"Error in natural article reading: {e}")
            # Fallback to simple scrolling
            try:
                self._fallback_browsing_behavior(duration_minutes)
                return True
            except Exception as fallback_error:
                self.logger.error(f"Fallback browsing also failed: {fallback_error}")
                return False
    
    def _simulate_distraction(self):
        """Simulate human distraction behavior"""
        try:
            distraction_type = random.choice([
                "scroll_back",      # Scroll back to re-read
                "mouse_wander",     # Mouse wanders around
                "pause_long",       # Long pause
                "scroll_random"     # Random scrolling
            ])
            
            self.logger.info(f"[DISTRACTION] Simulating {distraction_type}")
            
            if distraction_type == "scroll_back":
                # Scroll back to previous content
                self.driver.execute_script("window.scrollBy(0, -200);")
                time.sleep(random.uniform(2, 5))
                
            elif distraction_type == "mouse_wander":
                # Mouse wanders around
                self.mouse_simulator.random_mouse_movement(duration=2.0)
                
            elif distraction_type == "pause_long":
                # Long pause like human got distracted
                time.sleep(random.uniform(5, 12))
                
            elif distraction_type == "scroll_random":
                # Random scrolling
                for _ in range(random.randint(2, 5)):
                    scroll_amount = random.randint(-300, 300)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(0.5, 1.5))
                    
        except Exception as e:
            self.logger.debug(f"Error in distraction simulation: {e}")
    
    def _simulate_mood_transition(self, old_mood, new_mood):
        """Simulate natural mood transition behavior"""
        try:
            # Add transition pause
            transition_pause = random.uniform(1.0, 2.5)
            time.sleep(transition_pause)
            
            # Add transition-specific behavior
            if old_mood == "focused" and new_mood == "distracted":
                # From focused to distracted - simulate losing focus
                self.driver.execute_script("window.scrollBy({top: -50, behavior: 'smooth'});")
                time.sleep(random.uniform(0.5, 1.0))
            elif old_mood == "distracted" and new_mood == "focused":
                # From distracted to focused - simulate refocusing
                self.driver.execute_script("window.scrollBy({top: 30, behavior: 'smooth'});")
                time.sleep(random.uniform(0.5, 1.0))
            elif old_mood == "quick" and new_mood == "careful":
                # From quick to careful - simulate slowing down
                self.driver.execute_script("window.scrollBy({top: -20, behavior: 'smooth'});")
                time.sleep(random.uniform(1.0, 2.0))
            elif old_mood == "careful" and new_mood == "quick":
                # From careful to quick - simulate speeding up
                self.driver.execute_script("window.scrollBy({top: 40, behavior: 'smooth'});")
                time.sleep(random.uniform(0.3, 0.8))
                
        except Exception as e:
            self.logger.debug(f"Error in mood transition: {e}")
    
    def _focused_reading(self, rhythm):
        """Focused reading behavior with natural micro-movements"""
        try:
            # Natural scroll amount based on rhythm (smaller, more natural)
            if rhythm < 25:
                scroll_amount = random.randint(50, 120)  # Slower, smaller scrolls
            else:
                scroll_amount = random.randint(80, 150)  # Faster, slightly larger scrolls
            
            # Smooth scrolling with natural variations
            self.driver.execute_script(f"window.scrollBy({{top: {scroll_amount}, behavior: 'smooth'}});")
            
            # Natural reading pause with micro-variations - CONFIGURATION-BASED
            if self.config.get('reading.natural_reading_pauses', True):
                pause_min = self.config.get('reading.pause_timing.focused_pause_min', 1.0)
                pause_max = self.config.get('reading.pause_timing.focused_pause_max', 3.0)
                base_pause = random.uniform(pause_min, pause_max)
            else:
                base_pause = random.uniform(0.5, 1.5)  # Shorter pauses if disabled
            
            # Add micro-movements during reading
            micro_movement_chance = self.config.get('reading.micro_movement_chance', 0.3)
            if random.random() < micro_movement_chance:
                self.mouse.random_mouse_movement(random.uniform(0.5, 1.5))
            
            # Natural reading pause with comprehension time
            if self.config.get('reading.comprehension_time', True):
                time.sleep(base_pause)
            else:
                time.sleep(base_pause * 0.5)  # Shorter comprehension time if disabled
            
            # Occasional re-reading behavior
            re_read_chance = self.config.get('reading.re_read_chance', 0.15)
            if random.random() < re_read_chance:
                self.driver.execute_script("window.scrollBy({top: -30, behavior: 'smooth'});")
                # Re-read pause - CONFIGURATION-BASED
                re_read_pause_min = self.config.get('reading.pause_timing.re_read_pause_min', 0.5)
                re_read_pause_max = self.config.get('reading.pause_timing.re_read_pause_max', 2.0)
                time.sleep(random.uniform(re_read_pause_min, re_read_pause_max))
                
        except Exception as e:
            self.logger.debug(f"Error in focused reading: {e}")
            # Fallback to simple scroll
            try:
                self.driver.execute_script("window.scrollBy(0, 80);")
                time.sleep(random.uniform(1.5, 2.5))
            except:
                pass
    
    def _distracted_reading(self, rhythm):
        """Distracted reading behavior"""
        try:
            # Irregular scrolling with frequent pauses
            scroll_amount = random.randint(50, 150)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Longer pauses (like human getting distracted) - CONFIGURATION-BASED
            pause_min = self.config.get('reading.pause_timing.distracted_pause_min', 2.0)
            pause_max = self.config.get('reading.pause_timing.distracted_pause_max', 6.0)
            time.sleep(random.uniform(pause_min, pause_max))
            
            # Sometimes scroll back - CONFIGURATION-BASED
            if random.random() < 0.3:
                self.driver.execute_script("window.scrollBy(0, -100);")
                re_read_pause_min = self.config.get('reading.pause_timing.re_read_pause_min', 0.5)
                re_read_pause_max = self.config.get('reading.pause_timing.re_read_pause_max', 2.0)
                time.sleep(random.uniform(re_read_pause_min, re_read_pause_max))
                
        except Exception as e:
            self.logger.debug(f"Error in distracted reading: {e}")
            # Fallback to simple scroll
            try:
                self.driver.execute_script("window.scrollBy(0, 50);")
                time.sleep(random.uniform(2, 4))
            except:
                pass
    
    def _careful_reading(self, rhythm):
        """Careful reading behavior"""
        try:
            # Small, careful scrolls
            scroll_amount = random.randint(50, 120)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Longer pauses for careful reading - CONFIGURATION-BASED
            pause_min = self.config.get('reading.pause_timing.careful_pause_min', 2.5)
            pause_max = self.config.get('reading.pause_timing.careful_pause_max', 5.0)
            time.sleep(random.uniform(pause_min, pause_max))
            
            # Sometimes re-read by scrolling back - CONFIGURATION-BASED
            if random.random() < 0.4:
                self.driver.execute_script("window.scrollBy(0, -50);")
                re_read_pause_min = self.config.get('reading.pause_timing.re_read_pause_min', 0.5)
                re_read_pause_max = self.config.get('reading.pause_timing.re_read_pause_max', 2.0)
                time.sleep(random.uniform(re_read_pause_min, re_read_pause_max))
                
        except Exception as e:
            self.logger.debug(f"Error in careful reading: {e}")
            # Fallback to simple scroll
            try:
                self.driver.execute_script("window.scrollBy(0, 75);")
                time.sleep(random.uniform(2, 3))
            except:
                pass
    
    def _quick_reading(self, rhythm):
        """Quick reading behavior"""
        try:
            # Larger scrolls for quick reading
            scroll_amount = random.randint(200, 400)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Shorter pauses - CONFIGURATION-BASED
            pause_min = self.config.get('reading.pause_timing.quick_pause_min', 0.5)
            pause_max = self.config.get('reading.pause_timing.quick_pause_max', 2.0)
            time.sleep(random.uniform(pause_min, pause_max))
            
        except Exception as e:
            self.logger.debug(f"Error in quick reading: {e}")
            # Fallback to simple scroll
            try:
                self.driver.execute_script("window.scrollBy(0, 150);")
                time.sleep(random.uniform(0.5, 1))
            except:
                pass
    
    def _initial_article_scan(self):
        """Initial scan of the article to understand structure"""
        try:
            self.logger.info("Performing initial article scan")
            
            # Get article structure
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Quick scan: scroll to see article structure
            scan_positions = [0.2, 0.4, 0.6, 0.8]  # Scan at 20%, 40%, 60%, 80% of article
            
            for position in scan_positions:
                target_scroll = int(page_height * position)
                self._human_like_scroll_to_position(target_scroll, duration=1.5)
                
                # Quick pause to "see" the content
                scan_pause = random.uniform(0.8, 2.0)
                time.sleep(scan_pause)
                
                # Occasional mouse movement during scan
                if random.random() < 0.3:
                    self._natural_mouse_tracking()
            
            # Return to top to start reading
            self._human_like_scroll_to_position(0, duration=2.0)
            time.sleep(random.uniform(1.0, 2.5))
            
        except Exception as e:
            self.logger.warning(f"Error during initial article scan: {e}")
    
    def _natural_paragraph_reading(self, reading_rhythm):
        """Read a paragraph naturally based on reading rhythm - NO FAST READING"""
        try:
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Calculate reading speed based on rhythm (0-100)
            # Higher rhythm = slightly faster reading, but NO FAST READING
            base_scroll_amount = random.randint(30, 80)  # Much smaller, more human-like scrolls
            rhythm_multiplier = 0.5 + (reading_rhythm / 100) * 0.3  # 0.5x to 0.8x (NO FAST)
            scroll_amount = int(base_scroll_amount * rhythm_multiplier)
            
            # Add natural variation with micro-adjustments
            variation = random.uniform(0.6, 1.1)  # Reduced max variation
            scroll_amount = int(scroll_amount * variation)
            
            # Add micro-adjustments like human reading
            if random.random() < 0.4:  # 40% chance for micro-adjustment
                micro_adjustment = random.randint(-15, 15)
                scroll_amount += micro_adjustment
            
            # Check if we're near the end - but don't stop too early
            remaining_height = page_height - current_scroll - viewport_height
            if remaining_height < 100:  # Only stop when very close to bottom
                # Ensure we scroll to the very bottom to read everything
                self.logger.info("Near bottom, ensuring complete reading to the end")
                self._ensure_complete_bottom_reading()
                return "finished"
            
            # Determine scroll behavior based on reading rhythm - NO FAST READING
            if reading_rhythm < 40:  # Slow, careful reading
                # Use line-by-line scrolling for careful reading
                lines_to_scroll = random.randint(1, 3)  # Fewer lines for more careful reading
                self._natural_line_by_line_scroll(lines_to_scroll)
                
                # Much longer reading pause for comprehension
                reading_pause = random.uniform(8.0, 15.0)  # Much longer pauses for understanding
                time.sleep(reading_pause)
                
                # Add comprehension pause for complex content
                if random.random() < 0.3:  # 30% chance for comprehension pause
                    comprehension_pause = random.uniform(5.0, 12.0)
                    self.logger.info(f"Comprehension pause: {comprehension_pause:.1f}s")
                    time.sleep(comprehension_pause)
                
                # Higher chance of re-reading
                if random.random() < 0.4:  # Increased re-read chance
                    return "re_read_needed"
                    
            else:  # Normal reading (NO FAST READING)
                # Use paragraph-based scrolling for normal reading
                paragraph_length = random.choice(["short", "medium", "long"])
                self._natural_paragraph_scroll(paragraph_length)
                
                # Normal reading pause - much longer for understanding
                reading_pause = random.uniform(6.0, 12.0)  # Much longer normal pauses
                time.sleep(reading_pause)
                
                # Add thinking pause for processing information - UNIFIED THINKING BEHAVIOR
                if self._simulate_thinking_behavior(article_text, "processing"):
                    pass  # Thinking behavior already executed in _simulate_thinking_behavior
                
                # Occasional re-reading
                if random.random() < 0.25:  # Increased re-read chance
                    return "re_read_needed"
            
            return "reading"
            
        except Exception as e:
            self.logger.warning(f"Error during natural paragraph reading: {e}")
            return "reading"
    
    def _re_read_previous_content(self):
        """Re-read previous content like humans do"""
        try:
            self.logger.info("Re-reading previous content")
            
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            
            # Scroll back to re-read (like humans do when they miss something)
            re_read_amount = random.randint(150, 400)
            new_position = max(0, current_scroll - re_read_amount)
            
            self._human_like_scroll_to_position(new_position, duration=2.0)
            
            # Longer pause for re-reading
            re_read_pause = random.uniform(4.0, 10.0)
            time.sleep(re_read_pause)
            
            # Mouse movement during re-reading (like following text)
            self._natural_mouse_tracking()
            
        except Exception as e:
            self.logger.warning(f"Error during re-reading: {e}")
    
    def _careful_content_scan(self):
        """Careful scanning behavior - NO FAST SCANNING"""
        try:
            self.logger.info("Careful content scanning")
            
            # Moderate scroll for careful scanning
            scan_amount = random.randint(200, 350)  # Reduced from 300-600
            self._human_like_scroll_by_amount(scan_amount, duration=1.5)  # Slower duration
            
            # Longer pause for careful scanning
            scan_pause = random.uniform(2.0, 4.0)  # Longer pause
            time.sleep(scan_pause)
            
        except Exception as e:
            self.logger.warning(f"Error during careful content scan: {e}")
    
    def _finish_reading_behavior(self):
        """Final reading behavior when near the end - comprehensive reading"""
        try:
            self.logger.info("[READ] Starting comprehensive finish reading behavior")
            
            # Get page dimensions
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            
            # Ensure we're at the very bottom
            bottom_position = page_height - viewport_height
            self.logger.info(f"Scrolling to absolute bottom: {bottom_position}")
            self._human_like_scroll_to_position(bottom_position, duration=4.0)
            
            # Comprehensive bottom reading
            self.logger.info("Reading bottom content comprehensively")
            bottom_reading_pause = random.uniform(15.0, 25.0)  # Very long pause for bottom reading
            time.sleep(bottom_reading_pause)
            
            # Scroll up to re-read conclusion section
            conclusion_scroll = random.randint(300, 600)
            conclusion_position = max(0, bottom_position - conclusion_scroll)
            self.logger.info(f"Re-reading conclusion section from position: {conclusion_position}")
            self._human_like_scroll_to_position(conclusion_position, duration=3.0)
            
            # Read conclusion thoroughly
            conclusion_pause = random.uniform(12.0, 20.0)  # Long pause for conclusion
            time.sleep(conclusion_pause)
            
            # Scroll back to bottom for final verification
            self.logger.info("Final verification - scrolling back to bottom")
            self._human_like_scroll_to_position(bottom_position, duration=2.0)
            
            # Final comprehensive reading pause
            final_verification_pause = random.uniform(8.0, 15.0)
            self.logger.info(f"Final verification reading pause: {final_verification_pause:.1f}s")
            time.sleep(final_verification_pause)
            
            # Verify we've read the entire article
            self._verify_complete_article_reading()
            
            self.logger.info("[SUCCESS] Comprehensive finish reading behavior completed")
            
        except Exception as e:
            self.logger.warning(f"Error during finish reading behavior: {e}")
    
    def _human_like_scroll_to_position(self, target_position, duration=2.0):
        """Human-like scroll to specific position with natural patterns"""
        try:
            current_position = self.driver.execute_script("return window.pageYOffset")
            distance = target_position - current_position
            
            if abs(distance) < 30:  # Already close enough
                return True
            
            # Human-like scroll patterns
            scroll_direction = 1 if distance > 0 else -1
            abs_distance = abs(distance)
            
            # Calculate natural scroll behavior
            if abs_distance < 200:  # Small scroll - single smooth movement
                self._natural_small_scroll(distance, duration)
            elif abs_distance < 800:  # Medium scroll - with micro-pauses
                self._natural_medium_scroll(distance, duration)
            else:  # Large scroll - with multiple phases
                self._natural_large_scroll(distance, duration)
            
            return True
            
        except Exception as e:
            return False
    
    def _natural_small_scroll(self, distance, duration):
        """Natural small scroll behavior"""
        try:
            # Small scrolls are usually smooth with slight variations
            steps = random.randint(3, 8)
            step_size = distance / steps
            step_duration = duration / steps
            
            for step in range(steps):
                # Natural scroll with slight acceleration/deceleration
                progress = (step + 1) / steps
                
                # Ease-in-out curve for natural movement
                if progress < 0.5:
                    ease_factor = 2 * progress * progress
                else:
                    ease_factor = 1 - 2 * (1 - progress) * (1 - progress)
                
                new_position = self.driver.execute_script("return window.pageYOffset") + (step_size * ease_factor)
                self.driver.execute_script(f"window.scrollTo(0, {new_position});")
                
                # Natural timing variation
                delay = step_duration * random.uniform(0.8, 1.3)
                time.sleep(delay)
                
                # Occasional micro-pause (like reading a word)
                if random.random() < 0.15:
                    micro_pause = random.uniform(0.1, 0.3)
                    time.sleep(micro_pause)
            
        except Exception as e:
            pass
    
    def _natural_medium_scroll(self, distance, duration):
        """Natural medium scroll behavior with micro-pauses"""
        try:
            # Medium scrolls have natural pauses and variations
            phases = random.randint(2, 4)  # Multiple phases
            phase_distance = distance / phases
            
            for phase in range(phases):
                # Scroll phase
                phase_start = self.driver.execute_script("return window.pageYOffset")
                phase_end = phase_start + phase_distance
                
                # Natural scroll within phase
                self._natural_small_scroll(phase_distance, duration / phases)
                
                # Natural pause between phases (like reading)
                if phase < phases - 1:  # Don't pause after last phase
                    pause_duration = random.uniform(0.3, 1.2)
                    time.sleep(pause_duration)
                    
                    # Occasional hesitation (like re-reading)
                    if random.random() < 0.2:
                        hesitation = random.uniform(0.5, 1.5)
                        time.sleep(hesitation)
            
        except Exception as e:
            pass
    
    def _natural_large_scroll(self, distance, duration):
        """Natural large scroll behavior with multiple phases and pauses"""
        try:
            # Large scrolls are broken into natural reading phases
            phases = random.randint(3, 6)
            phase_distance = distance / phases
            
            for phase in range(phases):
                # Scroll phase
                self._natural_medium_scroll(phase_distance, duration / phases)
                
                # Longer pause between phases (like reading a section) - much longer
                if phase < phases - 1:  # Don't pause after last phase
                    pause_duration = random.uniform(3.0, 8.0)  # Much longer pauses
                    time.sleep(pause_duration)
                    
                    # Occasional longer pause (like getting distracted) - more frequent and longer
                    if random.random() < 0.4:  # Increased chance
                        distraction_pause = random.uniform(5.0, 12.0)  # Much longer distraction pause
                        time.sleep(distraction_pause)
                        self.logger.info(f"Distraction pause during scroll: {distraction_pause:.1f}s")
            
        except Exception as e:
            pass
    
    def _human_like_scroll_by_amount(self, scroll_amount, duration=1.5):
        """Human-like scroll by specific amount"""
        try:
            current_position = self.driver.execute_script("return window.pageYOffset")
            target_position = current_position + scroll_amount
            self._human_like_scroll_to_position(target_position, duration)
        except Exception as e:
            pass
    
    def _calculate_natural_reading_pause(self, reading_rhythm):
        """Calculate natural pause between reading actions - NO FAST READING"""
        # Base pause based on reading rhythm - NO FAST READING
        if reading_rhythm < 40:  # Slow reading
            base_pause = random.uniform(8.0, 15.0)  # Much longer pauses for comprehension
        else:  # Normal reading (NO FAST READING)
            base_pause = random.uniform(6.0, 12.0)  # Much longer normal pauses
        
        # Add occasional longer pauses (like getting distracted or thinking) - more frequent and longer
        if random.random() < 0.35:  # Increased chance for distraction/thinking pause
            distraction_pause = random.uniform(12.0, 30.0)  # Much longer distraction pauses
            base_pause += distraction_pause
            self.logger.info(f"Distraction/thinking pause: {distraction_pause:.1f}s")
        
        # Add comprehension pause for complex content - more frequent and longer
        if random.random() < 0.3:  # Increased chance for comprehension pause
            comprehension_pause = random.uniform(8.0, 20.0)  # Much longer comprehension pause
            base_pause += comprehension_pause
            self.logger.info(f"Comprehension pause: {comprehension_pause:.1f}s")
        
        return base_pause
    
    def _natural_mouse_tracking(self):
        """Natural mouse movement like following text"""
        try:
            # Shorter, more natural mouse movements
            duration = random.uniform(0.5, 1.5)
            self.mouse.random_mouse_movement(duration)
        except Exception as e:
            pass
    
    def _ensure_complete_bottom_reading(self):
        """Ensure article is read completely to the bottom"""
        try:
            self.logger.info("[READ] Ensuring complete reading to the bottom of the article")
            
            # Get current position and page dimensions
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Scroll to the very bottom
            bottom_position = page_height - viewport_height
            self.logger.info(f"Scrolling to bottom position: {bottom_position}")
            self._human_like_scroll_to_position(bottom_position, duration=3.0)
            
            # Read the bottom content thoroughly
            self.logger.info("Reading bottom content thoroughly")
            bottom_reading_pause = random.uniform(10.0, 20.0)  # Long pause for bottom reading
            time.sleep(bottom_reading_pause)
            
            # Scroll up a bit to re-read some bottom content
            if random.random() < 0.7:  # 70% chance to re-read bottom
                re_read_scroll = random.randint(100, 300)
                re_read_position = bottom_position - re_read_scroll
                self.logger.info(f"Re-reading bottom content from position: {re_read_position}")
                self._human_like_scroll_to_position(re_read_position, duration=2.0)
                
                # Read the re-read content
                re_read_pause = random.uniform(8.0, 15.0)
                time.sleep(re_read_pause)
                
                # Scroll back to bottom
                self._human_like_scroll_to_position(bottom_position, duration=2.0)
            
            # Final bottom reading pause
            final_bottom_pause = random.uniform(5.0, 12.0)
            self.logger.info(f"Final bottom reading pause: {final_bottom_pause:.1f}s")
            time.sleep(final_bottom_pause)
            
            self.logger.info("[SUCCESS] Complete bottom reading finished")
            
        except Exception as e:
            self.logger.warning(f"Error in complete bottom reading: {e}")
    
    def _verify_complete_article_reading(self):
        """Verify that the entire article has been read comprehensively"""
        try:
            self.logger.info("[SCAN] Verifying complete article reading")
            
            # Get current position and page dimensions
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Calculate reading coverage
            max_scroll_position = page_height - viewport_height
            reading_coverage = (current_scroll / max_scroll_position) * 100 if max_scroll_position > 0 else 100
            
            self.logger.info(f"[STATS] Reading coverage: {reading_coverage:.1f}%")
            
            # Ensure we've covered at least 95% of the article
            if reading_coverage < 95:
                self.logger.info(f"[WARNING] Reading coverage below 95% ({reading_coverage:.1f}%), ensuring complete coverage")
                
                # Scroll to any missed sections
                missed_sections = []
                for i in range(0, int(max_scroll_position), 500):  # Check every 500px
                    if i > current_scroll - 200:  # If we haven't read this section
                        missed_sections.append(i)
                
                # Read missed sections
                for section_position in missed_sections[:3]:  # Limit to 3 sections
                    self.logger.info(f"Reading missed section at position: {section_position}")
                    self._human_like_scroll_to_position(section_position, duration=2.0)
                    
                    # Read the section
                    section_reading_pause = random.uniform(8.0, 15.0)
                    time.sleep(section_reading_pause)
                
                # Final scroll to bottom
                self._human_like_scroll_to_position(max_scroll_position, duration=2.0)
                final_verification_pause = random.uniform(5.0, 10.0)
                time.sleep(final_verification_pause)
            
            # Final comprehensive reading verification
            self.logger.info("[READ] Performing final comprehensive reading verification")
            
            # Scroll through the entire article one more time (quick scan)
            self._comprehensive_article_scan()
            
            self.logger.info("[SUCCESS] Complete article reading verification finished")
            
        except Exception as e:
            self.logger.warning(f"Error in complete article reading verification: {e}")
    
    def _comprehensive_article_scan(self):
        """Perform a comprehensive scan of the entire article"""
        try:
            self.logger.info("[READ] Performing comprehensive article scan")
            
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            max_scroll_position = page_height - viewport_height
            
            # Scan in sections
            section_size = 400  # 400px sections
            num_sections = max(1, int(max_scroll_position / section_size))
            
            for section in range(num_sections):
                section_position = section * section_size
                self.logger.info(f"Scanning section {section + 1}/{num_sections} at position: {section_position}")
                
                # Scroll to section
                self._human_like_scroll_to_position(section_position, duration=1.5)
                
                # Brief reading pause
                section_pause = random.uniform(3.0, 6.0)
                time.sleep(section_pause)
            
            # Final scroll to bottom
            self._human_like_scroll_to_position(max_scroll_position, duration=2.0)
            final_scan_pause = random.uniform(5.0, 10.0)
            time.sleep(final_scan_pause)
            
            self.logger.info("[SUCCESS] Comprehensive article scan completed")
            
        except Exception as e:
            self.logger.warning(f"Error in comprehensive article scan: {e}")
    
    def _natural_paragraph_scroll(self, paragraph_length="medium"):
        """Natural scroll behavior based on paragraph length"""
        try:
            # Get current scroll position
            current_scroll = self.driver.execute_script("return window.pageYOffset")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            # Calculate scroll amount based on paragraph length - more human-like
            if paragraph_length == "short":
                # Short paragraphs - very small, precise scrolls
                scroll_amount = random.randint(25, 60)  # Much smaller for human-like reading
                phases = random.randint(2, 4)  # More phases for smoothness
            elif paragraph_length == "long":
                # Long paragraphs - moderate scrolls with more pauses
                scroll_amount = random.randint(80, 150)  # Reduced for more natural reading
                phases = random.randint(3, 6)  # More phases for smoothness
            else:  # medium
                # Medium paragraphs - balanced scrolls
                scroll_amount = random.randint(50, 100)  # Reduced for more natural reading
                phases = random.randint(2, 4)  # More phases for smoothness
            
            # Natural scroll with phases
            phase_amount = scroll_amount / phases
            
            for phase in range(phases):
                # Scroll phase
                self._human_like_scroll_by_amount(phase_amount, duration=1.0)
                
                # Natural pause between phases (like reading) - much longer
                if phase < phases - 1:
                    pause_duration = random.uniform(3.0, 8.0)  # Much longer pauses between phases
                    time.sleep(pause_duration)
                    
                    # Occasional micro-scroll adjustment (more frequent)
                    if random.random() < 0.6:  # Increased chance for micro-adjustment
                        micro_adjustment = random.randint(-8, 8)  # Smaller adjustments
                        self._human_like_scroll_by_amount(micro_adjustment, duration=1.2)  # Longer duration
            
            return True
            
        except Exception as e:
            return False
    
    def _natural_line_by_line_scroll(self, lines=3):
        """Natural line-by-line scrolling like reading"""
        try:
            # Line-by-line scrolling is very natural - smaller and more human-like
            line_height = random.randint(12, 20)  # Smaller line height for more natural reading
            
            for line in range(lines):
                # Scroll one line with micro-adjustments
                scroll_amount = line_height + random.randint(-2, 2)  # Small variation
                self._human_like_scroll_by_amount(scroll_amount, duration=0.8)  # Longer duration
                
                # Natural pause between lines - much longer for comprehension
                line_pause = random.uniform(2.0, 5.0)  # Much longer pauses
                time.sleep(line_pause)
                
                # Occasional longer pause (like reading a complex sentence) - more frequent and longer
                if random.random() < 0.4:  # Increased chance
                    reading_pause = random.uniform(4.0, 10.0)  # Much longer reading pause
                    self.logger.info(f"Complex sentence reading pause: {reading_pause:.1f}s")
                    time.sleep(reading_pause)
                
                # Occasional micro-scroll adjustment - more frequent
                if random.random() < 0.5:  # Increased chance for micro-adjustment
                    micro_adjustment = random.randint(-3, 3)
                    self._human_like_scroll_by_amount(micro_adjustment, duration=0.8)  # Longer duration
            
            return True
            
        except Exception as e:
            return False
    
    def _navigate_with_referer(self, target_url, referer_url):
        """DEPRECATED: Use _real_referer_flow() instead - this method doesn't work properly"""
        self.logger.warning("[DEPRECATED] _navigate_with_referer() doesn't work properly")
        self.logger.info("[INFO] Use _real_referer_flow() instead")
        return self._real_referer_flow(target_url, referer_url)
    
    def _real_referer_flow(self, target_url, referer_url):
        """REAL referer flow: 1. Buka referer page 2. Navigate ke target (referer akan terkirim otomatis)"""
        try:
            self.logger.info(f"[REAL REFERER] Starting real referer flow: {referer_url} -> {target_url}")
            
            # Step 1: Buka referer page (REAL)
            self.logger.info(f"[STEP 1] Opening referer page: {referer_url}")
            try:
                self.driver.get(referer_url)
                self.logger.info("[DEBUG] Referer page navigation executed")
            except Exception as ref_e:
                self.logger.error(f"[ERROR] Referer page navigation failed: {ref_e}")
                return False
            
            # Wait for referer page to load
            time.sleep(random.uniform(2, 5))
            
            # Check referer page load
            try:
                referer_current_url = self.driver.current_url
                self.logger.info(f"[DEBUG] Referer page loaded: {referer_current_url}")
                
                # Check if referer page has referer policy
                try:
                    referer_policy = self.driver.execute_script("return document.referrerPolicy;")
                    self.logger.info(f"[DEBUG] Referer policy: {referer_policy}")
                except:
                    self.logger.info("[DEBUG] Could not get referer policy")
                    
            except Exception as check_e:
                self.logger.warning(f"[DEBUG] Error checking referer page: {check_e}")
            
            # Step 2: Simulate browsing on referer page
            self.logger.info("[STEP 2] Simulating browsing on referer page")
            self._simulate_referer_browsing()
            
            # Step 3: Navigate to target using LINK CLICK METHOD (lebih reliable untuk referer)
            self.logger.info(f"[STEP 3] Navigating to target using link click method: {target_url}")
            try:
                # Use link click method for better referer support
                self.driver.execute_script(f"""
                    var link = document.createElement('a');
                    link.href = '{target_url}';
                    link.target = '_self';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                """)
                self.logger.info("[DEBUG] Link click navigation executed")
            except Exception as nav_e:
                self.logger.error(f"[ERROR] Link click navigation failed: {nav_e}")
                # Fallback to direct navigation
                try:
                    self.driver.get(target_url)
                    self.logger.info("[DEBUG] Fallback to direct navigation")
                except Exception as fallback_e:
                    self.logger.error(f"[ERROR] Fallback navigation also failed: {fallback_e}")
                    return False
            
            # Wait for target page to load with timeout
            load_timeout = 15  # 15 seconds timeout
            start_time = time.time()
            while time.time() - start_time < load_timeout:
                try:
                    current_url = self.driver.current_url
                    if target_url in current_url:
                        self.logger.info(f"[DEBUG] Page loaded successfully: {current_url}")
                        break
                    time.sleep(0.5)
                except Exception as check_e:
                    self.logger.warning(f"[DEBUG] Error checking page load: {check_e}")
                    time.sleep(0.5)
            else:
                self.logger.warning(f"[WARNING] Page load timeout after {load_timeout} seconds")
            
            # Additional wait for page stabilization
            time.sleep(random.uniform(1, 3))
            
            # Step 4: Verify referer was sent
            self.logger.info("[STEP 4] Verifying referer was sent")
            referer_verified = self._verify_referer_sent(referer_url)
            
            if referer_verified:
                self.logger.info("[SUCCESS] Real referer flow completed successfully")
                return True
            else:
                self.logger.warning("[WARNING] Referer verification failed - this is expected with direct navigation")
                self.logger.info("[INFO] Link click method should have already sent referer")
                
                # Check if we're already on the target page
                current_url = self.driver.current_url
                if target_url in current_url:
                    self.logger.info("[SUCCESS] Navigation completed successfully")
                    return True
                else:
                    self.logger.warning("[WARNING] Navigation may have failed")
                    return False
                
        except Exception as e:
            self.logger.error(f"[ERROR] Real referer flow failed: {e}")
            return False
    
    def _proxy_referer_flow(self, target_url, referer_url):
        """PROXY-BASED referer flow: Use proxy with referer headers"""
        try:
            self.logger.info(f"[PROXY REFERER] Starting proxy referer flow: {referer_url} -> {target_url}")
            
            # Method 1: Try using CDP (Chrome DevTools Protocol) to set headers
            try:
                # Enable network domain
                self.driver.execute_cdp_cmd('Network.enable', {})
                
                # Set referer header via CDP
                self.driver.execute_cdp_cmd('Network.setRequestInterception', {'enabled': True})
                
                # Navigate with referer
                self.driver.get(target_url)
                
                # Wait for page to load
                time.sleep(random.uniform(2, 4))
                
                # Verify referer was sent
                if self._verify_referer_sent(referer_url):
                    self.logger.info("[SUCCESS] Proxy referer flow completed successfully")
                    return True
                else:
                    self.logger.warning("[WARNING] Proxy referer verification failed")
                    return True  # Still return True as navigation worked
                    
            except Exception as e:
                self.logger.warning(f"CDP method failed: {e}")
            
            # Method 2: Fallback to real referer flow
            self.logger.info("[FALLBACK] Using real referer flow as fallback")
            return self._real_referer_flow(target_url, referer_url)
                
        except Exception as e:
            self.logger.error(f"[ERROR] Proxy referer flow failed: {e}")
            return False
    
    def _cdp_referer_flow(self, target_url, referer_url):
        """CDP-BASED referer flow: Use Chrome DevTools Protocol to set headers"""
        try:
            self.logger.info(f"[CDP REFERER] Starting CDP referer flow: {referer_url} -> {target_url}")
            
            # Enable network domain
            self.driver.execute_cdp_cmd('Network.enable', {})
            
            # Set referer header via CDP
            self.driver.execute_cdp_cmd('Network.setRequestInterception', {'enabled': True})
            
            # Navigate with referer
            self.driver.get(target_url)
            
            # Wait for page to load
            time.sleep(random.uniform(2, 4))
            
            # Verify referer was sent
            if self._verify_referer_sent(referer_url):
                self.logger.info("[SUCCESS] CDP referer flow completed successfully")
                return True
            else:
                self.logger.warning("[WARNING] CDP referer verification failed")
                return True  # Still return True as navigation worked
                
        except Exception as e:
            self.logger.error(f"[ERROR] CDP referer flow failed: {e}")
            return False
    
    def get_referer_method(self):
        """Get the best referer method to use"""
        try:
            # Check if CDP is available
            try:
                self.driver.execute_cdp_cmd('Network.enable', {})
                return 'cdp'
            except:
                pass
            
            # Check if proxy is available
            try:
                if hasattr(self.driver, 'execute_cdp_cmd'):
                    return 'proxy'
            except:
                pass
            
            # Default to real referer flow
            return 'real'
            
        except Exception as e:
            self.logger.warning(f"Error determining referer method: {e}")
            return 'real'
    
    def open_article_with_best_referer(self, article_url=None, referer_url=None):
        """Open article with the best available referer method"""
        try:
            # Get best referer method
            method = self.get_referer_method()
            self.logger.info(f"[REFERER] Using best referer method: {method}")
            
            if method == 'cdp':
                return self._cdp_referer_flow(article_url, referer_url)
            elif method == 'proxy':
                return self._proxy_referer_flow(article_url, referer_url)
            else:
                return self._real_referer_flow(article_url, referer_url)
                
        except Exception as e:
            self.logger.error(f"Error in best referer method: {e}")
            return False
    
    def _set_referer_header(self, referer_url):
        """DEPRECATED: This method doesn't work - JavaScript cannot set HTTP headers"""
        self.logger.warning("[DEPRECATED] _set_referer_header() doesn't work - JavaScript cannot set HTTP headers")
        self.logger.info("[INFO] Use _real_referer_flow() or _proxy_referer_flow() instead")
        return False
    
    def _verify_referer_sent(self, expected_referer):
        """Verify that referer was sent to the current page - REAL METHOD with detailed debugging"""
        try:
            # Get current URL for debugging
            current_url = self.driver.current_url
            self.logger.info(f"[DEBUG] Current URL: {current_url}")
            
            # Check document.referrer (the only reliable method)
            actual_referer = self.driver.execute_script("return document.referrer;")
            self.logger.info(f"[DEBUG] document.referrer: '{actual_referer}'")
            
            # Check if referer is empty or None
            if not actual_referer or actual_referer == "":
                self.logger.warning("[DEBUG] document.referrer is empty - possible causes:")
                self.logger.warning("  1. Browser security policy blocking referer")
                self.logger.warning("  2. HTTPS to HTTP referer not sent")
                self.logger.warning("  3. Cross-origin policy blocking referer")
                self.logger.warning("  4. Browser privacy settings")
                
                # Try to get referer from other sources
                try:
                    # Check if referer is in URL parameters
                    if 'referer' in current_url or 'ref' in current_url:
                        self.logger.info("[DEBUG] Referer found in URL parameters")
                    
                    # Check if referer is in page title or content
                    page_title = self.driver.title
                    if expected_referer.split('//')[1].split('/')[0] in page_title:
                        self.logger.info("[DEBUG] Referer domain found in page title")
                    
                except Exception as debug_e:
                    self.logger.warning(f"[DEBUG] Error in additional checks: {debug_e}")
            
            # Check if referer matches (partial match for domain)
            expected_domain = expected_referer.split('//')[1].split('/')[0] if '//' in expected_referer else expected_referer
            actual_domain = actual_referer.split('//')[1].split('/')[0] if actual_referer and '//' in actual_referer else actual_referer
            
            if actual_referer and expected_referer in actual_referer:
                self.logger.info(f"[SUCCESS] Real referer detected: {actual_referer}")
                return True
            elif actual_domain and expected_domain in actual_domain:
                self.logger.info(f"[SUCCESS] Referer domain detected: {actual_domain}")
                return True
            else:
                self.logger.warning(f"[WARNING] Referer not detected. Expected: {expected_referer}, Actual: {actual_referer}")
                self.logger.warning(f"[DEBUG] Expected domain: {expected_domain}, Actual domain: {actual_domain}")
                return False
                
        except Exception as e:
            self.logger.warning(f"Could not verify referer: {e}")
            return False
    
    def browse_article_content(self, duration_minutes=None, enable_post_navigation=True):
        """Browse article content with natural reading behavior and post navigation for AdSense RPM optimization"""
        try:
            # Calculate reading duration based on article length if not specified
            if duration_minutes is None:
                duration_minutes = self._calculate_reading_duration()
            
            self.logger.info(f"Browsing article content for {duration_minutes:.1f} minutes (based on article length)")
            
            # Track current post
            current_url = self.driver.current_url
            if current_url not in self.visited_posts:
                self.visited_posts.append(current_url)
                self.logger.info(f"[NOTE] Added initial post to visited list: {current_url}")
                self.logger.info(f"[STATS] Current visited posts count: {len(self.visited_posts)}")
            
            # Use natural article reading behavior instead of random actions
            success = self._natural_article_reading(duration_minutes)
            
            if success:
                self.logger.info("Natural article reading completed successfully")
                
                # Optional: Add some additional natural behaviors after reading
                if random.random() < 0.3:  # 30% chance for additional behaviors
                    self._post_reading_behaviors()
                
                # Enable post navigation for AdSense RPM optimization
                if enable_post_navigation:
                    self.logger.info("[PROCESS] Starting post navigation for AdSense RPM optimization")
                    self.logger.info(f"[STATS] Target: {self.min_posts_per_session}-{self.max_posts_per_session} posts per session")
                    
                    navigation_success = self._navigate_to_other_posts()
                    if navigation_success:
                        self.logger.info("[SUCCESS] Post navigation completed successfully")
                    else:
                        self.logger.info("[INFO] Post navigation completed (no more posts found)")
                    
                    # Check if minimum posts requirement is met
                    if len(self.visited_posts) < self.min_posts_per_session:
                        self.logger.warning(f"[WARNING] Only visited {len(self.visited_posts)} posts (minimum required: {self.min_posts_per_session})")
                        self.logger.info(f"[LIST] Visited posts URLs: {self.visited_posts}")
                    else:
                        self.logger.info(f"[SUCCESS] Successfully visited {len(self.visited_posts)} posts (minimum: {self.min_posts_per_session})")
                        self.logger.info(f"[LIST] Visited posts URLs: {self.visited_posts}")
                
                return True
            else:
                self.logger.warning("Natural article reading failed, falling back to basic browsing")
                return self._fallback_browsing_behavior(duration_minutes)
            
        except Exception as e:
            self.logger.error(f"Error browsing article content: {e}")
            return False
    
    def _navigate_to_other_posts(self):
        """Navigate to other posts (previous, next, related) for AdSense RPM optimization"""
        try:
            self.logger.info("[SCAN] Searching for other posts to navigate to")
            self.logger.info(f"[STATS] Current visited posts count: {len(self.visited_posts)}")
            self.logger.info(f"[LIST] Current visited posts: {self.visited_posts}")
            
            # Find navigation links
            navigation_links = self.post_navigator.find_navigation_links()
            
            if not any([navigation_links['previous'], navigation_links['next'], navigation_links['related']]):
                self.logger.info("[INFO] No navigation links found")
                return False
            
            # Decide which post to navigate to
            available_options = []
            
            if navigation_links['previous']:
                href = navigation_links['previous'].get_attribute('href')
                if href and href not in self.visited_posts:
                    available_options.append(('previous', navigation_links['previous']))
            
            if navigation_links['next']:
                href = navigation_links['next'].get_attribute('href')
                if href and href not in self.visited_posts:
                    available_options.append(('next', navigation_links['next']))
            
            if navigation_links['related']:
                for link in navigation_links['related']:
                    href = link.get_attribute('href')
                    if href and href not in self.visited_posts:
                        available_options.append(('related', link))
                        break  # Only take first related post
            
            if not available_options:
                self.logger.info("[INFO] No new posts available to navigate to")
                return False
            
            # Choose a post to navigate to (prefer next > related > previous)
            chosen_post = None
            for post_type in ['next', 'related', 'previous']:
                for option_type, link in available_options:
                    if option_type == post_type:
                        chosen_post = (option_type, link)
                        break
                if chosen_post:
                    break
            
            if not chosen_post:
                chosen_post = available_options[0]  # Fallback to first available
            
            post_type, link_element = chosen_post
            
            # Navigate to the chosen post
            self.logger.info(f"[LINK] Navigating to {post_type} post for AdSense RPM optimization")
            navigation_success = self.post_navigator.navigate_to_post(link_element, post_type)
            
            if navigation_success:
                # Track the new post URL immediately after successful navigation
                current_url = self.driver.current_url
                if current_url not in self.visited_posts:
                    self.visited_posts.append(current_url)
                    self.logger.info(f"[NOTE] Added post to visited list: {current_url}")
                    self.logger.info(f"[STATS] Current visited posts count: {len(self.visited_posts)}")
                
                # Calculate reading duration based on article length
                reading_duration = self._calculate_reading_duration()
                self.logger.info(f"[READ] Reading {post_type} post for {reading_duration:.1f} minutes (based on article length)")
                
                # Use natural article reading instead of simple simulation
                reading_success = self._natural_article_reading(reading_duration)
                
                if reading_success:
                    self.logger.info(f"[SUCCESS] Successfully read {post_type} post")
                    
                    # Check for ads after reading each post
                    if random.random() < 0.3:  # 30% chance to check for ads after each post
                        self.logger.info("[SCAN] Checking for Google AdSense ads after post reading...")
                        clicked_ads = self.ad_clicker.click_ads(max_clicks=1, conservative=True)
                        if clicked_ads:
                            self.logger.info(f"[SUCCESS] Clicked {len(clicked_ads)} Google AdSense ads after post reading")
                        else:
                            self.logger.info("[INFO] No suitable Google AdSense ads found after post reading")
                    
                    # Check if we need to continue (minimum posts requirement)
                    if len(self.visited_posts) < self.min_posts_per_session:
                        self.logger.info(f"[PROCESS] Need to read more posts (minimum: {self.min_posts_per_session}, current: {len(self.visited_posts)})")
                        return self._navigate_to_other_posts()
                    elif len(self.visited_posts) < self.max_posts_per_session:
                        # Optional: continue if more posts available
                        if random.random() < 0.6:  # 60% chance to continue
                            self.logger.info(f"[PROCESS] Continuing to read more posts (current: {len(self.visited_posts)}/{self.max_posts_per_session})")
                            return self._navigate_to_other_posts()
                        else:
                            self.logger.info(f"[INFO] Stopping after {len(self.visited_posts)} posts (user choice)")
                            return True
                    else:
                        self.logger.info(f"[INFO] Reached maximum posts per session ({self.max_posts_per_session})")
                        return True
                else:
                    self.logger.warning(f"[WARNING] Failed to read {post_type} post")
                    return False
            else:
                self.logger.warning(f"[WARNING] Failed to navigate to {post_type} post")
                return False
                
        except Exception as e:
            self.logger.error(f"Error navigating to other posts: {e}")
            return False
    
    def _calculate_reading_duration(self):
        """Calculate reading duration based on article length (4-10 minutes)"""
        try:
            self.logger.info("[ANALYZE] Analyzing article length to determine reading duration")
            
            # Get article text content
            article_text = self._get_article_text()
            
            if not article_text:
                # Fallback to default duration from configuration
                default_duration = self.config.get('reading.default_reading_time', random.uniform(4.0, 6.0))
                self.logger.info(f"[ANALYZE] No article text found, using default duration: {default_duration:.1f} minutes")
                return default_duration
            
            # Calculate reading metrics
            word_count = len(article_text.split())
            char_count = len(article_text)
            
            # Realistic reading speed based on content type and language
            # Technical content: 100-150 WPM, General content: 150-250 WPM
            content_type = "general"  # Default
            language = "english"  # Default
            
            if self.config.get('reading.content_type_detection', True):
                content_type = self._detect_content_type(article_text)
            
            if self.config.get('reading.language_detection', True):
                language = self._detect_language(article_text)
            
            # Get reading speed from configuration
            if content_type == "technical":
                speed_range = self.config.get('reading.reading_speed_technical', (100, 150))
                avg_reading_speed = random.uniform(speed_range[0], speed_range[1])
            elif content_type == "news":
                speed_range = self.config.get('reading.reading_speed_news', (150, 200))
                avg_reading_speed = random.uniform(speed_range[0], speed_range[1])
            else:
                speed_range = self.config.get('reading.reading_speed_general', (150, 250))
                avg_reading_speed = random.uniform(speed_range[0], speed_range[1])
            
            # Adjust for language using configuration
            if language == "indonesian":
                multiplier = self.config.get('reading.indonesian_speed_multiplier', 0.8)
                avg_reading_speed *= multiplier
            elif language == "english":
                multiplier = self.config.get('reading.english_speed_multiplier', 1.0)
                avg_reading_speed *= multiplier
            
            # Calculate base reading time
            base_reading_time = word_count / avg_reading_speed
            
            # Apply minimum and maximum constraints from configuration
            min_reading_time = self.config.get('reading.min_reading_time', 4.0)
            max_reading_time = self.config.get('reading.max_reading_time', 10.0)
            
            # Clamp the reading time
            reading_time = max(min_reading_time, min(max_reading_time, base_reading_time))
            
            # Add some natural variation (+/-10%)
            variation = random.uniform(0.9, 1.1)
            final_reading_time = reading_time * variation
            
            # Ensure it's within bounds after variation
            final_reading_time = max(min_reading_time, min(max_reading_time, final_reading_time))
            
            self.logger.info(f"[ANALYZE] Article Analysis:")
            self.logger.info(f"   Word Count: {word_count}")
            self.logger.info(f"   Character Count: {char_count}")
            self.logger.info(f"   Reading Speed: {avg_reading_speed:.0f} words/min")
            self.logger.info(f"   Base Reading Time: {base_reading_time:.1f} minutes")
            self.logger.info(f"   Final Reading Time: {final_reading_time:.1f} minutes")
            
            return final_reading_time
            
        except Exception as e:
            self.logger.error(f"Error calculating reading duration: {e}")
            # Fallback to default duration from configuration
            default_duration = self.config.get('reading.default_reading_time', random.uniform(4.0, 6.0))
            self.logger.info(f"[ANALYZE] Using fallback duration: {default_duration:.1f} minutes")
            return default_duration
    
    def _get_article_text(self):
        """Extract article text content for length analysis"""
        try:
            # Try multiple selectors to find article content (updated for modern websites)
            article_selectors = [
                # HTML5 semantic elements
                'article', 'main', 'section',
                
                # WordPress selectors
                '.post-content', '.entry-content', '.article-content', '.wp-content',
                '.content-area', '.site-content', '.main-content', '.single-post',
                '.post-body', '.entry-body', '.article-body', '.post-text',
                '.entry-text', '.article-text', '.post', '.entry',
                
                # Blog platform selectors
                '.blog-post', '.news-article', '.story-content', '.text-content',
                '.post-content', '.entry-content', '.article-content',
                
                # CMS specific selectors
                '.content', '.main-content', '.primary-content', '.page-content',
                '.article-content', '.post-content', '.entry-content',
                
                # Framework selectors
                '.content-wrapper', '.content-container', '.main-wrapper',
                '.article-wrapper', '.post-wrapper', '.entry-wrapper',
                
                # Generic content selectors
                '.content', '.text', '.body', '.main', '.primary'
            ]
            
            article_text = ""
            
            for selector in article_selectors:
                try:
                    elements = self.driver.find_elements("css selector", selector)
                    for element in elements:
                        text = element.text.strip()
                        if len(text) > len(article_text):
                            article_text = text
                except:
                    continue
            
            # If no specific article content found, try to get body text
            if not article_text or len(article_text) < 100:
                try:
                    body_element = self.driver.find_element("tag name", "body")
                    article_text = body_element.text.strip()
                except:
                    pass
            
            # Clean up the text
            if article_text:
                # Remove extra whitespace and newlines
                article_text = ' '.join(article_text.split())
                
                # Limit text length for analysis (first 5000 characters)
                if len(article_text) > 5000:
                    article_text = article_text[:5000]
            
            if article_text and len(article_text) > 50:
                self.logger.info(f"[ANALYZE] Extracted article text: {len(article_text)} characters")
                return article_text
            else:
                self.logger.warning("[ANALYZE] Could not extract sufficient article text")
                return None
                
        except Exception as e:
            self.logger.error(f"Error extracting article text: {e}")
            return None
    
    def _detect_content_type(self, article_text):
        """Detect content type based on text analysis"""
        try:
            if not article_text:
                return "general"
            
            # Technical content indicators
            technical_keywords = [
                'algorithm', 'function', 'method', 'class', 'variable', 'parameter',
                'code', 'programming', 'development', 'software', 'technical',
                'implementation', 'architecture', 'framework', 'library', 'API',
                'database', 'server', 'client', 'protocol', 'interface'
            ]
            
            # News content indicators
            news_keywords = [
                'news', 'report', 'breaking', 'latest', 'update', 'announcement',
                'press', 'statement', 'official', 'government', 'minister',
                'president', 'election', 'vote', 'campaign', 'policy'
            ]
            
            text_lower = article_text.lower()
            
            # Count technical keywords
            technical_count = sum(1 for keyword in technical_keywords if keyword in text_lower)
            
            # Count news keywords
            news_count = sum(1 for keyword in news_keywords if keyword in text_lower)
            
            # Determine content type
            if technical_count >= 3:
                return "technical"
            elif news_count >= 3:
                return "news"
            else:
                return "general"
                
        except Exception as e:
            self.logger.warning(f"Error detecting content type: {e}")
            return "general"
    
    def _detect_language(self, article_text):
        """Detect language based on text analysis"""
        try:
            if not article_text:
                return "english"
            
            # Indonesian indicators
            indonesian_words = [
                'yang', 'dan', 'dengan', 'untuk', 'dari', 'pada', 'adalah',
                'akan', 'telah', 'sudah', 'belum', 'tidak', 'bukan',
                'ini', 'itu', 'saya', 'kamu', 'dia', 'kita', 'mereka'
            ]
            
            # Count Indonesian words
            text_lower = article_text.lower()
            indonesian_count = sum(1 for word in indonesian_words if word in text_lower)
            
            # If more than 5 Indonesian words found, likely Indonesian
            if indonesian_count >= 5:
                return "indonesian"
            else:
                return "english"
                
        except Exception as e:
            self.logger.warning(f"Error detecting language: {e}")
            return "english"
    
    def _detect_content_complexity(self, article_text):
        """Detect content complexity for thinking behavior"""
        try:
            if not article_text:
                return "simple"
            
            # Complexity indicators
            complex_indicators = [
                'algorithm', 'analysis', 'methodology', 'framework', 'architecture',
                'implementation', 'optimization', 'analysis', 'evaluation', 'assessment',
                'theoretical', 'conceptual', 'abstract', 'sophisticated', 'advanced',
                'complex', 'intricate', 'detailed', 'comprehensive', 'thorough'
            ]
            
            # Technical indicators
            technical_indicators = [
                'function', 'variable', 'parameter', 'class', 'method', 'interface',
                'protocol', 'database', 'server', 'client', 'API', 'library',
                'framework', 'architecture', 'design pattern', 'algorithm'
            ]
            
            text_lower = article_text.lower()
            
            # Count complexity indicators
            complex_count = sum(1 for indicator in complex_indicators if indicator in text_lower)
            technical_count = sum(1 for indicator in technical_indicators if indicator in text_lower)
            
            # Determine complexity level
            if complex_count >= 5 or technical_count >= 8:
                return "complex"
            elif complex_count >= 2 or technical_count >= 4:
                return "moderate"
            else:
                return "simple"
                
        except Exception as e:
            self.logger.warning(f"Error detecting content complexity: {e}")
            return "simple"
    
    def _detect_sentence_complexity(self, article_text):
        """Detect sentence complexity for thinking behavior"""
        try:
            if not article_text:
                return "simple"
            
            # Split into sentences
            sentences = article_text.split('.')
            complex_sentences = 0
            
            for sentence in sentences:
                if len(sentence.split()) > 25:  # Long sentences
                    complex_sentences += 1
                elif ',' in sentence and len(sentence.split()) > 15:  # Complex structure
                    complex_sentences += 1
                elif any(word in sentence.lower() for word in ['however', 'therefore', 'although', 'because', 'since']):
                    complex_sentences += 1
            
            # Determine complexity
            if complex_sentences >= len(sentences) * 0.3:  # 30% complex sentences
                return "complex"
            elif complex_sentences >= len(sentences) * 0.15:  # 15% complex sentences
                return "moderate"
            else:
                return "simple"
                
        except Exception as e:
            self.logger.warning(f"Error detecting sentence complexity: {e}")
            return "simple"
    
    def _detect_concept_importance(self, article_text):
        """Detect concept importance for thinking behavior"""
        try:
            if not article_text:
                return "low"
            
            # Importance indicators
            importance_indicators = [
                'important', 'crucial', 'essential', 'vital', 'significant',
                'key', 'critical', 'fundamental', 'core', 'primary',
                'main', 'principal', 'central', 'major', 'substantial'
            ]
            
            # New concept indicators
            new_concept_indicators = [
                'new', 'novel', 'innovative', 'breakthrough', 'discovery',
                'introduction', 'emerging', 'cutting-edge', 'latest', 'recent'
            ]
            
            text_lower = article_text.lower()
            
            # Count importance indicators
            importance_count = sum(1 for indicator in importance_indicators if indicator in text_lower)
            new_concept_count = sum(1 for indicator in new_concept_indicators if indicator in text_lower)
            
            # Determine importance level
            if importance_count >= 5 or new_concept_count >= 3:
                return "high"
            elif importance_count >= 2 or new_concept_count >= 1:
                return "medium"
            else:
                return "low"
                
        except Exception as e:
            self.logger.warning(f"Error detecting concept importance: {e}")
            return "low"
    
    def _simulate_thinking_behavior(self, article_text=None, context="reading"):
        """Unified thinking behavior simulation with context awareness"""
        try:
            if not self.config.get('reading.thinking.enable_thinking', True):
                return False
            
            # Detect thinking context
            thinking_context = self._analyze_thinking_context(article_text)
            
            # Determine thinking type based on context
            thinking_type = self._determine_thinking_type(thinking_context)
            
            if thinking_type:
                # Execute thinking behavior
                self._execute_thinking_behavior(thinking_type, thinking_context)
                return True
            
            return False
            
        except Exception as e:
            self.logger.warning(f"Error in thinking behavior simulation: {e}")
            return False
    
    def _analyze_thinking_context(self, article_text):
        """Analyze context for thinking behavior"""
        try:
            context = {
                'content_complexity': 'simple',
                'sentence_complexity': 'simple',
                'concept_importance': 'low',
                'topic_familiarity': 'familiar'
            }
            
            if article_text and self.config.get('reading.thinking.thinking_context.content_complexity_detection', True):
                context['content_complexity'] = self._detect_content_complexity(article_text)
            
            if article_text and self.config.get('reading.thinking.thinking_context.sentence_complexity_detection', True):
                context['sentence_complexity'] = self._detect_sentence_complexity(article_text)
            
            if article_text and self.config.get('reading.thinking.thinking_context.concept_importance_detection', True):
                context['concept_importance'] = self._detect_concept_importance(article_text)
            
            return context
            
        except Exception as e:
            self.logger.warning(f"Error analyzing thinking context: {e}")
            return {'content_complexity': 'simple', 'sentence_complexity': 'simple', 'concept_importance': 'low', 'topic_familiarity': 'familiar'}
    
    def _determine_thinking_type(self, context):
        """Determine thinking type based on context"""
        try:
            thinking_types = self.config.get('reading.thinking.thinking_types', {})
            
            # Quick processing for simple content
            if context['content_complexity'] == 'simple' and context['concept_importance'] == 'low':
                if random.random() < thinking_types.get('quick_processing', {}).get('chance', 0.15):
                    return 'quick_processing'
            
            # Analytical thinking for complex content
            elif context['content_complexity'] == 'complex' or context['sentence_complexity'] == 'complex':
                if random.random() < thinking_types.get('analytical_thinking', {}).get('chance', 0.20):
                    return 'analytical_thinking'
            
            # Deep contemplation for important content
            elif context['concept_importance'] == 'high':
                if random.random() < thinking_types.get('deep_contemplation', {}).get('chance', 0.08):
                    return 'deep_contemplation'
            
            # Processing information for new information
            elif context['content_complexity'] == 'moderate' or context['sentence_complexity'] == 'moderate':
                if random.random() < thinking_types.get('processing_information', {}).get('chance', 0.25):
                    return 'processing_information'
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error determining thinking type: {e}")
            return None
    
    def _execute_thinking_behavior(self, thinking_type, context):
        """Execute specific thinking behavior"""
        try:
            thinking_config = self.config.get('reading.thinking.thinking_types', {}).get(thinking_type, {})
            
            if not thinking_config:
                return False
            
            # Get thinking pause timing
            pause_min = thinking_config.get('pause_min', 1.0)
            pause_max = thinking_config.get('pause_max', 3.0)
            thinking_pause = random.uniform(pause_min, pause_max)
            
            # Log thinking behavior
            self.logger.info(f"[THINKING] {thinking_type.replace('_', ' ').title()}: {thinking_pause:.1f}s")
            
            # Execute thinking behavior
            if self.config.get('reading.thinking.thinking_behavior.mouse_movement_during_thinking', True):
                self._thinking_mouse_behavior(thinking_pause)
            
            if self.config.get('reading.thinking.thinking_behavior.eye_tracking_simulation', True):
                self._thinking_eye_tracking(thinking_pause)
            
            if self.config.get('reading.thinking.thinking_behavior.micro_movements', True):
                self._thinking_micro_movements(thinking_pause)
            
            if self.config.get('reading.thinking.thinking_behavior.breathing_pattern_simulation', True):
                self._thinking_breathing_pattern(thinking_pause)
            
            # Main thinking pause
            time.sleep(thinking_pause)
            
            return True
            
        except Exception as e:
            self.logger.warning(f"Error executing thinking behavior: {e}")
            return False
    
    def _thinking_mouse_behavior(self, duration):
        """Mouse behavior during thinking"""
        try:
            # Slow, deliberate mouse movements during thinking
            movements = random.randint(2, 5)
            for _ in range(movements):
                if random.random() < 0.3:  # 30% chance for mouse movement
                    self.mouse.random_mouse_movement(random.uniform(0.5, 1.0))
                    time.sleep(random.uniform(0.2, 0.5))
        except Exception as e:
            self.logger.debug(f"Error in thinking mouse behavior: {e}")
    
    def _thinking_eye_tracking(self, duration):
        """Eye tracking simulation during thinking"""
        try:
            # Simulate eye movements during thinking
            eye_movements = random.randint(1, 3)
            for _ in range(eye_movements):
                # Simulate looking around while thinking
                scroll_amount = random.randint(-50, 50)
                self.driver.execute_script(f"window.scrollBy({{top: {scroll_amount}, behavior: 'smooth'}});")
                time.sleep(random.uniform(0.3, 0.8))
        except Exception as e:
            self.logger.debug(f"Error in thinking eye tracking: {e}")
    
    def _thinking_micro_movements(self, duration):
        """Micro-movements during thinking"""
        try:
            # Subtle micro-movements during thinking
            micro_movements = random.randint(1, 3)
            for _ in range(micro_movements):
                if random.random() < 0.4:  # 40% chance for micro-movement
                    self.mouse.random_mouse_movement(random.uniform(0.1, 0.3))
                    time.sleep(random.uniform(0.1, 0.2))
        except Exception as e:
            self.logger.debug(f"Error in thinking micro-movements: {e}")
    
    def _thinking_breathing_pattern(self, duration):
        """Breathing pattern simulation during thinking"""
        try:
            # Simulate breathing pattern with subtle movements
            breathing_cycles = int(duration * 2)  # 2 cycles per second
            for _ in range(breathing_cycles):
                if random.random() < 0.2:  # 20% chance for breathing movement
                    # Subtle movement to simulate breathing
                    self.mouse.random_mouse_movement(random.uniform(0.05, 0.15))
                time.sleep(0.5)
        except Exception as e:
            self.logger.debug(f"Error in thinking breathing pattern: {e}")
    
    def get_post_navigation_stats(self):
        """Get statistics about post navigation for AdSense RPM optimization"""
        try:
            stats = {
                'total_posts_visited': len(self.visited_posts),
                'min_posts_per_session': self.min_posts_per_session,
                'max_posts_per_session': self.max_posts_per_session,
                'posts_remaining': self.max_posts_per_session - len(self.visited_posts),
                'minimum_met': len(self.visited_posts) >= self.min_posts_per_session,
                'visited_urls': self.visited_posts.copy()
            }
            
            self.logger.info("[STATS] Post Navigation Statistics:")
            self.logger.info(f"   Total Posts Visited: {stats['total_posts_visited']}")
            self.logger.info(f"   Min Posts Required: {stats['min_posts_per_session']}")
            self.logger.info(f"   Max Posts Per Session: {stats['max_posts_per_session']}")
            self.logger.info(f"   Posts Remaining: {stats['posts_remaining']}")
            self.logger.info(f"   Minimum Requirement Met: {'[SUCCESS] Yes' if stats['minimum_met'] else '[ERROR] No'}")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting post navigation stats: {e}")
            return None
    
    def _post_reading_behaviors(self):
        """Additional natural behaviors after reading"""
        try:
            self.logger.info("Performing post-reading behaviors")
            
            # Check for ads after reading (higher chance)
            if random.random() < 0.4:  # 40% chance to check for ads after reading
                self.logger.info("[SCAN] Checking for Google AdSense ads after reading...")
                clicked_ads = self.ad_clicker.click_ads(max_clicks=1, conservative=True)
                if clicked_ads:
                    self.logger.info(f"[SUCCESS] Clicked {len(clicked_ads)} Google AdSense ads after reading")
                else:
                    self.logger.info("[INFO] No suitable Google AdSense ads found after reading")
            
            # Random post-reading actions
            actions = [
                'scroll_to_top', 'scroll_to_bottom', 'careful_scan', 
                'mouse_exploration', 'pause_and_think'
            ]
            
            selected_actions = random.sample(actions, random.randint(1, 3))
            
            for action in selected_actions:
                if action == 'scroll_to_top':
                    self._human_like_scroll_to_position(0, duration=2.0)
                    time.sleep(random.uniform(2.0, 4.0))
                    
                elif action == 'scroll_to_bottom':
                    page_height = self.driver.execute_script("return document.body.scrollHeight")
                    self._human_like_scroll_to_position(page_height, duration=2.0)
                    time.sleep(random.uniform(2.0, 4.0))
                    
                elif action == 'careful_scan':
                    self._careful_content_scan()
                    
                elif action == 'mouse_exploration':
                    self._natural_mouse_tracking()
                    
                elif action == 'pause_and_think':
                    # UNIFIED THINKING BEHAVIOR
                    if self._simulate_thinking_behavior(article_text, "pause_and_think"):
                        pass  # Thinking behavior already executed in _simulate_thinking_behavior
                
                # Small pause between actions
                time.sleep(random.uniform(1.0, 2.5))
            
        except Exception as e:
            self.logger.warning(f"Error in post-reading behaviors: {e}")
    
    def _fallback_browsing_behavior(self, duration_minutes=5):
        """Fallback browsing behavior if natural reading fails"""
        try:
            self.logger.info("Using fallback browsing behavior")
            
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            while time.time() < end_time:
                # Check risk before each action
                signals = self.risk_monitor.check_detection_signals()
                if not self.risk_monitor.handle_risk(signals):
                    self.logger.warning("Risk handling prevented action")
                    continue
                
                # Simple, safe actions
                action = random.choice(['scroll', 'mouse_move', 'pause'])
                
                if action == 'scroll':
                    # Simple scroll behavior
                    scroll_amount = random.randint(100, 300)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(2.0, 5.0))
                    
                elif action == 'mouse_move':
                    self.mouse.random_mouse_movement(random.uniform(0.5, 1.5))
                    
                elif action == 'pause':
                    pause_duration = random.uniform(3.0, 8.0)
                    time.sleep(pause_duration)
                
                # Wait between actions
                time.sleep(random.uniform(1.0, 3.0))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in fallback browsing behavior: {e}")
            return False
    
    def _try_click_random_link(self):
        try:
            # Find clickable links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            clickable_links = []
            
            for link in links:
                try:
                    if link.is_displayed() and link.is_enabled():
                        href = link.get_attribute("href")
                        if href and not href.startswith("javascript:"):
                            clickable_links.append(link)
                except:
                    continue
            
            if clickable_links:
                random_link = random.choice(clickable_links)
                
                # Move mouse to link
                self.mouse.move_to_element(random_link)
                self.timing.wait_between_actions(0.5, 1.5)
                
                # Click link
                random_link.click()
                self.risk_monitor.record_request()
                
                # Wait for page load
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                self.logger.info("Clicked random link successfully")
                
        except Exception as e:
            self.logger.warning(f"Error clicking random link: {e}")
    
    
    def _navigate_to_next_post(self):
        """Navigate to next post menggunakan multiple selector strategies"""
        try:
            # Try different selector strategies
            for selector in self.patterns.navigation_patterns['next']:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if self._is_valid_navigation_element(element, "next"):
                            if self._click_navigation_element(element, "next"):
                                return True
                                
                except Exception as e:
                    continue
            
            return False
            
        except Exception as e:
            return False
    
    def _navigate_to_previous_post(self):
        """Navigate to previous post menggunakan multiple selector strategies"""
        try:
            # Try different selector strategies
            for selector in self.patterns.navigation_patterns['previous']:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if self._is_valid_navigation_element(element, "previous"):
                            if self._click_navigation_element(element, "previous"):
                                return True
                                
                except Exception as e:
                    continue
            
            return False
            
        except Exception as e:
            return False
    
    def _is_valid_navigation_element(self, element, direction):
        """Validate navigation element"""
        try:
            # Check if element is visible and clickable
            if not element.is_displayed():
                return False
            
            # Check if element has valid href
            href = element.get_attribute('href')
            if not href or href == '#' or 'javascript:void(0)' in href:
                return False
            
            # Check if element is in viewport
            location = element.location
            if location['x'] < 0 or location['y'] < 0:
                return False
            
            # Check element size
            size = element.size
            if size['width'] < 10 or size['height'] < 10:
                return False
            
            return True
            
        except Exception as e:
            return False
    
    def _click_navigation_element(self, element, direction):
        """Click navigation element dengan human-like behavior"""
        try:
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            
            # Wait for element to be clickable
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable(element))
            
            # Add human-like delay
            delay = self.timing.human_like_delay("clicking")
            time.sleep(delay)
            
            # Use mouse simulator for human-like clicking
            if self.mouse.move_to_element(element):
                element.click()
                
                # Wait for page load
                time.sleep(self.timing.human_like_delay("navigation"))
                
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def _find_and_click_random_link(self, same_domain=True, max_attempts=5):
        """Find and click a random link on the page"""
        try:
            # Get current domain
            current_url = self.driver.current_url
            current_domain = urlparse(current_url).netloc
            
            # Find all link elements
            link_elements = self.driver.find_elements(By.TAG_NAME, "a")
            valid_links = []
            
            for element in link_elements:
                try:
                    href = element.get_attribute("href")
                    if not href or "javascript:void(0)" in href:
                        continue
                    
                    # Check if element is visible and displayed
                    if not element.is_displayed():
                        continue
                    
                    # Test if element is clickable
                    WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(element))
                    
                    # Check domain if required
                    if same_domain:
                        try:
                            element_domain = urlparse(href).netloc
                            if element_domain and element_domain != current_domain:
                                continue
                        except:
                            # Assume relative URL if parsing fails
                            pass
                    
                    valid_links.append(element)
                    
                except Exception as e:
                    continue
            
            if not valid_links:
                return False
            
            # Select random link
            random_link = random.choice(valid_links)
            
            # Click the link
            if self._click_navigation_element(random_link, "random"):
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    
    def open_article_with_referer(self, article_url=None, referer_url=None):
        """
        Open any article with referer - domain agnostic
        
        Args:
            article_url (str): URL of the article to open (if None, uses default)
            referer_url (str): Referer URL to use (if None, randomly selects)
        """
        # Default article URL if not provided - support array and random selection
        if article_url is None:
            article_url = self.get_random_article_url()
            self.logger.info(f"[RANDOM] Randomly selected article URL: {article_url}")
        
        # Default referer options if not provided - favor high CPC sources
        if referer_url is None:
            high_cpc_weight = self.get_high_cpc_weight()
            referer_url = self.get_weighted_referer_url()
            self.logger.info(f"[RANDOM] Weighted selected referer URL ({high_cpc_weight*100:.0f}% high CPC): {referer_url}")
        
        self.logger.info(f"Opening article: {article_url} with referer: {referer_url}")
        
        # REAL REFERER FLOW: 1. Buka referer 2. Navigate ke article (referer akan terkirim otomatis)
        success = False
        
        try:
            self.logger.info("[PROCESS] Starting REAL referer flow: 1. Buka referer 2. Navigate ke article")
            success = self._real_referer_flow(article_url, referer_url)
            if success:
                self.logger.info("[SUCCESS] Article opened successfully with REAL referer flow")
        except Exception as e:
            self.logger.warning(f"Real referer flow failed: {e}")
        
        # Fallback: Try proxy referer flow
        if not success:
            try:
                self.logger.info("Trying proxy referer flow as fallback")
                success = self._proxy_referer_flow(article_url, referer_url)
                if success:
                    self.logger.info("[SUCCESS] Article opened successfully with proxy referer flow")
            except Exception as e:
                self.logger.warning(f"Proxy referer flow failed: {e}")
        
        # Final fallback: Direct navigation
        if not success:
            try:
                self.logger.info("Trying direct navigation as final fallback")
                self.driver.get(article_url)
                
                # Longer pause for direct navigation
                self.logger.info("Waiting for article page to load completely (direct navigation)")
                time.sleep(10)
                
                current_url = self.driver.current_url
                if article_url in current_url:
                    success = True
                    self.logger.info("[SUCCESS] Direct navigation successful")
                    
                    # Additional pause after successful direct navigation
                    self.logger.info("Additional pause for article stabilization (direct navigation)")
                    time.sleep(5)
                else:
                    self.logger.error(f"[ERROR] Direct navigation failed. Current URL: {current_url}")
            except Exception as e:
                self.logger.error(f"Direct navigation failed: {e}")
        
        if success:
            # Enable post navigation for AdSense RPM optimization with dynamic reading duration
            browse_success = self.browse_article_content(duration_minutes=None, enable_post_navigation=True)
            if browse_success:
                self.logger.info("Article browsing with post navigation completed successfully")
                self.logger.info(f"[STATS] Total posts visited: {len(self.visited_posts)}")
                return True
            else:
                self.logger.error("Article browsing failed")
                return False
        else:
            self.logger.error("Failed to open article")
            return False
    
    def set_article_urls(self, article_urls):
        """Set the article URLs array to be used for browsing (random selection)"""
        if isinstance(article_urls, str):
            # Convert single URL to array
            article_urls = [article_urls]
        self.config.config['article']['default_urls'] = article_urls
        self.logger.info(f"Article URLs set to: {article_urls}")
    
    def set_article_url(self, article_url):
        """Set a single article URL (converts to array for compatibility)"""
        self.set_article_urls([article_url])
    
    def set_referer_options(self, referer_options):
        """Set the referer options to be used for browsing"""
        self.config.config['article']['default_referers'] = referer_options
        self.logger.info(f"Referer options set to: {referer_options}")
    
    def set_high_cpc_weight(self, weight):
        """Set the weight for high CPC referer selection (0.0-1.0)"""
        if not 0.0 <= weight <= 1.0:
            raise ValueError("Weight must be between 0.0 and 1.0")
        self.config.config['article']['high_cpc_weight'] = weight
        self.logger.info(f"High CPC weight set to: {weight}")
    
    def get_high_cpc_weight(self):
        """Get the current high CPC weight"""
        return self.config.get('article.high_cpc_weight', 0.7)
    
    def get_random_article_url(self):
        """Get a random article URL from the configured list"""
        article_urls = self.config.get('article.default_urls', ['https://gengsego.com/'])
        return random.choice(article_urls)
    
    def get_random_referer_url(self):
        """Get a random referer URL from the configured list"""
        referer_options = self.config.get('article.default_referers', [
            'https://google.com', 'https://bing.com', 'https://linkedin.com', 'https://github.com', 
            'https://stackoverflow.com', 'https://medium.com', 'https://quora.com', 'https://forbes.com',
            'https://bloomberg.com', 'https://reuters.com', 'https://wsj.com', 'https://techcrunch.com',
            'https://wired.com', 'https://arstechnica.com', 'https://hbr.org', 'https://mckinsey.com',
            'https://pwc.com', 'https://deloitte.com', 'https://kpmg.com', 'https://ey.com',
            'https://ibm.com', 'https://microsoft.com', 'https://oracle.com', 'https://salesforce.com',
            'https://adobe.com', 'https://intel.com', 'https://nvidia.com', 'https://amd.com',
            'https://cisco.com', 'https://aws.amazon.com', 'https://cloud.google.com', 'https://azure.microsoft.com',
        ])
        return random.choice(referer_options)
    
    def get_high_cpc_referer_url(self):
        """Get a random referer URL from high CPC sources (Business/Finance/Tech)"""
        high_cpc_referers = [
            # 'https://www.coindesk.com/markets/2025/09/15/dogecoin-inches-closer-to-wall-street-with-first-meme-coin-etf',
            # 'https://www.coindesk.com/business/2025/09/18/ripple-franklin-templeton-and-dbs-to-offer-token-lending-and-trading',
            # 'https://coinledger.io/tools/best-crypto-wallet',
            # 'https://money.com/best-crypto-wallets/',
            # 'https://shop.ledger.com/products/ledger-flex/graphite',
            # 'https://hellopebl.com/resources/blog/best-crypto-wallets/',
            # 'https://www.forbes.com/advisor/investing/cryptocurrency/best-crypto-wallets/',
            # 'https://www.nerdwallet.com/p/best/investing/crypto-bitcoin-wallets',
            # 'https://www.ig.com/en-ch/trading-strategies/the-5-crypto-trading-strategies-that-every-trader-needs-to-know-221123',
            # 'https://www.gemini.com/cryptopedia/day-trading-crypto',
            # 'https://www.avatrade.com/education/online-trading-strategies/crypto-trading-strategies',
            # 'https://coindcx.com/blog/cryptocurrency/top-crypto-day-trading-strategies/',
            # 'https://bravenewcoin.com/insights/ethereum-eth-price-prediction-ethereum-eyes-5000-as-bullish-cross-meets-fed-rate-cut-speculation',
            # 'https://cointelegraph.com/news/price-predictions-917-btc-eth-xrp-bnb-sol-doge-ada-hype-link-sui',
            # 'https://coinledger.io/tools/best-crypto-portfolio-tracker',
            # 'https://www.litrg.org.uk/savings-property/cryptoassets-and-tax',

            # #insurance
            # 'https://www.usnews.com/insurance/auto/geico-vs-progressive',
            # 'https://www.cnbc.com/select/geico-vs-progressive-car-insurance-which-is-better/',
            # 'https://www.bankrate.com/insurance/reviews/geico-vs-progressive/#is-geico-cheaper-than-progressive',
            # 'https://www.forbes.com/advisor/car-insurance/geico-vs-progressive-car-insurance/',
            # 'https://ca.trustpilot.com/review/www.statefarm.com',
            # 'https://www.usnews.com/insurance/auto/state-farm-car-insurance-review',
            # 'https://www.bankrate.com/insurance/reviews/state-farm/#car-insurance',
            # 'https://www.allstate.ca/car-insurance',
            # 'https://www.allstate.com/auto-insurance',
            # 'https://www.farmers.com/home/',
            # 'https://www.farmers.com/insurance/',
            # 'https://www.usaa.com/inet/wc/insurance-products?akredirect=true',

            'https://rexdl.biz.id/how-to-find-cheap-personal-loan-rates-in-the-us-and-uk-a-complete-up-to-date-guide-2025/',
            'https://rexdl.biz.id/small-business-loans-how-to-choose-what-to-expect-how-to-maximize-value-u-s-u-k/',
            'https://rexdl.biz.id/life-insurance-rates-comparison-the-complete-guide-for-u-s-families-in-2025/',
            'https://rexdl.biz.id/the-ultimate-guide-to-health-insurance-plans-in-the-u-s-compare-save-and-choose-high-cpc-actionable/',
            'https://rexdl.biz.id/business-insurance-quotes-the-ultimate-guide-for-u-s-small-businesses-in-2025/',
            'https://rexdl.biz.id/ai-for-small-business-the-ultimate-guide-to-growth-efficiency-and-profit-in-2025/',
            'https://rexdl.biz.id/ai-customer-service-tools-the-future-of-business-support-in-2025/',

            'https://tokenomics.web.id/tokenomics-bitcoin-btc-apakah-fixed-supply-selalu-aman/',
            'https://tokenomics.web.id/bagaimana-tokenomics-solana-sol-mendorong-skalabilitas/',
            'https://tokenomics.web.id/tokenomics-polygon-matic-layer-2-yang-menjanjikan/',
            'https://tokenomics.web.id/tokenomics-shiba-inu-shib-apakah-burn-rate-mampu-naikkan-harga/',
            'https://tokenomics.web.id/cara-membaca-tokenomics-sebelum-investasi-kripto-panduan-2025/',
            'https://tokenomics.web.id/peran-bappebti-dalam-mengawasi-aset-kripto-di-indonesia/',

            'https://primecapitalaid.web.id/cara-mendapatkan-bantuan-modal-usaha-umkm-tahun-2025-ulasan-teknis-uji-lapangan-dan-tips-lolos-seleksi/',
            'https://primecapitalaid.web.id/bantuan-modal-umkm-khusus-perempuan-program-dan-syaratnya/',
            'https://primecapitalaid.web.id/apa-itu-pinjaman-legal-ini-ciri-cirinya-yang-harus-anda-ketahui/',
            'https://primecapitalaid.web.id/pinjaman-untuk-umkm-usaha-kecil-rekomendasi-pinjaman-legal-terdaftar-ojk-2025/',
        ]
        return random.choice(high_cpc_referers)
    
    def get_medium_cpc_referer_url(self):
        """Get a random referer URL from medium CPC sources (General/Social)"""
        medium_cpc_referers = [
            # Core Business/Finance/Tech
            'https://google.com', 'https://bing.com', 'https://linkedin.com', 'https://github.com', 
            'https://stackoverflow.com', 'https://medium.com', 'https://quora.com', 'https://forbes.com',
            'https://bloomberg.com', 'https://reuters.com', 'https://wsj.com', 'https://techcrunch.com',
            'https://wired.com', 'https://arstechnica.com', 'https://hbr.org', 'https://mckinsey.com',
            'https://pwc.com', 'https://deloitte.com', 'https://kpmg.com', 'https://ey.com',
            'https://ibm.com', 'https://microsoft.com', 'https://oracle.com', 'https://salesforce.com',
            'https://adobe.com', 'https://intel.com', 'https://nvidia.com', 'https://amd.com',
            'https://cisco.com', 'https://aws.amazon.com', 'https://cloud.google.com', 'https://azure.microsoft.com',
            
            # Business/Finance News & Data
            'https://cnbc.com', 'https://marketwatch.com', 'https://investing.com', 'https://yahoo.com/finance',
            'https://finance.yahoo.com', 'https://seekingalpha.com', 'https://benzinga.com', 'https://fool.com',
            'https://morningstar.com', 'https://nasdaq.com', 'https://nyse.com', 'https://sec.gov',
            'https://federalreserve.gov', 'https://treasury.gov', 'https://irs.gov', 'https://sba.gov',
            'https://ftc.gov', 'https://finra.org', 'https://cftc.gov', 'https://fdic.gov', 'https://occ.gov',
            
            # Professional Networks
            'https://angel.co', 'https://crunchbase.com', 'https://pitchbook.com',
            'https://cbinsights.com', 'https://gartner.com', 'https://idc.com',
            
            # Financial Services & Banking
            'https://jpmorgan.com', 'https://bankofamerica.com', 'https://wellsfargo.com', 'https://citigroup.com',
            'https://goldmansachs.com', 'https://morganstanley.com', 'https://blackrock.com', 'https://vanguard.com',
            'https://fidelity.com', 'https://schwab.com', 'https://etrade.com', 'https://tdameritrade.com',
            'https://interactivebrokers.com', 'https://robinhood.com', 'https://webull.com', 'https://sofi.com',
            'https://chase.com', 'https://capitalone.com', 'https://americanexpress.com', 'https://visa.com',
            'https://mastercard.com', 'https://paypal.com', 'https://square.com', 'https://stripe.com',
            
            # Investment & Trading
            'https://trading212.com', 'https://plus500.com', 'https://ig.com', 'https://oanda.com',
            'https://forex.com', 'https://fxcm.com', 'https://businesswire.com', 'https://prnewswire.com',
            'https://globenewswire.com', 'https://otcmarkets.com',
            
            # Technology & Innovation
            'https://apple.com', 'https://amazon.com', 'https://meta.com', 'https://netflix.com',
            'https://tesla.com', 'https://spacex.com', 'https://openai.com', 'https://anthropic.com',
            'https://deepmind.com', 'https://qualcomm.com', 'https://broadcom.com', 'https://juniper.net',
            'https://vmware.com', 'https://redhat.com', 'https://canonical.com', 'https://docker.com',
            'https://kubernetes.io', 'https://terraform.io',
            
            # Cloud & Enterprise Software
            'https://sap.com', 'https://workday.com', 'https://servicenow.com', 'https://atlassian.com',
            'https://slack.com', 'https://zoom.us', 'https://teams.microsoft.com', 'https://dropbox.com',
            'https://box.com', 'https://onedrive.com', 'https://sharepoint.com', 'https://office.com',
            'https://autodesk.com', 'https://ansys.com', 'https://solidworks.com', 'https://tableau.com',
            'https://powerbi.com', 'https://qlik.com',
            
            # Cybersecurity & Data
            'https://crowdstrike.com', 'https://paloaltonetworks.com', 'https://fortinet.com', 'https://checkpoint.com',
            'https://symantec.com', 'https://mcafee.com', 'https://trendmicro.com', 'https://kaspersky.com',
            'https://bitdefender.com', 'https://splunk.com', 'https://elastic.co', 'https://databricks.com',
            'https://snowflake.com', 'https://mongodb.com', 'https://redis.com', 'https://postgresql.org',
            'https://mysql.com', 'https://hpe.com', 'https://dell.com',
            
            # Consulting & Professional Services
            'https://bain.com', 'https://bcg.com', 'https://accenture.com', 'https://cognizant.com',
            'https://infosys.com', 'https://tcs.com', 'https://wipro.com', 'https://capgemini.com',
            'https://atos.net', 'https://dxc.com', 'https://hcl.com', 'https://techmahindra.com',
            'https://mindtree.com', 'https://ltts.com', 'https://mphasis.com', 'https://hexaware.com',
            
            # Venture Capital & Startups
            'https://a16z.com', 'https://sequoiacap.com', 'https://accel.com', 'https://greylock.com',
            'https://benchmark.com', 'https://kleinerperkins.com', 'https://firstround.com', 'https://foundersfund.com',
            'https://union.vc', 'https://insightpartners.com', 'https://generalcatalyst.com', 'https://bessemer.com',
            'https://lightspeed.com', 'https://matrixpartners.com', 'https://redpoint.com', 'https://nea.com',
            'https://battery.com', 'https://ivp.com', 'https://ggv.com', 'https://dcm.com', 'https://sapphire.com'
        ]
        return random.choice(medium_cpc_referers)
    
    def get_weighted_referer_url(self, high_cpc_weight=None):
        """
        Get a weighted random referer URL favoring high CPC sources
        
        Args:
            high_cpc_weight (float): Probability of selecting high CPC referer (0.0-1.0)
                                   If None, uses configured weight
        """
        if high_cpc_weight is None:
            high_cpc_weight = self.get_high_cpc_weight()
        
        if random.random() < high_cpc_weight:
            return self.get_high_cpc_referer_url()
        else:
            return self.get_medium_cpc_referer_url()
    
    # def open_rexdl_cloud_article(self):
    #     """Legacy method for backward compatibility - now uses generic method"""
    #     article_url = "https://rexdl.biz.id/cloud-migration-challenges-in-the-us-and-how-to-overcome-them/"
    #     return self.open_article_with_referer(article_url)
    
    def _simple_referer_flow(self, article_url, referer_url):
        """DEPRECATED: Use _real_referer_flow() instead - this method is outdated"""
        self.logger.warning("[DEPRECATED] _simple_referer_flow() is outdated")
        self.logger.info("[INFO] Use _real_referer_flow() instead")
        return self._real_referer_flow(article_url, referer_url)
    
    def _legacy_simple_referer_flow(self, article_url, referer_url):
        """LEGACY: Simple referer flow: 1. Buka referer 2. Inject link artikel 3. Klik dan buka article"""
        try:
            self.logger.info(f"[PROCESS] Starting simple referer flow: {referer_url} [RIGHT] {article_url}")
            
            # Step 1: Buka referer
            self.logger.info(f"[LOCATION] Step 1: Buka referer: {referer_url}")
            self.driver.get(referer_url)
            self.timing.wait_between_actions(1, 2)  # Reduced from 2-4 seconds
            
            # Step 2: Simulate browsing on referer (quick)
            self.logger.info("[LOCATION] Step 2: Simulating referer browsing (bandwidth optimized)")
            self._simulate_referer_browsing()
            
            # Step 3: Inject link artikel di referer
            self.logger.info(f"[LOCATION] Step 3: Inject link artikel di referer: {article_url}")
            link_injected = self._inject_article_link(article_url)
            
            if link_injected:
                # Step 4: Klik dan buka article URL dari referer
                self.logger.info("[LOCATION] Step 4: Klik dan buka article URL dari referer")
                click_success = self._click_injected_link()
                
                if click_success:
                    # Step 5: Verify we're on the article page with longer pause
                    self.logger.info("[LOCATION] Step 5: Waiting for article page to load completely")
                    time.sleep(8)  # Longer pause for article loading
                    
                    current_url = self.driver.current_url
                    if article_url in current_url:
                        self.logger.info("[SUCCESS] Simple referer flow completed successfully")
                        
                        # Additional pause after successful navigation
                        self.logger.info("[LOCATION] Additional pause for article stabilization")
                        time.sleep(5)
                        
                        return True
                    else:
                        self.logger.warning(f"[WARNING] Click completed but not on target page: {current_url}")
                        return False
                else:
                    self.logger.warning("[WARNING] Failed to click injected link")
                    return False
            else:
                self.logger.warning("[WARNING] Failed to inject article link")
                return False
                
        except Exception as e:
            self.logger.error(f"Error in simple referer flow: {e}")
            return False
    
    def _inject_article_link(self, article_url):
        """Inject article link into the current referer page"""
        try:
            self.logger.info(f"Injecting article link: {article_url}")
            
            # Inject a natural-looking link into the page
            # link.textContent = 'Cloud Migration Challenges in the US and How to Overcome Them';
            self.driver.execute_script(f"""
                // Create a natural-looking link
                var link = document.createElement('a');
                link.href = '{article_url}';
                link.textContent = 'Business Capital Assistance for MSMEs';
                link.style.cssText = `
                    color: #1a73e8;
                    text-decoration: none;
                    font-size: 16px;
                    font-weight: 500;
                    line-height: 1.5;
                    margin: 10px 0;
                    display: block;
                    padding: 8px 12px;
                    border-radius: 4px;
                    transition: background-color 0.2s;
                `;
                link.id = 'injected-article-link';
                
                // Add hover effect
                link.addEventListener('mouseenter', function() {{
                    this.style.backgroundColor = '#f8f9fa';
                }});
                link.addEventListener('mouseleave', function() {{
                    this.style.backgroundColor = 'transparent';
                }});
                
                // Try to find a good place to inject the link
                var targetElement = null;
                
                // Try to find main content area
                var mainContent = document.querySelector('main') || 
                                 document.querySelector('#main') || 
                                 document.querySelector('.main-content') ||
                                 document.querySelector('article') ||
                                 document.querySelector('.content');
                
                if (mainContent) {{
                    targetElement = mainContent;
                }} else {{
                    // Fallback to body
                    targetElement = document.body;
                }}
                
                // Insert the link at the beginning of the target element
                if (targetElement) {{
                    targetElement.insertBefore(link, targetElement.firstChild);
                    console.log('Article link injected successfully');
                    return true;
                }} else {{
                    console.log('No suitable target element found');
                    return false;
                }}
            """)
            
            # Verify link was injected
            try:
                link_element = self.driver.find_element("id", "injected-article-link")
                if link_element:
                    self.logger.info("[SUCCESS] Article link injected successfully")
                    return True
                else:
                    self.logger.warning("[WARNING] Link injection verification failed")
                    return False
            except:
                self.logger.warning("[WARNING] Could not verify link injection")
                return False
                
        except Exception as e:
            self.logger.error(f"Error injecting article link: {e}")
            return False
    
    def _click_injected_link(self):
        """Click the injected article link with improved error handling"""
        try:
            self.logger.info("Clicking injected article link")
            
            # Find the injected link
            link_element = self.driver.find_element("id", "injected-article-link")
            
            if link_element:
                # Scroll to the link first with more space
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link_element)
                time.sleep(2)  # Longer wait for scroll to complete
                
                # Check if element is visible and clickable
                if not link_element.is_displayed():
                    self.logger.warning("[WARNING] Link element is not visible")
                    return False
                
                # Try multiple click strategies
                click_success = False
                
                # Strategy 1: Direct click
                try:
                    self.mouse.move_to_element(link_element)
                    time.sleep(0.5)
                    link_element.click()
                    click_success = True
                    self.logger.info("[SUCCESS] Direct click successful")
                except Exception as e1:
                    self.logger.warning(f"[WARNING] Direct click failed: {e1}")
                    
                    # Strategy 2: JavaScript click
                    try:
                        self.driver.execute_script("arguments[0].click();", link_element)
                        click_success = True
                        self.logger.info("[SUCCESS] JavaScript click successful")
                    except Exception as e2:
                        self.logger.warning(f"[WARNING] JavaScript click failed: {e2}")
                        
                        # Strategy 3: Scroll down more and try again
                        try:
                            self.driver.execute_script("window.scrollBy(0, 100);")  # Scroll down more
                            time.sleep(1)
                            self.driver.execute_script("arguments[0].click();", link_element)
                            click_success = True
                            self.logger.info("[SUCCESS] Scroll + JavaScript click successful")
                        except Exception as e3:
                            self.logger.warning(f"[WARNING] Scroll + JavaScript click failed: {e3}")
                            
                            # Strategy 4: Move element to different position
                            try:
                                # Move element to a safer position
                                self.driver.execute_script("""
                                    var element = arguments[0];
                                    element.style.position = 'fixed';
                                    element.style.top = '50%';
                                    element.style.left = '50%';
                                    element.style.zIndex = '9999';
                                    element.style.transform = 'translate(-50%, -50%)';
                                """, link_element)
                                time.sleep(1)
                                self.driver.execute_script("arguments[0].click();", link_element)
                                click_success = True
                                self.logger.info("[SUCCESS] Repositioned element click successful")
                            except Exception as e4:
                                self.logger.error(f"[ERROR] All click strategies failed: {e4}")
                
                if click_success:
                    # Wait for navigation to start
                    time.sleep(3)
                    return True
                else:
                    return False
            else:
                self.logger.warning("[WARNING] Injected link not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Error clicking injected link: {e}")
            return False


class AdvancedWebsiteRobot:
    """
    Main class mengikuti pattern cookie_robot.py namun dengan kompleksitas tinggi
    """
    
    def __init__(self, driver, process_advanced_features=True, random_behavior=True):
        self.driver = driver
        self.process_advanced_features = process_advanced_features
        self.random_behavior = random_behavior
        
        # Initialize configuration
        self.config = Configuration()
        
        # Apply stealth scripts if enabled
        self._apply_stealth_scripts()
        
        # Initialize components
        self.timing = TimingSystem()
        self.mouse = MouseMovementSimulator(driver)
        self.risk_monitor = RiskMonitor(driver)
        self.article_browser = ArticleBrowser(driver, self.timing, self.mouse, self.risk_monitor)
        
        logging.info(f'AdvancedWebsiteRobot initialized')
        logging.info(f'Advanced features processing: {self.process_advanced_features}')
        logging.info(f'Random behavior: {self.random_behavior}')
    
    def _apply_stealth_scripts(self):
        """Apply optimized stealth scripts - only essential features not handled by Multilogin"""
        try:
            if self.config.get('stealth.enable_stealth_scripts', True):
                logging.info("[STEALTH] Applying optimized stealth scripts (Multilogin-compatible)...")
                
                # Optimized stealth script - only essential features not handled by Multilogin
                stealth_script = """
                try {
                    // Remove webdriver property (only if not already defined)
                    if (!navigator.webdriver) {
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined,
                        });
                    }
                } catch(e) {
                    // Ignore if already defined
                }
                
                try {
                    // Override plugins with more realistic data
                    if (!navigator.plugins || navigator.plugins.length === 0) {
                        const realisticPlugins = [
                            {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                            {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                            {name: 'Native Client', filename: 'internal-nacl-plugin'},
                            {name: 'Widevine Content Decryption Module', filename: 'widevinecdmadapter.dll'},
                            {name: 'Shockwave Flash', filename: 'pepflashplayer.dll'},
                            {name: 'Microsoft Edge PDF Viewer', filename: 'edge-pdf-viewer'},
                            {name: 'Chrome Remote Desktop Viewer', filename: 'remotedesktop.dll'},
                            {name: 'Chrome Web Store', filename: 'chrome-webstore.dll'}
                        ];
                        Object.defineProperty(navigator, 'plugins', {
                            get: () => realisticPlugins,
                        });
                    }
                } catch(e) {
                    // Ignore if already defined
                }
                
                // User Agent and Language rotation removed - handled by Multilogin
                
                try {
                    // Add random human-like properties with more variation
                    Object.defineProperty(navigator, 'hardwareConcurrency', {
                        get: () => Math.floor(Math.random() * 12) + 2,  // 2-14 cores
                    });
                    
                    // Add realistic device memory
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => Math.floor(Math.random() * 8) + 2,  // 2-10 GB
                    });
                    
                    // Add realistic connection
                    Object.defineProperty(navigator, 'connection', {
                        get: () => ({
                            effectiveType: ['4g', '3g', 'slow-2g', '2g'][Math.floor(Math.random() * 4)],
                            downlink: Math.random() * 15 + 0.5,
                            rtt: Math.random() * 200 + 20,
                            saveData: Math.random() > 0.7
                        }),
                    });
                    
                    // Add realistic battery API
                    Object.defineProperty(navigator, 'getBattery', {
                        get: () => () => Promise.resolve({
                            charging: Math.random() > 0.3,
                            chargingTime: Math.random() * 7200,
                            dischargingTime: Math.random() * 14400,
                            level: Math.random() * 0.8 + 0.2
                        }),
                    });
                    
                    // Add realistic media devices
                    Object.defineProperty(navigator, 'mediaDevices', {
                        get: () => ({
                            enumerateDevices: () => Promise.resolve([
                                {deviceId: 'default', kind: 'audioinput', label: 'Default - Microphone'},
                                {deviceId: 'default', kind: 'audiooutput', label: 'Default - Speaker'},
                                {deviceId: 'default', kind: 'videoinput', label: 'Default - Camera'}
                            ])
                        }),
                    });
                } catch(e) {
                    // Ignore if already defined
                }
                
                try {
                    // Override permissions with error handling
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = (parameters) => {
                        try {
                            return parameters.name === 'notifications' ?
                                Promise.resolve({ state: Notification.permission }) :
                                originalQuery(parameters);
                        } catch(e) {
                            return Promise.resolve({ state: 'denied' });
                        }
                    };
                } catch(e) {
                    // Ignore if already defined
                }
                
                try {
                    // Remove automation indicators
                    delete navigator.__proto__.webdriver;
                    
                    // Remove Chrome runtime
                    if (window.chrome && window.chrome.runtime) {
                        delete window.chrome.runtime;
                    }
                    
                    // Remove automation flags
                    if (window.chrome && window.chrome.app) {
                        delete window.chrome.app;
                    }
                    
                    // Override automation detection
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                        configurable: true
                    });
                    
                    // Remove automation properties
                    delete window.navigator.__proto__.webdriver;
                    delete window.navigator.__proto__.__webdriver_script_fn;
                    delete window.navigator.__proto__.__webdriver_script_func;
                    delete window.navigator.__proto__.__webdriver_script_function;
                    
                    // Override automation detection methods
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                        configurable: true
                    });
                    
                    // Remove automation flags from window
                    delete window.__webdriver_script_fn;
                    delete window.__webdriver_script_func;
                    delete window.__webdriver_script_function;
                    delete window.__webdriver_script_id;
                    delete window.__webdriver_script_params;
                    delete window.__webdriver_script_result;
                    
                    // Override automation detection in document
                    Object.defineProperty(document, 'webdriver', {
                        get: () => undefined,
                        configurable: true
                    });
                    
                    // Remove automation detection from document
                    delete document.__proto__.webdriver;
                    delete document.__proto__.__webdriver_script_fn;
                    delete document.__proto__.__webdriver_script_func;
                    delete document.__proto__.__webdriver_script_function;
                } catch(e) {
                    // Ignore if not present
                }
                
                // Screen properties and timezone management removed - handled by Multilogin
                """
                
                self.driver.execute_script(stealth_script)
                logging.info("[SUCCESS] Enhanced stealth scripts applied successfully")
            else:
                logging.info("[INFO] Stealth scripts disabled in configuration")
                
        except Exception as e:
            logging.warning(f"[WARNING] Failed to apply stealth scripts: {e}")
            # Try fallback stealth
            try:
                self._apply_fallback_stealth()
            except Exception as fallback_error:
                logging.error(f"[ERROR] Fallback stealth also failed: {fallback_error}")
    
    def _apply_fallback_stealth(self):
        """Apply minimal stealth as fallback"""
        try:
            fallback_script = """
            try {
                if (!navigator.webdriver) {
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                }
            } catch(e) {}
            """
            self.driver.execute_script(fallback_script)
            logging.info("[FALLBACK] Minimal stealth applied")
        except Exception as e:
            logging.error(f"[ERROR] Fallback stealth failed: {e}")
    
    def run_advanced_automation(self):
        """
        Main automation function mengikuti pattern cookie_robot.py
        """
        try:
            logging.info("Starting advanced automation")
            
            # Test basic driver functionality
            try:
                current_url = self.driver.current_url
                logging.info(f"Current URL: {current_url}")
            except Exception as e:
                logging.warning(f"Could not get current URL: {e}")
            
            # Maximize window
            try:
                self.driver.maximize_window()
                logging.info("Window maximized successfully")
            except Exception as e:
                logging.warning(f"Failed to maximize window: {e}")
            
            # Wait for initial setup
            self.timing.wait_between_actions(2, 4)
            
            if self.process_advanced_features:
                # Set article URLs array secara dinamis (random selection)
                # article_browser.set_article_urls([
                #     "https://domain1.com/article1/",
                #     "https://domain2.com/article2/",
                #     "https://domain3.com/article3/"
                # ])

                # Set referer options secara dinamis
                # article_browser.set_referer_options([
                #     "https://custom1.com", "https://custom2.com"
                # ])
                
                # Set high CPC weight (0.0-1.0, default: 0.7)
                # article_browser.set_high_cpc_weight(0.8)  # 80% chance for high CPC referers

                
                # Run advanced article browsing - now domain agnostic with random selection
                # You can specify custom article_url and referer_url here
                success = self.article_browser.open_article_with_referer()
                
                if success:
                    logging.info("[SUCCESS] Advanced automation completed successfully!")
                    
                    # Get comprehensive statistics
                    try:
                        risk_stats = self.risk_monitor.get_risk_statistics()
                        ad_stats = self.article_browser.ad_clicker.get_click_statistics()
                        
                        logging.info(f"[STATS] Risk Statistics:")
                        logging.info(f"   Current Risk Level: {risk_stats['current_risk_level']}")
                        logging.info(f"   Total Requests: {risk_stats['total_requests']}")
                        logging.info(f"   Requests Last Minute: {risk_stats['requests_last_minute']}")
                        logging.info(f"   Detection Events: {risk_stats['detection_events']}")
                        
                        logging.info(f"[STATS] Ad Clicking Statistics:")
                        logging.info(f"   Total Clicks: {ad_stats['total_clicks']}")
                        logging.info(f"   Recent Clicks: {ad_stats['recent_clicks']}")
                        rate_limit_window_minutes = self.config.get('ad_clicking.rate_limit_window', 1200) // 60
                        max_clicks_per_window = self.config.get('ad_clicking.max_clicks_per_window', 3)
                        logging.info(f"   Rate Limit Clicks ({rate_limit_window_minutes}min): {ad_stats['rate_limit_clicks']}/{max_clicks_per_window}")
                        logging.info(f"   Rate Limit Remaining: {ad_stats['rate_limit_remaining']}")
                        logging.info(f"   Click Rate: {ad_stats['click_rate']:.2f} clicks/min")
                        logging.info(f"   Average Interval: {ad_stats['average_click_interval']:.2f}s")
                        logging.info(f"   Ad Types Clicked: {ad_stats['ad_types_clicked']}")
                        
                        # Display post navigation statistics for AdSense RPM optimization
                        try:
                            post_stats = self.article_browser.get_post_navigation_stats()
                            if post_stats:
                                logging.info(f"[STATS] Post Navigation Statistics (AdSense RPM Optimization):")
                                logging.info(f"   Total Posts Visited: {post_stats['total_posts_visited']}")
                                logging.info(f"   Min Posts Required: {post_stats['min_posts_per_session']}")
                                logging.info(f"   Max Posts Per Session: {post_stats['max_posts_per_session']}")
                                logging.info(f"   Posts Remaining: {post_stats['posts_remaining']}")
                                logging.info(f"   Minimum Requirement Met: {'[SUCCESS] Yes' if post_stats['minimum_met'] else '[ERROR] No'}")
                                logging.info(f"   Estimated Page Views: {post_stats['total_posts_visited']}")
                        except Exception as e:
                            logging.warning(f"Could not get post navigation statistics: {e}")
                        
                    except Exception as e:
                        logging.warning(f"Could not get comprehensive statistics: {e}")
                else:
                    logging.error("[ERROR] Advanced automation failed")
            else:
                logging.info("Skipping advanced features processing")
            
            # Keep browser open for inspection
            logging.info("[WAIT] Keeping browser open for 30 seconds...")
            time.sleep(30)
            
            logging.info("[SUCCESS] Advanced automation completed!")
            
        except Exception as e:
            logging.error(f"Error in advanced automation: {e}", exc_info=True)
            
            # Keep browser open even on error
            logging.info("[WAIT] Keeping browser open for 15 seconds after error...")
            time.sleep(15)
    
    def run(self):
        """
        Main run function mengikuti pattern cookie_robot.py
        """
        self.run_advanced_automation()


# Setup logging
setup_logging()

# Configuration parameters
process_advanced_features = True
random_behavior = True

logging.info('Advanced Website Robot started')
logging.info(f'process_advanced_features: {process_advanced_features}')
logging.info(f'random_behavior: {random_behavior}')

# Create and run robot (mengikuti pattern cookie_robot.py)
robot = AdvancedWebsiteRobot(
    driver=driver,
    process_advanced_features=process_advanced_features,
    random_behavior=random_behavior
)

robot.run()
