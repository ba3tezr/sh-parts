/**
 * SH Parts Translation System
 * نظام ترجمة موحد لـ JavaScript
 * 
 * @author Zakee Tahawi
 * @version 1.0
 */

class Translator {
    constructor() {
        // Get current language from HTML lang attribute or default to Arabic
        this.currentLang = document.documentElement.lang || 'ar';
        this.translations = {};
        this.fallbackLang = 'ar';
        this.isLoaded = false;
        
        // Load translations on initialization
        this.loadTranslations();
    }

    /**
     * Load translation file for current language
     */
    async loadTranslations() {
        try {
            const response = await fetch(`/static/js/translations/${this.currentLang}.json`);
            if (!response.ok) {
                throw new Error(`Failed to load translations for ${this.currentLang}`);
            }
            this.translations = await response.json();
            this.isLoaded = true;
            console.log(`✅ Translations loaded for: ${this.currentLang}`);
        } catch (error) {
            console.error('❌ Failed to load translations:', error);
            // Try to load fallback language
            if (this.currentLang !== this.fallbackLang) {
                try {
                    const fallbackResponse = await fetch(`/static/js/translations/${this.fallbackLang}.json`);
                    this.translations = await fallbackResponse.json();
                    this.isLoaded = true;
                    console.warn(`⚠️ Loaded fallback language: ${this.fallbackLang}`);
                } catch (fallbackError) {
                    console.error('❌ Failed to load fallback translations:', fallbackError);
                }
            }
        }
    }

    /**
     * Translate a key
     * @param {string} key - Translation key
     * @param {object} params - Parameters to replace in translation {name: 'value'}
     * @returns {string} Translated text
     */
    t(key, params = {}) {
        // Get translation or return key if not found
        let text = this.translations[key] || key;
        
        // Replace placeholders: {name}, {count}, etc.
        Object.keys(params).forEach(param => {
            const placeholder = `{${param}}`;
            text = text.replace(new RegExp(placeholder, 'g'), params[param]);
        });
        
        return text;
    }

    /**
     * Translate with plural support
     * @param {string} key - Translation key base
     * @param {number} count - Count for plural
     * @param {object} params - Additional parameters
     * @returns {string} Translated text with correct plural form
     */
    tn(key, count, params = {}) {
        let pluralKey;
        
        // Arabic plural rules (6 forms)
        if (this.currentLang === 'ar') {
            if (count === 0) {
                pluralKey = `${key}_zero`;
            } else if (count === 1) {
                pluralKey = `${key}_one`;
            } else if (count === 2) {
                pluralKey = `${key}_two`;
            } else if (count >= 3 && count <= 10) {
                pluralKey = `${key}_few`;
            } else if (count >= 11 && count <= 99) {
                pluralKey = `${key}_many`;
            } else {
                pluralKey = `${key}_other`;
            }
        } else {
            // English plural rules (2 forms)
            pluralKey = count === 1 ? `${key}_one` : `${key}_other`;
        }
        
        // Fallback to base key if plural form not found
        if (!this.translations[pluralKey]) {
            pluralKey = key;
        }
        
        return this.t(pluralKey, { ...params, count });
    }

    /**
     * Check if translations are loaded
     * @returns {boolean}
     */
    isReady() {
        return this.isLoaded;
    }

    /**
     * Get current language
     * @returns {string}
     */
    getCurrentLanguage() {
        return this.currentLang;
    }

    /**
     * Change language and reload translations
     * @param {string} lang - Language code (ar, en)
     */
    async changeLanguage(lang) {
        if (lang === this.currentLang) {
            return;
        }
        
        this.currentLang = lang;
        this.isLoaded = false;
        await this.loadTranslations();
        
        // Update HTML lang attribute
        document.documentElement.lang = lang;
        
        // Update direction
        document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    }

    /**
     * Translate all elements with data-translate attribute
     */
    translatePage() {
        const elements = document.querySelectorAll('[data-translate]');
        elements.forEach(element => {
            const key = element.getAttribute('data-translate');
            if (key) {
                element.textContent = this.t(key);
            }
        });
    }
}

// Create global instance
window.translator = new Translator();

// Global shorthand functions
window.t = function(key, params) {
    return window.translator.t(key, params);
};

window.tn = function(key, count, params) {
    return window.translator.tn(key, count, params);
};

// Auto-translate page when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Wait for translations to load
    const checkLoaded = setInterval(function() {
        if (window.translator.isReady()) {
            clearInterval(checkLoaded);
            window.translator.translatePage();
        }
    }, 100);
    
    // Timeout after 5 seconds
    setTimeout(function() {
        clearInterval(checkLoaded);
    }, 5000);
});

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Translator;
}

