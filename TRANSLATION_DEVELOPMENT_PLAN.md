# 🚀 خطة تطويرية شاملة للترجمات - SH Parts Translation Roadmap

**المدة الإجمالية:** 5 أيام عمل (40 ساعة)  
**الأولوية:** عالية  
**المسؤول:** Zakee Tahawi

---

## 📊 نظرة عامة

### الهدف الرئيسي
تحويل نظام SH Parts إلى نظام متعدد اللغات بالكامل (عربي/إنجليزي) مع دعم RTL/LTR وترجمة شاملة لجميع العناصر.

### النطاق (Scope)
- ✅ ترجمة كاملة لجميع Templates (HTML)
- ✅ ترجمة كاملة لجميع نصوص JavaScript
- ✅ إكمال ملفات .po (453 نص)
- ✅ إضافة مبدل لغة في شاشة تسجيل الدخول
- ✅ نظام ترجمة موحد لـ JavaScript
- ✅ اختبارات شاملة للترجمات

---

## 📅 المراحل التفصيلية

---

## 🔵 المرحلة 1: إعداد البنية التحتية (يوم 1 - 8 ساعات)

### 1.1 إنشاء نظام ترجمة JavaScript (3 ساعات)

**الملفات المطلوبة:**
```
static/js/translations/
├── ar.json          # الترجمات العربية
├── en.json          # الترجمات الإنجليزية
└── translator.js    # محرك الترجمة
```

**محتوى `translator.js`:**
```javascript
// نظام ترجمة JavaScript موحد
class Translator {
    constructor() {
        this.currentLang = document.documentElement.lang || 'ar';
        this.translations = {};
        this.loadTranslations();
    }

    async loadTranslations() {
        try {
            const response = await fetch(`/static/js/translations/${this.currentLang}.json`);
            this.translations = await response.json();
        } catch (error) {
            console.error('Failed to load translations:', error);
        }
    }

    t(key, params = {}) {
        let text = this.translations[key] || key;
        // Replace placeholders: {name}, {count}, etc.
        Object.keys(params).forEach(param => {
            text = text.replace(`{${param}}`, params[param]);
        });
        return text;
    }

    // Plural support
    tn(key, count, params = {}) {
        const pluralKey = count === 1 ? `${key}_one` : `${key}_other`;
        return this.t(pluralKey, { ...params, count });
    }
}

// Global instance
window.translator = new Translator();
window.t = (key, params) => window.translator.t(key, params);
window.tn = (key, count, params) => window.translator.tn(key, count, params);
```

**محتوى `ar.json` (مثال):**
```json
{
    "loading": "جاري التحميل...",
    "error": "حدث خطأ",
    "success": "تمت العملية بنجاح",
    "confirm_delete": "هل أنت متأكد من الحذف؟",
    "confirm_delete_multiple": "هل أنت متأكد من حذف {count} عنصر؟",
    "no_data": "لا توجد بيانات",
    "search": "بحث",
    "filter": "تصفية",
    "export": "تصدير",
    "print": "طباعة",
    "save": "حفظ",
    "cancel": "إلغاء",
    "close": "إغلاق",
    "edit": "تعديل",
    "delete": "حذف",
    "view": "عرض",
    "add": "إضافة",
    "customers": "العملاء",
    "inventory": "المخزون",
    "sales": "المبيعات",
    "reports": "التقارير"
}
```

**محتوى `en.json` (مثال):**
```json
{
    "loading": "Loading...",
    "error": "An error occurred",
    "success": "Operation completed successfully",
    "confirm_delete": "Are you sure you want to delete?",
    "confirm_delete_multiple": "Are you sure you want to delete {count} items?",
    "no_data": "No data available",
    "search": "Search",
    "filter": "Filter",
    "export": "Export",
    "print": "Print",
    "save": "Save",
    "cancel": "Cancel",
    "close": "Close",
    "edit": "Edit",
    "delete": "Delete",
    "view": "View",
    "add": "Add",
    "customers": "Customers",
    "inventory": "Inventory",
    "sales": "Sales",
    "reports": "Reports"
}
```

**الاستخدام:**
```javascript
// قبل
alert('جاري التحميل...');

// بعد
alert(t('loading'));

// مع معاملات
alert(t('confirm_delete_multiple', { count: 5 }));
```

---

### 1.2 تحديث base.html لتحميل نظام الترجمة (1 ساعة)

**في `templates/base/base.html`:**
```html
<!-- Translation System -->
<script src="{% static 'js/translations/translator.js' %}"></script>
<script>
    // Set language from Django
    document.documentElement.lang = '{{ LANGUAGE_CODE }}';
</script>
```

---

### 1.3 إنشاء أداة لاستخراج النصوص (2 ساعات)

**ملف:** `scripts/extract_translations.py`

```python
#!/usr/bin/env python3
"""
أداة لاستخراج جميع النصوص من JavaScript وإضافتها لملفات الترجمة
"""
import re
import json
from pathlib import Path

def extract_from_js(file_path):
    """استخراج النصوص العربية من ملفات JavaScript"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن النصوص العربية في alert, confirm, innerHTML, etc.
    patterns = [
        r"alert\(['\"]([^'\"]+)['\"]\)",
        r"confirm\(['\"]([^'\"]+)['\"]\)",
        r"innerHTML\s*=\s*['\"]([^'\"]+)['\"]\)",
        r"textContent\s*=\s*['\"]([^'\"]+)['\"]\)",
    ]
    
    texts = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if any('\u0600' <= c <= '\u06FF' for c in match):  # Arabic chars
                texts.add(match)
    
    return texts

def main():
    # استخراج من جميع ملفات HTML
    templates_dir = Path('templates/pages')
    all_texts = set()
    
    for html_file in templates_dir.glob('*.html'):
        texts = extract_from_js(html_file)
        all_texts.update(texts)
    
    # حفظ في ملف JSON
    output = {text: text for text in sorted(all_texts)}
    
    with open('translations_to_add.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم استخراج {len(all_texts)} نص")

if __name__ == '__main__':
    main()
```

---

### 1.4 إضافة مبدل اللغة في شاشة تسجيل الدخول (2 ساعات)

**في `templates/pages/login.html`:**

```html
<!-- Language Switcher in Login Page -->
<div class="login-lang-switcher">
    <button type="button" class="lang-btn {% if LANGUAGE_CODE == 'ar' %}active{% endif %}" 
            onclick="changeLoginLanguage('ar')">
        <i class="bi bi-translate"></i> العربية
    </button>
    <button type="button" class="lang-btn {% if LANGUAGE_CODE == 'en' %}active{% endif %}" 
            onclick="changeLoginLanguage('en')">
        <i class="bi bi-translate"></i> English
    </button>
</div>

<style>
.login-lang-switcher {
    position: absolute;
    top: 20px;
    right: 20px;
    display: flex;
    gap: 10px;
    z-index: 10;
}

.login-lang-switcher .lang-btn {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid #e0e0e0;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 14px;
    font-weight: 500;
}

.login-lang-switcher .lang-btn:hover {
    background: white;
    border-color: #0d6efd;
    transform: translateY(-2px);
}

.login-lang-switcher .lang-btn.active {
    background: #0d6efd;
    color: white;
    border-color: #0d6efd;
}
</style>

<script>
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function changeLoginLanguage(lang) {
    fetch('/i18n/setlang/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: new URLSearchParams({
            language: lang,
            next: window.location.pathname
        })
    }).then(() => {
        window.location.reload();
    });
}
</script>
```

---

## 🟢 المرحلة 2: ترجمة ملفات .po (يوم 2 - 8 ساعات)

### 2.1 إكمال locale/ar/LC_MESSAGES/django.po (4 ساعات)

**الخطوات:**
1. فتح ملف `locale/ar/LC_MESSAGES/django.po`
2. ترجمة جميع النصوص الفارغة (453 نص)
3. استخدام أداة مساعدة (Poedit أو VS Code extension)

**مثال:**
```po
# قبل
msgid "Personal info"
msgstr ""

# بعد
msgid "Personal info"
msgstr "المعلومات الشخصية"
```

---

### 2.2 إكمال locale/en/LC_MESSAGES/django.po (2 ساعات)

**ملاحظة:** معظم النصوص بالإنجليزية أصلاً، لكن يجب التأكد من:
- ترجمة النصوص العربية إلى إنجليزي
- توحيد المصطلحات

---

### 2.3 تجميع الترجمات (Compile) (30 دقيقة)

```bash
# تجميع ملفات .po إلى .mo
python manage.py compilemessages

# التحقق من عدم وجود أخطاء
python manage.py compilemessages --check
```

---

### 2.4 اختبار الترجمات (1.5 ساعة)

- تبديل اللغة والتحقق من ظهور الترجمات
- فحص Admin Panel
- فحص رسائل الأخطاء

---

## 🟡 المرحلة 3: ترجمة Templates (يوم 3 - 8 ساعات)

### 3.1 تحديث جميع Templates لاستخدام {% trans %} (6 ساعات)

**قائمة الملفات (حسب الأولوية):**

1. **login.html** (1 ساعة)
2. **dashboard.html** (1 ساعة)
3. **customers_enhanced.html** (1 ساعة)
4. **inventory_enhanced.html** (1 ساعة)
5. **sales.html** (1 ساعة)
6. **باقي الملفات** (1 ساعة)

**النمط المتبع:**
```django
{% load i18n %}

<!-- قبل -->
<h2>إدارة العملاء</h2>
<button>إضافة عميل</button>

<!-- بعد -->
<h2>{% trans "إدارة العملاء" %}</h2>
<button>{% trans "إضافة عميل" %}</button>
```

---

### 3.2 إضافة data-translate للعناصر الديناميكية (2 ساعة)

```html
<span data-translate="total_sales">{% trans "إجمالي المبيعات" %}</span>
```

---

## 🟠 المرحلة 4: ترجمة JavaScript (يوم 4 - 8 ساعات)

### 4.1 إنشاء ملفات الترجمة الكاملة (3 ساعات)

**تشغيل أداة الاستخراج:**
```bash
python scripts/extract_translations.py
```

**إضافة الترجمات يدوياً إلى:**
- `static/js/translations/ar.json` (200+ نص)
- `static/js/translations/en.json` (200+ نص)

---

### 4.2 تحديث جميع ملفات JavaScript (4 ساعات)

**الملفات المطلوب تحديثها:**
1. `templates/pages/customers_enhanced.html` (JavaScript مضمن)
2. `templates/pages/customer_details.html`
3. `templates/pages/inventory_enhanced.html`
4. `templates/pages/sales.html`
5. `templates/pages/location_transfer.html`
6. جميع الملفات الأخرى

**النمط:**
```javascript
// قبل
alert('جاري التحميل...');
confirm('هل أنت متأكد من الحذف؟');

// بعد
alert(t('loading'));
confirm(t('confirm_delete'));
```

---

### 4.3 اختبار JavaScript (1 ساعة)

- تبديل اللغة والتحقق من الرسائل
- اختبار جميع التنبيهات والنوافذ المنبثقة

---

## 🔴 المرحلة 5: الاختبار والتوثيق (يوم 5 - 8 ساعات)

### 5.1 اختبار شامل (4 ساعات)

**قائمة الاختبار:**
- [ ] تسجيل الدخول بالعربية
- [ ] تسجيل الدخول بالإنجليزية
- [ ] تبديل اللغة من الواجهة
- [ ] جميع الصفحات بالعربية
- [ ] جميع الصفحات بالإنجليزية
- [ ] RTL/LTR يعمل بشكل صحيح
- [ ] جميع رسائل JavaScript مترجمة
- [ ] جميع النماذج مترجمة
- [ ] جميع الأزرار مترجمة
- [ ] Admin Panel مترجم

---

### 5.2 إنشاء دليل الترجمة (2 ساعة)

**ملف:** `TRANSLATION_GUIDE.md`

محتويات:
- كيفية إضافة ترجمات جديدة
- كيفية تحديث ملفات .po
- كيفية استخدام نظام ترجمة JavaScript
- أفضل الممارسات

---

### 5.3 إصلاح الأخطاء (2 ساعة)

- إصلاح أي مشاكل تم اكتشافها
- تحسين الترجمات
- التأكد من التناسق

---

## 📦 المخرجات النهائية

### ملفات جديدة:
```
static/js/translations/
├── translator.js
├── ar.json
└── en.json

scripts/
└── extract_translations.py

docs/
└── TRANSLATION_GUIDE.md
```

### ملفات محدثة:
```
locale/ar/LC_MESSAGES/django.po  (453 ترجمة جديدة)
locale/en/LC_MESSAGES/django.po  (453 ترجمة جديدة)
templates/pages/*.html           (30+ ملف)
templates/base/base.html
```

---

## 🎯 معايير النجاح

- ✅ 100% من النصوص مترجمة
- ✅ مبدل اللغة يعمل في جميع الصفحات
- ✅ RTL/LTR يعمل بشكل صحيح
- ✅ لا توجد نصوص ثابتة غير قابلة للترجمة
- ✅ جميع رسائل JavaScript مترجمة
- ✅ اختبارات شاملة تمت بنجاح

---

**الملف التالي:** دليل التنفيذ خطوة بخطوة (TRANSLATION_IMPLEMENTATION_GUIDE.md)

