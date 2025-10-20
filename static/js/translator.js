/**
 * Translator.js - نظام الترجمة لـ SH Parts
 * يدعم العربية والإنجليزية
 */

let translations = {};
let currentLanguage = 'ar';

// تحميل الترجمات
async function loadTranslations() {
    try {
        const lang = localStorage.getItem('language') || 'ar';
        currentLanguage = lang;
        
        const response = await fetch(`/static/js/translations/${lang}.json`);
        if (!response.ok) {
            throw new Error(`Failed to load translations: ${response.status}`);
        }
        
        translations = await response.json();
        console.log(`✅ Translations loaded for: ${lang}`, Object.keys(translations).length, 'keys');
        
        // تطبيق الترجمات على الصفحة
        applyTranslations();
        
        return translations;
    } catch (error) {
        console.error('❌ Error loading translations:', error);
        translations = {};
        return {};
    }
}

// دالة الترجمة الرئيسية
function t(key, defaultValue = null) {
    if (!key) return defaultValue || '';
    
    const translation = translations[key];
    
    if (translation) {
        return translation;
    }
    
    // إذا لم توجد الترجمة، استخدم القيمة الافتراضية أو المفتاح نفسه
    if (defaultValue) {
        return defaultValue;
    }
    
    console.warn(`⚠️ Translation missing for key: "${key}"`);
    return key;
}

// تطبيق الترجمات على العناصر الموجودة
function applyTranslations() {
    // ترجمة العناصر مع data-translate
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        const translation = t(key);
        
        if (translation && translation !== key) {
            // حفظ النص الأصلي إذا لم يكن محفوظاً
            if (!element.hasAttribute('data-original-text')) {
                element.setAttribute('data-original-text', element.textContent.trim());
            }
            element.textContent = translation;
        }
    });
    
    // ترجمة placeholders
    document.querySelectorAll('[data-translate-placeholder]').forEach(element => {
        const key = element.getAttribute('data-translate-placeholder');
        const translation = t(key);
        
        if (translation && translation !== key) {
            element.setAttribute('placeholder', translation);
        }
    });
    
    // ترجمة title attributes
    document.querySelectorAll('[data-translate-title]').forEach(element => {
        const key = element.getAttribute('data-translate-title');
        const translation = t(key);
        
        if (translation && translation !== key) {
            element.setAttribute('title', translation);
        }
    });
}

// تبديل اللغة
async function switchLanguage(lang) {
    if (lang === currentLanguage) {
        return; // نفس اللغة
    }
    
    localStorage.setItem('language', lang);
    currentLanguage = lang;
    
    // تحديث اتجاه الصفحة
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    
    // تحديث Bootstrap CSS
    const bootstrapLink = document.querySelector('link[href*="bootstrap"]');
    if (bootstrapLink) {
        if (lang === 'ar') {
            bootstrapLink.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css';
        } else {
            bootstrapLink.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css';
        }
    }
    
    // إعادة تحميل الترجمات
    await loadTranslations();
    
    console.log(`✅ Language switched to: ${lang}`);
}

// تهيئة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', async function() {
    console.log('🌍 Initializing translator...');
    await loadTranslations();
    
    // إضافة مراقب للتغييرات في DOM لترجمة العناصر الجديدة
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1) { // عنصر HTML
                    // ترجمة العنصر الجديد وأطفاله
                    if (node.hasAttribute && node.hasAttribute('data-translate')) {
                        const key = node.getAttribute('data-translate');
                        const translation = t(key);
                        if (translation && translation !== key) {
                            node.textContent = translation;
                        }
                    }
                    
                    // ترجمة الأطفال
                    node.querySelectorAll && node.querySelectorAll('[data-translate]').forEach(el => {
                        const key = el.getAttribute('data-translate');
                        const translation = t(key);
                        if (translation && translation !== key) {
                            el.textContent = translation;
                        }
                    });
                }
            });
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// تصدير الدوال للاستخدام العام
window.t = t;
window.switchLanguage = switchLanguage;
window.applyTranslations = applyTranslations;
window.loadTranslations = loadTranslations;
