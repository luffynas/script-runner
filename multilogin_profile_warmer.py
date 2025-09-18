# -*- coding: utf-8 -*-
"""
Multilogin Profile Warmer - Advanced Profile Maturity System
============================================================

Script ini mengimplementasikan teknik warming profile yang canggih untuk Multilogin
berdasarkan penelitian terbaru tentang perilaku cookie, pola aktivitas pengguna, dan
sistem personalisasi iklan.

FITUR UTAMA:
- Simulasi aktivitas pengguna alami (scroll, klik, browsing)
- Manajemen Local Storage & IndexedDB
- Manajemen referrer dan history
- Jadwal warming multi-hari dengan pola alami
- Manajemen cookie canggih (first-party vs third-party)
- Fitur stealth untuk kematangan profile
- Integrasi dengan jadwal warming 14 hari

CARA PENGGUNAAN DI MULTILOGIN:
1. Upload script ini ke Multilogin Script Runner
2. Script menggunakan Google dorking technique (tidak perlu file eksternal)
3. Ubah konfigurasi di bagian MULTILOGIN_CONFIG sesuai kebutuhan
4. Jalankan script melalui Multilogin
5. Script akan otomatis search di Google dan browse hasil organik

KONFIGURASI:
- warming_mode: "quick" (3 aktivitas), "daily" (1 hari), "full" (14 hari)
- day_to_warm: Hari yang akan di-warm (untuk mode daily)
- start_day/end_day: Range hari (untuk mode full)
- preferred_category: Kategori query yang akan digunakan
  * "insurance": Insurance-related queries (24 queries)
  * "loans": Loans and financing queries (32 queries - International)
  * "loans_indonesia": Loans Indonesia queries (20 queries - Bahasa Indonesia)
  * "ai": AI and technology queries (24 queries)
  * "crypto": Cryptocurrency queries (24 queries)
  * "erp_crm": ERP/CRM business software queries (24 queries)

TEKNIK WARMING YANG DIIMPLEMENTASIKAN:
1. Google Dorking: Search di Google dengan query targeted, klik hasil organik
2. Natural Browsing: Scroll, mouse movement, klik elemen secara alami
3. Local Storage & IndexedDB: Simpan data analytics, preferences, tracking
4. Referrers & History: Simulasi traffic dari Google search results
5. Cookie Management: First-party dan third-party cookies untuk personalisasi
6. Dynamic Content: Tidak bergantung pada CSV static, selalu fresh content

Author: AI Assistant
Date: 2025
Version: 1.0
"""

import random
import time
import logging
import sys
import json
import datetime
from urllib.parse import urlparse, urljoin

# Selenium imports - akan tersedia di Multilogin environment
try:
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
except ImportError:
    # Fallback untuk development environment
    pass

try:
    import requests
except ImportError:
    # Fallback untuk development environment
    pass


def setup_logging():
    """Setup logging system for Multilogin environment"""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s'))
    
    logger = logging.getLogger('multilogin_profile_warmer')
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    
    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()
    logger.addHandler(console_handler)
    
    return logger


class WarmingConfiguration:
    """Advanced configuration for profile warming - optimized for Multilogin"""
    
    def __init__(self):
        self.config = {
            'timing': {
                'min_delay': 0.5,
                'max_delay': 3.0,
                'page_load_timeout': 30,
                'element_wait_timeout': 10,
                'human_typing_delay_range': (0.1, 0.3),
                'human_scroll_delay_range': (1, 5),
                'human_click_delay_range': (0.5, 2.0),
                'reading_pause_range': (2, 8),
                'between_sessions_delay': (300, 1800)  # 5-30 minutes
            },
            'stealth': {
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'window_size': (1920, 1080),
                'disable_images': False,
                'disable_javascript': False,
                'enable_stealth_scripts': True,
                'behavioral_stealth': True,
                'randomize_viewport': True
            },
            'warming': {
                'max_sessions_per_day': 8,
                'min_sessions_per_day': 3,
                'session_duration_range': (60, 300),  # 1-5 minutes
                'natural_break_chance': 0.15,
                'cross_domain_activity': True,
                'social_media_activity': True,
                'search_activity': True
            },
            'storage': {
                'enable_local_storage': True,
                'enable_indexed_db': True,
                'enable_session_storage': True,
                'storage_data_types': ['preferences', 'analytics', 'tracking', 'user_data'],
                'max_storage_entries': 50
            },
            'cookies': {
                'enable_first_party': True,
                'enable_third_party': True,
                'cookie_categories': ['analytics', 'preferences', 'advertising', 'functional'],
                'max_cookies_per_domain': 20,
                'cookie_expiry_range': (1, 365)  # days
            },
            'referrers': {
                'enable_referrer_simulation': True,
                'referrer_sources': [
                    'google.com', 'bing.com', 'yahoo.com', 'duckduckgo.com',
                    'facebook.com', 'twitter.com', 'linkedin.com', 'reddit.com',
                    'youtube.com', 'pinterest.com', 'instagram.com'
                ],
                'direct_traffic_ratio': 0.3,
                'search_traffic_ratio': 0.4,
                'social_traffic_ratio': 0.3
            },
            'domains': {
                'insurance_domains': [
                    # Domain insurance dari CSV yang sebenarnya digunakan
                    'travelers.com', 'allianz.com', 'rootinsurance.com',
                    'allstate.com', 'amfam.com', 'lemonade.com', 'statefarm.com',
                    'nationwide.com', 'geico.com', 'progressive.com', 'farmers.com',
                    'libertymutual.com', 'usaa.com', 'cigna.com', 'aetna.com',
                    'unitedhealthgroup.com', 'esurance.com', 'zurich.com', 'axa.com',
                    'chubb.com', 'nextinsurance.com', 'trustpilot.com', 'cnbc.com',
                    'policygenius.com', 'insurify.com', 'thezebra.com', 'nerdwallet.com',
                    'bankrate.com', 'moneysupermarket.com', 'gocompare.com',
                    'comparethemarket.com', 'compare.com', 'insurancequotes.com',
                    'insurance.com', 'medicare.gov', 'healthcare.gov', 'naic.org',
                    'iii.org', 'consumerreports.org', 'reviews.com', 'trustedchoice.com',
                    'kaiserpermanente.org'  # Ditambahkan dari CSV
                ],
                'general_domains': [
                    # Domain general yang benar-benar ada di CSV
                    'google.com', 'facebook.com', 'youtube.com', 'reddit.com', 
                    'twitter.com', 'linkedin.com', 'bing.com', 'nytimes.com', 
                    'theguardian.com'  # Ditambahkan dari CSV
                ],
                'comparison_sites': [
                    'compare.com', 'policygenius.com', 'insurify.com', 'thezebra.com',
                    'nerdwallet.com', 'bankrate.com', 'moneysupermarket.com',
                    'gocompare.com', 'comparethemarket.com'
                ]
            },
            'actions': {
                'homepage_actions': [
                    'Open homepage and scroll (read)',
                    'Open homepage and browse categories',
                    'Open homepage and search for products'
                ],
                'interaction_actions': [
                    'Use payment/premium calculator, interact',
                    'Open quotes page, use calculator if present',
                    'Fill out contact form',
                    'Subscribe to newsletter'
                ],
                'research_actions': [
                    'Read FAQ / requirements',
                    'Open reviews/trustpilot or testimonials',
                    'Open policies/coverage details, read FAQ',
                    'Compare plans or providers on aggregator'
                ],
                'conversion_actions': [
                    'Open \'Get a quote\' or product apply page',
                    'Add product to cart',
                    'Start checkout process',
                    'Download brochure or guide'
                ]
            },
            'behavioral_profiles': {
                'casual_browser': {
                    'scroll_intensity': 'light',
                    'click_probability': 0.3,
                    'dwell_time_range': (30, 120),
                    'session_frequency': 'low'
                },
                'researcher': {
                    'scroll_intensity': 'heavy',
                    'click_probability': 0.7,
                    'dwell_time_range': (120, 300),
                    'session_frequency': 'high'
                },
                'comparison_shopper': {
                    'scroll_intensity': 'medium',
                    'click_probability': 0.5,
                    'dwell_time_range': (90, 240),
                    'session_frequency': 'medium'
                },
                'quick_visitor': {
                    'scroll_intensity': 'light',
                    'click_probability': 0.2,
                    'dwell_time_range': (15, 60),
                    'session_frequency': 'very_high'
                }
            },
            'multilogin_specific': {
                'enable_profile_warming': True,
                'warm_before_main_automation': True,
                'preserve_existing_cookies': True,
                'simulate_real_user_patterns': True,
                'enable_cross_domain_tracking': True,
                'maintain_session_continuity': True
            }
        }
    
    def get(self, key_path, default=None):
        """Get configuration value using dot notation"""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value


class WarmingScheduleManager:
    """Manages multi-day warming schedules using Google dorking technique"""
    
    def __init__(self):
        self.logger = logging.getLogger('multilogin_profile_warmer')
        self.schedule_data = []
        self.current_day = 1
        self.current_session = 0
        
        # Use Google dorking technique instead of static CSV
        self.setup_dorking_queries()
    
    def setup_dorking_queries(self):
        """Setup Google dorking queries for natural profile warming"""
        try:
            # Insurance-focused dorking queries
            self.insurance_queries = [
                # Insurance comparison queries
                "best car insurance rates 2024",
                "cheap auto insurance quotes",
                "home insurance comparison",
                "life insurance rates comparison",
                "health insurance plans 2024",
                "travel insurance reviews",
                "pet insurance coverage",
                "business insurance quotes",
                
                # Insurance company specific
                "geico vs progressive insurance",
                "state farm insurance reviews",
                "allstate insurance rates",
                "farmers insurance coverage",
                "liberty mutual insurance quotes",
                "nationwide insurance reviews",
                "travelers insurance rates",
                "usaa insurance benefits",
                
                # Insurance topics
                "insurance deductible explained",
                "how to lower insurance premiums",
                "insurance claim process",
                "insurance coverage types",
                "insurance fraud prevention",
                "insurance agent vs broker",
                "insurance policy renewal",
                "insurance discounts available"
            ]
            
            # Loans-focused dorking queries (International)
            self.loans_queries = [
                # Personal loans
                "best personal loans 2024",
                "cheap personal loan rates",
                "personal loan comparison",
                "unsecured personal loans",
                "personal loan calculator",
                "personal loan requirements",
                "personal loan approval process",
                "personal loan vs credit card",
                
                # Business loans
                "small business loans 2024",
                "business loan rates comparison",
                "SBA loans application",
                "business line of credit",
                "equipment financing loans",
                "startup business loans",
                "business loan requirements",
                "business loan calculator",
                
                # Mortgage loans
                "best mortgage rates 2024",
                "home loan comparison",
                "mortgage calculator",
                "first time home buyer loans",
                "refinance mortgage rates",
                "VA loans benefits",
                "FHA loans requirements",
                "jumbo loan rates",
                
                # Auto loans
                "best auto loan rates 2024",
                "car loan calculator",
                "auto loan pre approval",
                "used car loans",
                "new car financing",
                "auto loan vs lease",
                "bad credit auto loans",
                "auto loan refinancing"
            ]
            
            # Loans Indonesia-focused dorking queries
            self.loans_indonesia_queries = [
                # Kredit tanpa agunan
                "kredit tanpa agunan terbaik 2024",
                "pinjaman tanpa agunan",
                "kredit tanpa jaminan",
                "kredit tanpa survey",
                
                # Pinjaman online
                "pinjaman online terpercaya",
                "pinjaman cepat online",
                "pinjaman bank syariah",
                "pinjaman bank konvensional",
                
                # Kredit multiguna
                "kredit multiguna terbaik",
                "kredit konsumtif terbaik",
                "kredit tanpa bunga",
                "cicilan tanpa bunga",
                
                # KPR (Kredit Pemilikan Rumah)
                "kredit pemilikan rumah KPR",
                "kredit rumah subsidi",
                "cicilan rumah murah",
                
                # KKB (Kredit Kendaraan Bermotor)
                "kredit kendaraan bermotor KKB",
                "cicilan mobil murah",
                "kredit motor terbaik",
                
                # KUR (Kredit Usaha Rakyat)
                "kredit usaha rakyat KUR",
                "kredit usaha kecil menengah"
            ]
            
            # AI-focused dorking queries
            self.ai_queries = [
                # AI tools and platforms
                "best AI tools 2024",
                "ChatGPT alternatives",
                "AI writing tools comparison",
                "AI image generators",
                "AI video editing tools",
                "AI coding assistants",
                "AI productivity tools",
                "AI automation software",
                
                # AI for business
                "AI for small business",
                "AI customer service tools",
                "AI marketing automation",
                "AI data analysis tools",
                "AI project management",
                "AI content creation",
                "AI chatbots for business",
                "AI workflow automation",
                
                # AI learning and development
                "AI courses online",
                "machine learning tutorials",
                "AI certification programs",
                "AI programming languages",
                "AI career opportunities",
                "AI skills development",
                "AI research papers",
                "AI industry trends 2024"
            ]
            
            # Cryptocurrency-focused dorking queries
            self.crypto_queries = [
                # Cryptocurrency trading
                "best crypto exchanges 2024",
                "cryptocurrency trading platforms",
                "crypto wallet comparison",
                "bitcoin trading strategies",
                "ethereum price prediction",
                "crypto portfolio tracker",
                "cryptocurrency taxes",
                "crypto security best practices",
                
                # DeFi and blockchain
                "DeFi platforms 2024",
                "yield farming strategies",
                "liquidity mining guide",
                "blockchain development",
                "smart contracts tutorial",
                "NFT marketplace comparison",
                "Web3 applications",
                "metaverse crypto projects",
                
                # Crypto news and analysis
                "cryptocurrency news today",
                "bitcoin price analysis",
                "crypto market trends",
                "altcoin investment guide",
                "crypto regulations 2024",
                "cryptocurrency adoption",
                "crypto mining profitability",
                "stablecoin comparison"
            ]
            
            # ERP/CRM-focused dorking queries
            self.erp_crm_queries = [
                # ERP systems
                "best ERP systems 2024",
                "ERP software comparison",
                "SAP vs Oracle ERP",
                "cloud ERP solutions",
                "ERP implementation guide",
                "ERP for small business",
                "ERP cost comparison",
                "ERP integration services",
                
                # CRM systems
                "best CRM software 2024",
                "Salesforce vs HubSpot",
                "CRM for small business",
                "CRM implementation guide",
                "CRM integration tools",
                "CRM automation features",
                "CRM pricing comparison",
                "CRM customization options",
                
                # Business management
                "business process automation",
                "workflow management tools",
                "project management software",
                "inventory management systems",
                "accounting software integration",
                "business intelligence tools",
                "data management solutions",
                "enterprise software selection"
            ]
            
            # Combine all queries for random selection
            self.dorking_queries = (
                self.insurance_queries + 
                self.loans_queries + 
                self.loans_indonesia_queries +
                self.ai_queries + 
                self.crypto_queries + 
                self.erp_crm_queries
            )
            
            self.logger.info(f"✅ Setup dorking queries:")
            self.logger.info(f"   - Insurance: {len(self.insurance_queries)} queries")
            self.logger.info(f"   - Loans (International): {len(self.loans_queries)} queries")
            self.logger.info(f"   - Loans Indonesia: {len(self.loans_indonesia_queries)} queries")
            self.logger.info(f"   - AI: {len(self.ai_queries)} queries")
            self.logger.info(f"   - Cryptocurrency: {len(self.crypto_queries)} queries")
            self.logger.info(f"   - ERP/CRM: {len(self.erp_crm_queries)} queries")
            self.logger.info(f"   - Total: {len(self.dorking_queries)} queries")
            
        except Exception as e:
            self.logger.error(f"❌ Error setting up dorking queries: {e}")
            # Use default query as fallback
            self.dorking_queries = ["insurance quotes comparison"]
    
    def get_random_dorking_query(self, category=None, config=None):
        """Get a random dorking query for Google search from specific category"""
        try:
            # Determine which category to use
            target_category = None
            
            # Priority 1: Explicit category parameter
            if category:
                target_category = category
            
            # Priority 2: Preferred category from config
            elif config and config.get('preferred_category'):
                target_category = config.get('preferred_category')
            
            # Priority 3: First enabled category from config
            elif config and config.get('query_categories'):
                enabled_categories = [cat for cat, enabled in config.get('query_categories', {}).items() if enabled]
                if enabled_categories:
                    target_category = enabled_categories[0]  # Use first enabled category
            
            # Priority 4: Default to insurance
            else:
                target_category = 'insurance'
            
            # Get queries from target category
            if target_category and hasattr(self, f'{target_category}_queries'):
                queries = getattr(self, f'{target_category}_queries')
                if queries:
                    self.logger.debug(f"Using {target_category} category with {len(queries)} queries")
                    return random.choice(queries)
            
            # Fallback to insurance queries
            if hasattr(self, 'insurance_queries') and self.insurance_queries:
                self.logger.debug("Fallback to insurance queries")
                return random.choice(self.insurance_queries)
            
            return "insurance quotes comparison"
            
        except Exception as e:
            self.logger.error(f"Error getting dorking query: {e}")
            return "insurance quotes comparison"
    
    def get_queries_by_category(self, category):
        """Get all queries for a specific category"""
        try:
            if hasattr(self, f'{category}_queries'):
                return getattr(self, f'{category}_queries')
            return []
        except Exception as e:
            self.logger.error(f"Error getting queries for category {category}: {e}")
            return []
    
    def get_available_categories(self):
        """Get list of available query categories"""
        return ['insurance', 'loans', 'ai', 'crypto', 'erp_crm']
    
    
    
    def get_next_activity(self, category=None, config=None):
        """Get next activity using Google dorking technique from specific category"""
        # Use Google dorking instead of static schedule
        query = self.get_random_dorking_query(category, config)
        
        # Determine category for logging
        if category:
            selected_category = category
        elif config and config.get('preferred_category'):
            selected_category = config.get('preferred_category')
        else:
            selected_category = 'insurance'  # Default to insurance
        
        return {
            'type': 'google_dorking',
            'query': query,
            'category': selected_category,
            'dwell_time': random.randint(30, 120),  # 30-120 seconds
            'inter_action_delay': random.randint(10, 30)  # 10-30 seconds
        }


class AdvancedTimingSystem:
    """Advanced timing system with human-like behavior"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('multilogin_profile_warmer')
        self.last_action_time = time.time()
        self.session_start_time = time.time()
    
    def human_like_delay(self, delay_type="normal"):
        """Generate human-like delays based on activity type"""
        base_delays = {
            "fast": (0.5, 1.5),
            "normal": (1.0, 3.0),
            "slow": (2.0, 5.0),
            "reading": (3.0, 8.0),
            "thinking": (5.0, 15.0)
        }
        
        min_delay, max_delay = base_delays.get(delay_type, base_delays["normal"])
        
        # Add some randomness and human-like patterns
        base_delay = random.uniform(min_delay, max_delay)
        
        # Occasionally add longer pauses (human behavior)
        if random.random() < 0.1:  # 10% chance
            base_delay += random.uniform(2, 8)
        
        # Add micro-delays for more human-like behavior
        micro_delay = random.uniform(0.1, 0.5)
        
        total_delay = base_delay + micro_delay
        time.sleep(total_delay)
        
        self.logger.debug(f"Applied {delay_type} delay: {total_delay:.2f}s")
        return total_delay
    
    def reading_pause(self, content_length="medium"):
        """Simulate reading pauses based on content length"""
        pause_ranges = {
            "short": (1, 3),
            "medium": (3, 8),
            "long": (8, 20),
            "very_long": (15, 45)
        }
        
        min_pause, max_pause = pause_ranges.get(content_length, pause_ranges["medium"])
        pause_duration = random.uniform(min_pause, max_pause)
        
        time.sleep(pause_duration)
        self.logger.debug(f"Reading pause ({content_length}): {pause_duration:.2f}s")
        return pause_duration
    
    def between_sessions_delay(self):
        """Delay between warming sessions"""
        min_delay, max_delay = self.config.get('timing.between_sessions_delay', (300, 1800))
        delay = random.uniform(min_delay, max_delay)
        
        self.logger.info(f"Waiting {delay/60:.1f} minutes between sessions")
        time.sleep(delay)
        return delay


class StorageManager:
    """Manages Local Storage, IndexedDB, and Session Storage"""
    
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.logger = logging.getLogger('multilogin_profile_warmer')
    
    def inject_storage_data(self, domain, data_type="analytics"):
        """Inject realistic storage data for a domain"""
        try:
            storage_scripts = {
                "analytics": """
                    // Google Analytics
                    if (typeof gtag !== 'undefined') {
                        gtag('config', 'GA_MEASUREMENT_ID', {
                            'custom_map': {'custom_parameter': 'value'},
                            'user_properties': {
                                'user_type': 'returning',
                                'engagement_level': 'high'
                            }
                        });
                    }
                    
                    // Local Storage Analytics
                    localStorage.setItem('ga_client_id', 'GA1.2.' + Math.random().toString(36).substr(2, 9));
                    localStorage.setItem('analytics_session_id', Date.now().toString());
                    localStorage.setItem('user_engagement_score', Math.floor(Math.random() * 100).toString());
                """,
                "preferences": """
                    // User Preferences
                    localStorage.setItem('theme_preference', 'light');
                    localStorage.setItem('language_preference', 'en-US');
                    localStorage.setItem('timezone_offset', new Date().getTimezoneOffset().toString());
                    localStorage.setItem('user_consent', 'true');
                    localStorage.setItem('cookie_preferences', JSON.stringify({
                        'necessary': true,
                        'analytics': true,
                        'marketing': false,
                        'preferences': true
                    }));
                """,
                "tracking": """
                    // Tracking Data
                    localStorage.setItem('visit_count', Math.floor(Math.random() * 50 + 1).toString());
                    localStorage.setItem('last_visit', Date.now().toString());
                    localStorage.setItem('session_duration', Math.floor(Math.random() * 1800 + 60).toString());
                    localStorage.setItem('page_views', Math.floor(Math.random() * 20 + 1).toString());
                """,
                "user_data": """
                    // User Data
                    sessionStorage.setItem('user_session_id', 'sess_' + Math.random().toString(36).substr(2, 9));
                    sessionStorage.setItem('current_page', window.location.href);
                    sessionStorage.setItem('referrer', document.referrer || 'direct');
                    sessionStorage.setItem('user_agent_hash', btoa(navigator.userAgent).substr(0, 16));
                """
            }
            
            script = storage_scripts.get(data_type, storage_scripts["analytics"])
            self.driver.execute_script(script)
            
            self.logger.debug(f"Injected {data_type} storage data for {domain}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error injecting storage data: {e}")
            return False
    
    def create_indexed_db_data(self, domain):
        """Create IndexedDB data for enhanced profile maturity"""
        try:
            script = """
                // Create IndexedDB for user data
                const request = indexedDB.open('UserDataDB', 1);
                
                request.onupgradeneeded = function(event) {
                    const db = event.target.result;
                    
                    // Create object stores
                    if (!db.objectStoreNames.contains('userPreferences')) {
                        const userPrefsStore = db.createObjectStore('userPreferences', { keyPath: 'id' });
                        userPrefsStore.createIndex('category', 'category', { unique: false });
                    }
                    
                    if (!db.objectStoreNames.contains('browsingHistory')) {
                        const historyStore = db.createObjectStore('browsingHistory', { keyPath: 'id' });
                        historyStore.createIndex('timestamp', 'timestamp', { unique: false });
                    }
                };
                
                request.onsuccess = function(event) {
                    const db = event.target.result;
                    const transaction = db.transaction(['userPreferences', 'browsingHistory'], 'readwrite');
                    
                    // Add user preferences
                    const userPrefsStore = transaction.objectStore('userPreferences');
                    userPrefsStore.add({
                        id: 1,
                        category: 'display',
                        key: 'theme',
                        value: 'light',
                        timestamp: Date.now()
                    });
                    
                    // Add browsing history dengan domain yang relevan dari CSV
                    const historyStore = transaction.objectStore('browsingHistory');
                    const relevantDomains = [
                        'travelers.com', 'humana.com', 'allianz.com', 'rootinsurance.com',
                        'allstate.com', 'amfam.com', 'lemonade.com', 'statefarm.com',
                        'nationwide.com', 'geico.com', 'progressive.com', 'farmers.com',
                        'libertymutual.com', 'usaa.com', 'cigna.com', 'aetna.com',
                        'unitedhealthgroup.com', 'esurance.com', 'zurich.com', 'axa.com',
                        'chubb.com', 'nextinsurance.com', 'trustpilot.com', 'cnbc.com',
                        'policygenius.com', 'insurify.com', 'thezebra.com', 'nerdwallet.com',
                        'bankrate.com', 'moneysupermarket.com', 'gocompare.com',
                        'comparethemarket.com', 'compare.com', 'insurancequotes.com',
                        'insurance.com', 'medicare.gov', 'healthcare.gov', 'naic.org',
                        'iii.org', 'consumerreports.org', 'reviews.com', 'trustedchoice.com',
                        'kaiserpermanente.org', 'theguardian.com', 'google.com', 'facebook.com',
                        'youtube.com', 'reddit.com', 'twitter.com', 'linkedin.com', 'bing.com', 'nytimes.com'
                    ];
                    
                    for (let i = 0; i < 10; i++) {
                        const domain = relevantDomains[i % relevantDomains.length];
                        const pageTypes = ['home', 'products', 'about', 'contact', 'services', 'pricing'];
                        const pageType = pageTypes[i % pageTypes.length];
                        
                        historyStore.add({
                            id: i + 1,
                            url: 'https://' + domain + '/' + pageType,
                            title: domain.charAt(0).toUpperCase() + domain.slice(1) + ' - ' + pageType.charAt(0).toUpperCase() + pageType.slice(1),
                            timestamp: Date.now() - (i * 3600000), // 1 jam per entry
                            duration: Math.floor(Math.random() * 300 + 30)
                        });
                    }
                };
            """
            
            self.driver.execute_script(script)
            self.logger.debug(f"Created IndexedDB data for {domain}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating IndexedDB data: {e}")
            return False


class CookieManager:
    """Advanced cookie management system"""
    
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.logger = logging.getLogger('multilogin_profile_warmer')
    
    def inject_realistic_cookies(self, domain, cookie_type="analytics"):
        """Inject realistic cookies for profile maturity"""
        try:
            # Get current URL to ensure domain compatibility
            current_url = self.driver.current_url
            current_domain = urlparse(current_url).netloc
            
            # Only inject cookies if we're on the same domain or subdomain
            if not self._is_domain_compatible(domain, current_domain):
                self.logger.debug(f"Skipping cookie injection for {domain} - domain mismatch with {current_domain}")
                return True
            
            cookie_templates = {
                "analytics": [
                    {
                        'name': '_ga',
                        'value': f'GA1.2.{random.randint(100000000, 999999999)}.{int(time.time())}',
                        'path': '/',
                        'expires': int(time.time()) + (365 * 24 * 3600)  # 1 year
                    },
                    {
                        'name': '_gid',
                        'value': f'GA1.2.{random.randint(100000000, 999999999)}.{int(time.time())}',
                        'path': '/',
                        'expires': int(time.time()) + (24 * 3600)  # 1 day
                    }
                ],
                "preferences": [
                    {
                        'name': 'user_preferences',
                        'value': json.dumps({
                            'theme': 'light',
                            'language': 'en',
                            'timezone': 'America/New_York'
                        }),
                        'path': '/',
                        'expires': int(time.time()) + (30 * 24 * 3600)  # 30 days
                    }
                ],
                "functional": [
                    {
                        'name': 'session_id',
                        'value': f'sess_{random.randint(100000, 999999)}',
                        'path': '/',
                        'expires': int(time.time()) + (24 * 3600)  # 1 day
                    }
                ]
            }
            
            cookies = cookie_templates.get(cookie_type, cookie_templates["analytics"])
            
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as cookie_error:
                    self.logger.debug(f"Could not inject cookie {cookie['name']}: {cookie_error}")
                    continue
            
            self.logger.debug(f"Injected {len(cookies)} {cookie_type} cookies for {current_domain}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error injecting cookies: {e}")
            return False
    
    def _is_domain_compatible(self, target_domain, current_domain):
        """Check if target domain is compatible with current domain for cookie injection"""
        try:
            # Remove www prefix for comparison
            target_clean = target_domain.replace('www.', '')
            current_clean = current_domain.replace('www.', '')
            
            # Check if domains match or if current is subdomain of target
            return (target_clean == current_clean or 
                   current_clean.endswith('.' + target_clean))
        except:
            return False
    
    def set_referrer_cookie(self, referrer_domain, target_domain):
        """Set referrer information in cookies"""
        try:
            referrer_cookie = {
                'name': 'referrer_info',
                'value': json.dumps({
                    'source': referrer_domain,
                    'timestamp': int(time.time()),
                    'campaign': 'organic'
                }),
                'domain': target_domain,
                'path': '/',
                'expires': int(time.time()) + (7 * 24 * 3600)  # 7 days
            }
            
            self.driver.add_cookie(referrer_cookie)
            self.logger.debug(f"Set referrer cookie: {referrer_domain} -> {target_domain}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting referrer cookie: {e}")
            return False


class HumanLikeBehavior:
    """Simulates human-like browsing behavior"""
    
    def __init__(self, driver, timing_system):
        self.driver = driver
        self.timing_system = timing_system
        self.logger = logging.getLogger('multilogin_profile_warmer')
        self.actions = ActionChains(driver)
    
    def natural_scroll(self, scroll_type="reading"):
        """Perform natural scrolling behavior"""
        try:
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            
            scroll_patterns = {
                "reading": {
                    "scroll_amount": viewport_height * 0.3,
                    "pause_range": (2, 5),
                    "scroll_count": random.randint(3, 8)
                },
                "scanning": {
                    "scroll_amount": viewport_height * 0.8,
                    "pause_range": (0.5, 2),
                    "scroll_count": random.randint(2, 5)
                },
                "exploring": {
                    "scroll_amount": viewport_height * 0.5,
                    "pause_range": (1, 3),
                    "scroll_count": random.randint(5, 12)
                }
            }
            
            pattern = scroll_patterns.get(scroll_type, scroll_patterns["reading"])
            
            for i in range(pattern["scroll_count"]):
                # Random scroll direction (mostly down, occasionally up)
                if random.random() < 0.1:  # 10% chance to scroll up
                    scroll_amount = -pattern["scroll_amount"] * 0.5
                else:
                    scroll_amount = pattern["scroll_amount"]
                
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                
                # Natural pause
                pause = random.uniform(*pattern["pause_range"])
                time.sleep(pause)
                
                # Occasionally move mouse
                if random.random() < 0.3:
                    self.random_mouse_movement()
            
            self.logger.debug(f"Completed {scroll_type} scroll pattern")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during natural scroll: {e}")
            return False
    
    def random_mouse_movement(self):
        """Simulate natural human mouse movements"""
        try:
            # Get current window size
            window_size = self.driver.get_window_size()
            width = window_size['width']
            height = window_size['height']
            
            # Ensure minimum window size
            if width < 200 or height < 200:
                self.logger.debug("Window too small for mouse movement, skipping")
                return
            
            # Human-like mouse movement with multiple micro-movements
            num_movements = random.randint(3, 7)
            
            for i in range(num_movements):
                # Small, natural movements like human would make
                small_offset_x = random.randint(-50, 50)
                small_offset_y = random.randint(-30, 30)
                
                try:
                    # Move with natural speed and slight curve
                    self.actions.move_by_offset(small_offset_x, small_offset_y).perform()
                    
                    # Human-like pause between movements
                    time.sleep(random.uniform(0.1, 0.4))
                    
                    # Sometimes add a tiny correction movement (like human adjusting)
                    if random.random() < 0.3:  # 30% chance
                        correction_x = random.randint(-10, 10)
                        correction_y = random.randint(-5, 5)
                        self.actions.move_by_offset(correction_x, correction_y).perform()
                        time.sleep(random.uniform(0.05, 0.2))
                        
                except:
                    break
            
            # Final settling pause (like human finding comfortable position)
            time.sleep(random.uniform(0.2, 0.8))
            
        except Exception as e:
            self.logger.debug(f"Mouse movement skipped: {e}")
            # Don't log as error since this is not critical
    
    def click_internal_links(self, max_clicks=3):
        """Click on internal links to build browsing history"""
        try:
            # Find internal links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            internal_links = []
            
            current_domain = urlparse(self.driver.current_url).netloc
            
            for link in links:
                try:
                    href = link.get_attribute("href")
                    if href and urlparse(href).netloc == current_domain:
                        if link.is_displayed() and link.is_enabled():
                            internal_links.append(link)
                except:
                    continue
            
            # Click on random internal links
            clicks_made = 0
            for _ in range(min(max_clicks, len(internal_links))):
                if not internal_links:
                    break
                
                link = random.choice(internal_links)
                internal_links.remove(link)
                
                try:
                    # Scroll to link
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(random.uniform(0.5, 1.5))
                    
                    # Click link
                    link.click()
                    clicks_made += 1
                    
                    # Wait for page load
                    time.sleep(random.uniform(2, 5))
                    
                    # Go back
                    self.driver.back()
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    self.logger.debug(f"Could not click link: {e}")
                    continue
            
            self.logger.debug(f"Clicked {clicks_made} internal links")
            return clicks_made
            
        except Exception as e:
            self.logger.error(f"Error clicking internal links: {e}")
            return 0


class MultiloginProfileWarmer:
    """Main class for Multilogin profile warming"""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger('multilogin_profile_warmer')
        self.config = WarmingConfiguration()
        self.schedule_manager = WarmingScheduleManager()  # Use Google dorking technique
        self.timing_system = AdvancedTimingSystem(self.config)
        self.storage_manager = StorageManager(driver, self.config)
        self.cookie_manager = CookieManager(driver, self.config)
        self.behavior = HumanLikeBehavior(driver, self.timing_system)
        
        self.logger.info("Multilogin Profile Warmer initialized")
    
    def apply_stealth_settings(self):
        """Apply stealth settings to the browser"""
        try:
            # Set user agent
            user_agent = self.config.get('stealth.user_agent')
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": user_agent
            })
            
            # Set window size
            window_size = self.config.get('stealth.window_size', (1920, 1080))
            self.driver.set_window_size(window_size[0], window_size[1])
            
            # Inject stealth scripts (with error handling)
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
                    // Override plugins (only if not already defined)
                    if (!navigator.plugins || navigator.plugins.length === 0) {
                        Object.defineProperty(navigator, 'plugins', {
                            get: () => [1, 2, 3, 4, 5],
                        });
                    }
                } catch(e) {
                    // Ignore if already defined
                }
                
                try {
                    // Override languages (only if not already defined)
                    if (!navigator.languages || navigator.languages.length === 0) {
                        Object.defineProperty(navigator, 'languages', {
                            get: () => ['en-US', 'en'],
                        });
                    }
                } catch(e) {
                    // Ignore if already defined
                }
            """
            
            self.driver.execute_script(stealth_script)
            self.logger.info("Applied stealth settings")
            
        except Exception as e:
            self.logger.error(f"Error applying stealth settings: {e}")
    
    def simulate_referrer_visit(self, referrer_domain, target_url):
        """Simulate coming from a referrer domain"""
        try:
            # Visit referrer first
            referrer_url = f"https://{referrer_domain}"
            self.logger.info(f"Simulating referrer visit: {referrer_url}")
            
            self.driver.get(referrer_url)
            self.timing_system.human_like_delay("normal")
            
            # Simulate some activity on referrer
            self.behavior.natural_scroll("scanning")
            self.timing_system.human_like_delay("reading")
            
            # Navigate to target with referrer
            self.driver.get(target_url)
            
            # Set referrer cookie
            target_domain = urlparse(target_url).netloc
            self.cookie_manager.set_referrer_cookie(referrer_domain, target_domain)
            
            self.logger.info(f"Completed referrer simulation: {referrer_domain} -> {target_url}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error simulating referrer visit: {e}")
            return False
    
    def execute_google_dorking_activity(self, activity):
        """Execute Google dorking activity for natural profile warming"""
        try:
            query = activity['query']
            dwell_time = activity['dwell_time']
            
            self.logger.info(f"🔍 Google dorking: '{query}'")
            
            # Step 1: Go to Google with natural delays
            self.driver.get("https://www.google.com")
            
            # Wait longer to appear more natural (like human loading page)
            time.sleep(random.uniform(2, 5))
            
            # Human-like behavior: scroll a bit (like checking the page)
            if random.random() < 0.7:  # 70% chance
                scroll_amount = random.randint(100, 300)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(1, 3))
                
                # Add human hesitation
                self.add_human_hesitation()
                
                # Scroll back up
                self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount//2});")
                time.sleep(random.uniform(0.5, 1.5))
            
            # Step 2: Find search box and type query
            try:
                search_box = self.driver.find_element(By.NAME, "q")
                
                # Human-like behavior: move mouse to search box first
                self.behavior.random_mouse_movement()
                time.sleep(random.uniform(0.5, 1.5))
                
                # Click on search box (like human would)
                search_box.click()
                time.sleep(random.uniform(0.3, 0.8))
                
                # Clear and start typing
                search_box.clear()
                time.sleep(random.uniform(0.2, 0.5))
                
                # Use human-like typing with potential mistakes
                self.simulate_human_typing_mistakes(search_box, query)
                
                # Human-like pause before submitting (like reading what they typed)
                time.sleep(random.uniform(2, 5))
                
                # Sometimes humans hesitate before submitting (like double-checking)
                if random.random() < 0.3:  # 30% chance
                    time.sleep(random.uniform(1, 3))
                    
                    # Sometimes they might clear and retype part of the query
                    if random.random() < 0.2:  # 20% chance
                        # Move cursor to middle and retype last few characters
                        search_box.send_keys(Keys.ARROW_LEFT * 3)
                        time.sleep(random.uniform(0.5, 1))
                        search_box.send_keys(Keys.DELETE * 2)
                        time.sleep(random.uniform(0.3, 0.8))
                        search_box.send_keys("quotes")  # Common insurance term
                        time.sleep(random.uniform(0.5, 1.5))
                
                # Step 3: Submit search
                search_box.send_keys(Keys.RETURN)
                self.timing_system.human_like_delay("normal")
                
                # Step 4: Click on random search result with human-like behavior
                search_results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
                if search_results:
                    # Skip first result (usually ads) and click on random organic result
                    organic_results = search_results[1:4]  # Take results 2-4
                    if organic_results:
                        random_result = random.choice(organic_results)
                        self.logger.info(f"📄 Clicking on search result: {random_result.text[:50]}...")
                        
                        # Human-like behavior: hover before clicking
                        try:
                            # Hover over the result first (like human would)
                            self.actions.move_to_element(random_result).perform()
                            time.sleep(random.uniform(0.5, 1.5))
                            
                            # Sometimes humans scroll to see more results before clicking
                            if random.random() < 0.4:  # 40% chance
                                self.driver.execute_script("window.scrollBy(0, 200);")
                                time.sleep(random.uniform(1, 2))
                                self.driver.execute_script("window.scrollBy(0, -100);")
                                time.sleep(random.uniform(0.5, 1))
                            
                            # Click the result
                            random_result.click()
                        except:
                            # If direct click fails, try clicking parent link
                            try:
                                parent_link = random_result.find_element(By.XPATH, "./..")
                                self.actions.move_to_element(parent_link).perform()
                                time.sleep(random.uniform(0.3, 0.8))
                                parent_link.click()
                            except:
                                # If still fails, use JavaScript click
                                self.driver.execute_script("arguments[0].click();", random_result)
                        
                        self.timing_system.human_like_delay("normal")
                        
                        # Step 5: Natural browsing behavior
                        self.perform_natural_browsing(dwell_time)
                        
                        return True
                    else:
                        self.logger.warning("No organic search results found")
                        return False
                else:
                    self.logger.warning("No search results found")
                    return False
                    
            except Exception as e:
                self.logger.error(f"Error during Google search: {e}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error executing Google dorking activity: {e}")
            return False
    
    def perform_natural_browsing(self, dwell_time):
        """Perform natural human browsing behavior on the current page"""
        try:
            # Human-like reading behavior
            reading_time = random.uniform(3, 8)  # Time to "read" the page
            time.sleep(reading_time)
            
            # Random scroll behavior with human-like patterns
            scroll_actions = random.randint(4, 10)
            for i in range(scroll_actions):
                # Human-like scroll patterns
                if i < scroll_actions // 2:
                    # First half: mostly scroll down (like reading)
                    scroll_amount = random.randint(150, 400)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                else:
                    # Second half: mix of up and down (like reviewing)
                    scroll_amount = random.randint(100, 300)
                    if random.random() < 0.6:  # 60% chance to scroll down
                        self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    else:  # 40% chance to scroll up
                        self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
                
                # Human-like pause between scrolls (like reading)
                time.sleep(random.uniform(1.5, 4))
                
                # Sometimes pause longer (like human getting distracted)
                if random.random() < 0.2:  # 20% chance
                    time.sleep(random.uniform(3, 8))
            
            # Random mouse movements (like human exploring)
            if random.random() < 0.8:  # 80% chance
                self.behavior.random_mouse_movement()
            
            # Random hover over elements (like human exploring)
            if random.random() < 0.6:  # 60% chance
                try:
                    hover_elements = self.driver.find_elements(By.CSS_SELECTOR, "a, button, img")
                    if hover_elements:
                        random_element = random.choice(hover_elements)
                        if random_element.is_displayed():
                            self.actions.move_to_element(random_element).perform()
                            time.sleep(random.uniform(1, 3))
                except:
                    pass
            
            # Random click on safe elements (like human exploring)
            if random.random() < 0.3:  # 30% chance
                try:
                    safe_elements = self.driver.find_elements(By.CSS_SELECTOR, "a, button")
                    if safe_elements:
                        random_element = random.choice(safe_elements)
                        if random_element.is_displayed() and random_element.is_enabled():
                            # Hover before clicking (like human)
                            self.actions.move_to_element(random_element).perform()
                            time.sleep(random.uniform(0.5, 1.5))
                            random_element.click()
                            time.sleep(random.uniform(2, 5))
                except:
                    pass  # Ignore click errors
            
            # Calculate remaining time and wait
            time_used = reading_time + (scroll_actions * 2.5) + 5  # Approximate time used
            remaining_time = dwell_time - time_used
            if remaining_time > 0:
                time.sleep(remaining_time)
                
        except Exception as e:
            self.logger.error(f"Error during natural browsing: {e}")
    
    def add_human_hesitation(self):
        """Add random human-like hesitation and pauses"""
        try:
            # Random hesitation patterns
            hesitation_types = [
                "scroll_pause",      # Pause while scrolling
                "reading_pause",     # Pause like reading
                "thinking_pause",    # Pause like thinking
                "distraction_pause"  # Pause like getting distracted
            ]
            
            hesitation_type = random.choice(hesitation_types)
            
            if hesitation_type == "scroll_pause":
                # Pause in middle of scrolling (like human reading)
                time.sleep(random.uniform(2, 5))
                
            elif hesitation_type == "reading_pause":
                # Longer pause like human reading content
                time.sleep(random.uniform(3, 8))
                
            elif hesitation_type == "thinking_pause":
                # Pause like human thinking about next action
                time.sleep(random.uniform(1, 4))
                
            elif hesitation_type == "distraction_pause":
                # Longer pause like human got distracted
                time.sleep(random.uniform(5, 12))
                
        except Exception as e:
            self.logger.debug(f"Error in human hesitation: {e}")
    
    def simulate_human_typing_mistakes(self, search_box, query):
        """Simulate human typing mistakes and corrections"""
        try:
            # 20% chance to make a typing mistake
            if random.random() < 0.2:
                # Make a mistake in the middle of typing
                mistake_position = len(query) // 2
                
                # Type up to mistake position
                for i, char in enumerate(query[:mistake_position]):
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.3))
                
                # Make a mistake (wrong character)
                mistake_char = random.choice("qwertyuiopasdfghjklzxcvbnm")
                search_box.send_keys(mistake_char)
                time.sleep(random.uniform(0.2, 0.5))
                
                # Realize mistake and backspace
                search_box.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.3, 0.8))
                
                # Continue typing correctly
                for char in query[mistake_position:]:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.3))
            else:
                # Normal typing without mistakes
                for char in query:
                    search_box.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.3))
                    
        except Exception as e:
            self.logger.debug(f"Error in typing simulation: {e}")
    
    def warm_profile_activity(self, activity):
        """Execute a single warming activity"""
        try:
            # Check if this is a Google dorking activity
            if activity.get('type') == 'google_dorking':
                return self.execute_google_dorking_activity(activity)
            
            # Legacy activity handling
            url = activity['url']
            action = activity['action']
            dwell_time = activity['dwell_time']
            
            self.logger.info(f"Executing activity: {action} at {url}")
            
            # Determine if we should use a referrer
            use_referrer = random.random() < 0.4  # 40% chance
            
            if use_referrer:
                referrer_sources = self.config.get('referrers.referrer_sources', [])
                referrer_domain = random.choice(referrer_sources)
                self.simulate_referrer_visit(referrer_domain, url)
            else:
                self.driver.get(url)
            
            # Wait for page load
            self.timing_system.human_like_delay("normal")
            
            # Inject storage data
            domain = urlparse(url).netloc
            storage_types = self.config.get('storage.storage_data_types', ['analytics'])
            for storage_type in random.sample(storage_types, random.randint(1, 3)):
                self.storage_manager.inject_storage_data(domain, storage_type)
            
            # Create IndexedDB data
            if self.config.get('storage.enable_indexed_db', True):
                self.storage_manager.create_indexed_db_data(domain)
            
            # Inject cookies
            cookie_types = self.config.get('cookies.cookie_categories', ['analytics'])
            for cookie_type in random.sample(cookie_types, random.randint(1, 2)):
                self.cookie_manager.inject_realistic_cookies(domain, cookie_type)
            
            # Perform activity-specific behavior
            if "scroll" in action.lower() or "read" in action.lower():
                self.behavior.natural_scroll("reading")
            elif "calculator" in action.lower() or "interact" in action.lower():
                self.behavior.natural_scroll("exploring")
                self.behavior.click_internal_links(2)
            elif "compare" in action.lower():
                self.behavior.natural_scroll("scanning")
                self.behavior.click_internal_links(3)
            else:
                self.behavior.natural_scroll("reading")
            
            # Dwell time
            actual_dwell = min(dwell_time, 300)  # Cap at 5 minutes
            self.timing_system.reading_pause("medium")
            
            # Additional random mouse movements
            for _ in range(random.randint(2, 5)):
                self.behavior.random_mouse_movement()
                time.sleep(random.uniform(0.5, 2))
            
            self.logger.info(f"Completed activity: {action} (dwell: {actual_dwell}s)")
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing warming activity: {e}")
            return False
    
    def run_daily_warming(self, day):
        """Run warming activities for a specific day"""
        try:
            activities = self.schedule_manager.get_activities_for_day(day)
            if not activities:
                self.logger.warning(f"No activities found for day {day}")
                return False
            
            self.logger.info(f"Starting warming for day {day} with {len(activities)} activities")
            
            successful_activities = 0
            for i, activity in enumerate(activities):
                try:
                    self.logger.info(f"Activity {i+1}/{len(activities)}: {activity['action']}")
                    
                    if self.warm_profile_activity(activity):
                        successful_activities += 1
                    
                    # Delay between activities
                    if i < len(activities) - 1:  # Don't delay after last activity
                        delay = activity.get('inter_action_delay', 60)
                        actual_delay = min(delay, 300)  # Cap at 5 minutes
                        time.sleep(actual_delay)
                    
                except Exception as e:
                    self.logger.error(f"Error in activity {i+1}: {e}")
                    continue
            
            self.logger.info(f"Completed day {day}: {successful_activities}/{len(activities)} activities successful")
            return successful_activities > 0
            
        except Exception as e:
            self.logger.error(f"Error running daily warming: {e}")
            return False
    
    def run_full_warming_schedule(self, start_day=1, end_day=14):
        """Run the complete warming schedule"""
        try:
            self.logger.info(f"Starting full warming schedule (days {start_day}-{end_day})")
            
            # Apply stealth settings
            self.apply_stealth_settings()
            
            for day in range(start_day, end_day + 1):
                self.logger.info(f"=== DAY {day} WARMING ===")
                
                if self.run_daily_warming(day):
                    self.logger.info(f"Day {day} warming completed successfully")
                else:
                    self.logger.warning(f"Day {day} warming had issues")
                
                # Delay between days (except after last day)
                if day < end_day:
                    self.timing_system.between_sessions_delay()
            
            self.logger.info("Full warming schedule completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error running full warming schedule: {e}")
            return False
    
    def run_single_session(self, max_activities=5, config=None):
        """Run a single warming session with random activities"""
        try:
            self.logger.info(f"Starting single warming session (max {max_activities} activities)")
            
            # Apply stealth settings
            self.apply_stealth_settings()
            
            activities_completed = 0
            for i in range(max_activities):
                activity = self.schedule_manager.get_next_activity(config=config)
                if not activity:
                    self.logger.info("No more activities in schedule")
                    break
                
                self.logger.info(f"Activity {i+1}/{max_activities}: {activity['category']} - '{activity['query']}'")
                
                if self.warm_profile_activity(activity):
                    activities_completed += 1
                
                # Random delay between activities (shorter for quick mode)
                delay = random.uniform(10, 30)  # 10-30 seconds for quick mode
                self.logger.info(f"Waiting {delay:.1f} seconds before next activity...")
                time.sleep(delay)
            
            self.logger.info(f"Single session completed: {activities_completed} activities")
            return activities_completed > 0
            
        except Exception as e:
            self.logger.error(f"Error running single session: {e}")
            return False


# =============================================================================
# MULTILOGIN SCRIPT RUNNER INTEGRATION
# =============================================================================

def run_multilogin_profile_warming(driver, warming_mode="single_session", day_range=None):
    """
    Main function untuk menjalankan profile warming di Multilogin Script Runner
    
    Args:
        driver: WebDriver instance dari Multilogin
        warming_mode: Mode warming ('single_session', 'daily', 'full_schedule')
        # Using Google dorking technique - no external files needed
        day_range: Range hari untuk warming (tuple: start_day, end_day)
    
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    try:
        logger = logging.getLogger('multilogin_profile_warmer')
        logger.info("=== MULTILOGIN PROFILE WARMER STARTED ===")
        
        # Initialize warmer
        warmer = MultiloginProfileWarmer(driver)  # Use Google dorking technique
        
        # Apply stealth settings
        warmer.apply_stealth_settings()
        
        if warming_mode == "single_session":
            logger.info("Running single session warming...")
            success = warmer.run_single_session(max_activities=5)
            
        elif warming_mode == "daily":
            if not day_range:
                day_range = (1, 1)  # Default: hari 1 saja
            logger.info(f"Running daily warming for day {day_range[0]}...")
            success = warmer.run_daily_warming(day_range[0])
            
        elif warming_mode == "full_schedule":
            if not day_range:
                day_range = (1, 14)  # Default: 14 hari
            logger.info(f"Running full schedule warming (days {day_range[0]}-{day_range[1]})...")
            success = warmer.run_full_warming_schedule(day_range[0], day_range[1])
            
        else:
            logger.error(f"Unknown warming mode: {warming_mode}")
            return False
        
        if success:
            logger.info("=== PROFILE WARMING COMPLETED SUCCESSFULLY ===")
        else:
            logger.warning("=== PROFILE WARMING COMPLETED WITH ISSUES ===")
        
        return success
        
    except Exception as e:
        logger.error(f"Error in profile warming: {e}")
        return False


def quick_warm_profile(driver, num_activities=3, config=None):
    """
    Quick profile warming untuk Multilogin - jalankan beberapa aktivitas warming
    
    Args:
        driver: WebDriver instance dari Multilogin
        num_activities: Jumlah aktivitas warming yang akan dijalankan
        config: Konfigurasi untuk kategori dan weight queries
    
    Returns:
        bool: True jika berhasil
    """
    try:
        logger = logging.getLogger('multilogin_profile_warmer')
        logger.info(f"Starting quick warming with {num_activities} activities")
        
        # Initialize warmer
        warmer = MultiloginProfileWarmer(driver)
        warmer.apply_stealth_settings()
        
        # Run single session with specified number of activities
        success = warmer.run_single_session(max_activities=num_activities, config=config)
        
        if success:
            logger.info("✅ Quick profile warming completed successfully!")
        else:
            logger.warning("❌ Quick profile warming had issues")
            
        return success
        
    except Exception as e:
        logger = logging.getLogger('multilogin_profile_warmer')
        logger.error(f"❌ Error in quick warming: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return False


def warm_profile_for_day(driver, day=1):
    """
    Warm profile untuk hari tertentu
    
    Args:
        driver: WebDriver instance dari Multilogin
        day: Hari yang akan di-warm (1-14)
        # Using Google dorking technique - no external files needed
    
    Returns:
        bool: True jika berhasil
    """
    return run_multilogin_profile_warming(driver, "daily", day_range=(day, day))


def warm_profile_full_schedule(driver, start_day=1, end_day=14):
    """
    Warm profile dengan jadwal lengkap 14 hari
    
    Args:
        driver: WebDriver instance dari Multilogin
        # Using Google dorking technique - no external files needed
        start_day: Hari mulai (default: 1)
        end_day: Hari akhir (default: 14)
    
    Returns:
        bool: True jika berhasil
    """
    return run_multilogin_profile_warming(driver, "full_schedule", day_range=(start_day, end_day))


# =============================================================================
# MULTILOGIN SCRIPT RUNNER ENTRY POINT
# =============================================================================

def main():
    """
    Entry point untuk Multilogin Script Runner
    Script ini akan otomatis dijalankan oleh Multilogin
    """
    try:
        # Setup logging
        logger = logging.getLogger('multilogin_profile_warmer')
        logger.info("=== MULTILOGIN PROFILE WARMER STARTED ===")
        
        # Di Multilogin Script Runner, driver sudah tersedia sebagai variabel global
        # Script ini akan dijalankan dalam context Multilogin yang menyediakan driver
        
        # Mode warming yang bisa dipilih:
        # 1. "quick" - Warming cepat 3 aktivitas
        # 2. "daily" - Warming untuk hari tertentu
        # 3. "full" - Warming jadwal lengkap 14 hari
        
        warming_mode = "quick"  # Ubah sesuai kebutuhan
        logger.info(f"Warming mode: {warming_mode}")
        
        # Driver tersedia di Multilogin environment
        # Jika error "driver is not defined", pastikan script dijalankan di Multilogin
        
        if warming_mode == "quick":
            # Quick warming - 3 aktivitas random
            logger.info("Starting quick profile warming...")
            success = quick_warm_profile(driver, num_activities=3)
            
        elif warming_mode == "daily":
            # Daily warming - hari 1 dengan Google dorking
            logger.info("Starting daily warming for day 1 with Google dorking technique")
            success = warm_profile_for_day(driver, day=1)
            
        elif warming_mode == "full":
            # Full schedule warming - 14 hari dengan Google dorking
            logger.info("Starting full schedule warming with Google dorking technique")
            success = warm_profile_full_schedule(driver, start_day=1, end_day=14)
        
        else:
            logger.error(f"Unknown warming mode: {warming_mode}")
            success = False
        
        if success:
            logger.info("✅ Profile warming completed successfully!")
            print("✅ Profile warming completed successfully!")
        else:
            logger.warning("❌ Profile warming had issues")
            print("❌ Profile warming had issues")
            
        return success
        
    except Exception as e:
        logger.error(f"❌ Error in main warming function: {e}")
        print(f"❌ Error in main warming function: {e}")
        return False


# =============================================================================
# CONFIGURATION FOR MULTILOGIN
# =============================================================================

# Konfigurasi yang bisa diubah untuk Multilogin
MULTILOGIN_CONFIG = {
    "warming_mode": "quick",  # "quick", "daily", "full"
    # Using Google dorking technique - no external files needed
    "day_to_warm": 1,  # Untuk mode "daily"
    "start_day": 1,    # Untuk mode "full"
    "end_day": 14,     # Untuk mode "full"
    "num_quick_activities": 30,  # Untuk mode "quick"
    "enable_stealth": True,
    "enable_storage_injection": True,
    "enable_cookie_management": True,
    "enable_referrer_simulation": True,
    
    # Query category - pilih satu kategori yang sesuai dengan profile browser
    "preferred_category": "ai",  # "insurance", "loans", "loans_indonesia", "ai", "crypto", "erp_crm"
    
    # Available categories for reference:
    # - "insurance": Insurance-related queries (24 queries)
    # - "loans": Loans and financing queries (32 queries - International) 
    # - "loans_indonesia": Loans Indonesia queries (20 queries - Bahasa Indonesia)
    # - "ai": AI and technology queries (24 queries)
    # - "crypto": Cryptocurrency queries (24 queries)
    # - "erp_crm": ERP/CRM business software queries (24 queries)
}

# =============================================================================
# INTEGRATION WITH EXISTING AUTOMATION SCRIPTS
# =============================================================================

def integrate_with_advanced_robot(driver):
    """
    Integrasi dengan advanced_website_robot.py yang sudah ada
    Jalankan warming sebelum automation utama
    """
    try:
        logger = logging.getLogger('multilogin_profile_warmer')
        logger.info("Integrating profile warming with advanced website robot...")
        
        # Quick warming sebelum automation utama
        success = quick_warm_profile(driver, num_activities=3)
        
        if success:
            logger.info("Profile warming completed, ready for main automation")
            return True
        else:
            logger.warning("Profile warming had issues, but continuing with automation")
            return False
            
    except Exception as e:
        logger.error(f"Error in integration: {e}")
        return False


def warm_before_adsense_automation(driver):
    """
    Warming khusus sebelum automation AdSense
    Fokus pada aktivitas yang relevan dengan AdSense
    """
    try:
        logger = logging.getLogger('multilogin_profile_warmer')
        logger.info("Running AdSense-focused profile warming...")
        
        # Initialize warmer dengan fokus AdSense
        warmer = MultiloginProfileWarmer(driver)
        warmer.apply_stealth_settings()
        
        # Aktivitas khusus untuk AdSense warming
        adsense_activities = [
            {
                'url': 'https://google.com',
                'action': 'Open homepage and scroll (read)',
                'dwell_time': 120,
                'inter_action_delay': 60
            },
            {
                'url': 'https://youtube.com',
                'action': 'Open homepage and scroll (read)',
                'dwell_time': 180,
                'inter_action_delay': 90
            },
            {
                'url': 'https://facebook.com',
                'action': 'Open homepage and scroll (read)',
                'dwell_time': 150,
                'inter_action_delay': 75
            }
        ]
        
        successful_activities = 0
        for activity in adsense_activities:
            if warmer.warm_profile_activity(activity):
                successful_activities += 1
        
        logger.info(f"AdSense warming completed: {successful_activities}/{len(adsense_activities)} activities")
        return successful_activities > 0
        
    except Exception as e:
        logger.error(f"Error in AdSense warming: {e}")
        return False


# =============================================================================
# MULTILOGIN SCRIPT RUNNER COMPATIBILITY
# =============================================================================

# Setup logging (mengikuti pattern advanced_website_robot.py)
setup_logging()

# Input parameters (mengikuti pattern advanced_website_robot.py)
inputparams = inputparams or {}

# Default configuration
warming_mode = "quick"
# CSV data is now embedded in the script - no external file needed
day_to_warm = 1
start_day = 1
end_day = 14
num_quick_activities = 30

# Override with input parameters
if 'warming_mode' in inputparams:
    warming_mode = inputparams['warming_mode']
if 'day_to_warm' in inputparams:
    day_to_warm = inputparams['day_to_warm']
if 'start_day' in inputparams:
    start_day = inputparams['start_day']
if 'end_day' in inputparams:
    end_day = inputparams['end_day']
if 'num_quick_activities' in inputparams:
    num_quick_activities = inputparams['num_quick_activities']

logging.info('Multilogin Profile Warmer started')
logging.info(f'inputparams: {inputparams}')
logging.info(f'warming_mode: {warming_mode}')
logging.info('Using Google dorking technique (no external files needed)')

# Create and run warmer (mengikuti pattern advanced_website_robot.py)
try:
    # Check if driver is available
    if 'driver' not in globals():
        logging.error("❌ Driver not available in global scope")
        raise Exception("Driver not available in global scope")
    
    logging.info("✅ Driver found, starting profile warming...")
    
    # Use MULTILOGIN_CONFIG for query categories
    config = MULTILOGIN_CONFIG
    
    # Log the selected category
    preferred_category = config.get('preferred_category', 'insurance')
    logging.info(f"Using query category: {preferred_category}")
    
    if warming_mode == "quick":
        logging.info(f"Starting quick warming with {num_quick_activities} activities")
        success = quick_warm_profile(driver, num_activities=num_quick_activities, config=config)
    elif warming_mode == "daily":
        logging.info(f"Starting daily warming for day {day_to_warm} with Google dorking technique")
        success = warm_profile_for_day(driver, day=day_to_warm)
    elif warming_mode == "full":
        logging.info(f"Starting full schedule warming (days {start_day}-{end_day}) with Google dorking technique")
        success = warm_profile_full_schedule(driver, start_day=start_day, end_day=end_day)
    else:
        logging.error(f"Unknown warming mode: {warming_mode}")
        success = False
    
    if success:
        logging.info("✅ Profile warming completed successfully!")
    else:
        logging.warning("❌ Profile warming had issues")
        
except NameError as e:
    logging.error(f"❌ NameError: {e}")
    logging.error("❌ Make sure script is running in Multilogin environment")
    success = False
except Exception as e:
    logging.error(f"❌ Error in profile warming: {e}")
    logging.error(f"❌ Error type: {type(e).__name__}")
    import traceback
    logging.error(f"❌ Traceback: {traceback.format_exc()}")
    success = False

# =============================================================================
# CONTOH PENGGUNAAN UNTUK BERBAGAI KATEGORI
# =============================================================================

"""
CONTOH KONFIGURASI UNTUK BERBAGAI KATEGORI:

1. INSURANCE PROFILE:
   MULTILOGIN_CONFIG["preferred_category"] = "insurance"
   # Akan menggunakan 24 insurance-related queries seperti:
   # - "best car insurance rates 2024"
   # - "geico vs progressive insurance"
   # - "insurance deductible explained"

2. LOANS PROFILE (International):
   MULTILOGIN_CONFIG["preferred_category"] = "loans"
   # Akan menggunakan 32 loans-related queries seperti:
   # - "best personal loans 2024"
   # - "small business loans 2024"
   # - "mortgage calculator"
   # - "auto loan rates"

3. LOANS INDONESIA PROFILE:
   MULTILOGIN_CONFIG["preferred_category"] = "loans_indonesia"
   # Akan menggunakan 20 loans Indonesia queries seperti:
   # - "kredit tanpa agunan terbaik 2024"
   # - "pinjaman online terpercaya"
   # - "kredit pemilikan rumah KPR"
   # - "kredit kendaraan bermotor KKB"

4. AI/TECH PROFILE:
   MULTILOGIN_CONFIG["preferred_category"] = "ai"
   # Akan menggunakan 24 AI-related queries seperti:
   # - "best AI tools 2024"
   # - "ChatGPT alternatives"
   # - "AI for small business"

5. CRYPTO PROFILE:
   MULTILOGIN_CONFIG["preferred_category"] = "crypto"
   # Akan menggunakan 24 crypto-related queries seperti:
   # - "best crypto exchanges 2024"
   # - "bitcoin trading strategies"
   # - "DeFi platforms 2024"

6. ERP/CRM PROFILE:
   MULTILOGIN_CONFIG["preferred_category"] = "erp_crm"
   # Akan menggunakan 24 ERP/CRM-related queries seperti:
   # - "best ERP systems 2024"
   # - "Salesforce vs HubSpot"
   # - "CRM for small business"

CARA MENGGUNAKAN:
1. Pilih kategori yang sesuai dengan profile browser yang akan di-warm
2. Set preferred_category di MULTILOGIN_CONFIG
3. Jalankan script di Multilogin
4. Script akan menggunakan query dari kategori yang dipilih secara konsisten
"""

# Untuk kompatibilitas dengan Multilogin Script Runner
if __name__ == "__main__":
    # Script akan dijalankan otomatis oleh Multilogin
    main()
