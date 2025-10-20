# 🌍 دليل الترجمة - SH Parts System

## 📖 نظرة عامة

نظام SH Parts يدعم **العربية والإنجليزية** بشكل كامل باستخدام:
- **Django i18n** للترجمة في Templates و Models
- **JavaScript Translation System** للترجمة في الكود الديناميكي

---

## 🚀 البدء السريع

### للمستخدم:
1. افتح صفحة تسجيل الدخول
2. اختر اللغة من الأزرار في الأعلى (العربية/English)
3. سجل الدخول - جميع الصفحات ستظهر باللغة المختارة

### للمطور:
```bash
# تحديث الترجمات بعد إضافة نصوص جديدة
python manage.py makemessages -l ar -l en
python manage.py compilemessages

# اختبار الترجمات
python scripts/test_translations.py
```

---

## 📝 كيفية إضافة نصوص جديدة

### 1. في Django Templates

```django
{% load i18n %}

<!-- نص بسيط -->
<h1>{% trans "لوحة التحكم" %}</h1>

<!-- نص مع متغيرات -->
{% blocktrans with name=user.name %}
    مرحباً {{ name }}
{% endblocktrans %}

<!-- في الأزرار -->
<button>{% trans "حفظ" %}</button>
```

### 2. في JavaScript

```javascript
// استخدام دالة t() للترجمة
alert(t('success_message'));
confirm(t('are_you_sure'));

// مع متغيرات
alert(t('welcome_user', {name: 'أحمد'}));
```

**ملاحظة:** يجب إضافة المفتاح في ملفات JSON أولاً:

`static/js/translations/ar.json`:
```json
{
  "success_message": "تم الحفظ بنجاح",
  "are_you_sure": "هل أنت متأكد؟"
}
```

`static/js/translations/en.json`:
```json
{
  "success_message": "Saved successfully",
  "are_you_sure": "Are you sure?"
}
```

### 3. في Models

```python
from django.utils.translation import gettext_lazy as _

class MyModel(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("الاسم")
    )
```

---

## 🔧 الأدوات المساعدة

### 1. سكريبت ترجمة ملفات .po
```bash
python scripts/translate_po_files.py
```
يقوم بترجمة النصوص الشائعة تلقائياً في ملفات .po

### 2. سكريبت تحديث JavaScript
```bash
python scripts/update_js_translations.py
```
يحول `alert()` و `confirm()` من نصوص ثابتة إلى `t()`

### 3. سكريبت الاختبار
```bash
python scripts/test_translations.py
```
يختبر اكتمال الترجمات في جميع الملفات

---

## 📂 هيكل الملفات

```
sh-parts/
├── locale/
│   ├── ar/
│   │   └── LC_MESSAGES/
│   │       ├── django.po    # ترجمات عربية
│   │       └── django.mo    # مجمع
│   └── en/
│       └── LC_MESSAGES/
│           ├── django.po    # ترجمات إنجليزية
│           └── django.mo    # مجمع
│
├── static/js/translations/
│   ├── translator.js        # محرك الترجمة
│   ├── ar.json             # 243 مفتاح عربي
│   └── en.json             # 243 مفتاح إنجليزي
│
├── templates/
│   ├── base/
│   │   └── base.html       # مبدل اللغة الرئيسي
│   └── pages/
│       ├── login.html      # صفحة تسجيل الدخول
│       └── ...             # باقي الصفحات
│
└── scripts/
    ├── translate_po_files.py
    ├── update_js_translations.py
    └── test_translations.py
```

---

## 🎨 مبدل اللغة

### في base.html (للصفحات الداخلية):
```html
<div class="lang-switcher">
    <button class="lang-btn {% if LANGUAGE_CODE|default:'ar'|slice:":2" == 'ar' %}active{% endif %}" 
            data-lang="ar">ع</button>
    <button class="lang-btn {% if LANGUAGE_CODE|default:'ar'|slice:":2" == 'en' %}active{% endif %}" 
            data-lang="en">EN</button>
</div>
```

### في login.html (صفحة تسجيل الدخول):
```html
<div class="lang-switcher-login">
    <button class="lang-btn {% if LANGUAGE_CODE|default:'ar'|slice:":2" == 'ar' %}active{% endif %}" 
            data-lang="ar">العربية</button>
    <button class="lang-btn {% if LANGUAGE_CODE|default:'ar'|slice:":2" == 'en' %}active{% endif %}" 
            data-lang="en">English</button>
</div>
```

### JavaScript للتبديل:
```javascript
document.querySelectorAll('.lang-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
        var lang = btn.getAttribute('data-lang');
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
        }).then(function(){ 
            window.location.reload(); 
        });
    });
});
```

---

## 🔄 سير العمل

### إضافة ميزة جديدة:

1. **كتابة الكود:**
```django
<!-- في template -->
<h1>{% trans "ميزة جديدة" %}</h1>
```

2. **استخراج النصوص:**
```bash
python manage.py makemessages -l ar -l en
```

3. **ترجمة النصوص:**
افتح `locale/ar/LC_MESSAGES/django.po` و `locale/en/LC_MESSAGES/django.po`
```po
msgid "ميزة جديدة"
msgstr "New Feature"
```

4. **تجميع الترجمات:**
```bash
python manage.py compilemessages
```

5. **اختبار:**
```bash
python scripts/test_translations.py
python manage.py runserver
```

---

## 📊 الإحصائيات الحالية

| المكون | العربية | الإنجليزية |
|--------|---------|------------|
| ملفات .po | 110 نص | 363 نص |
| ملفات JSON | 243 مفتاح | 243 مفتاح |
| Templates | 20/27 صفحة | 20/27 صفحة |
| Coverage | 74.1% | 74.1% |

---

## ⚙️ الإعدادات

### في settings.py:
```python
# اللغة الافتراضية
LANGUAGE_CODE = 'ar'

# اللغات المدعومة
LANGUAGES = [
    ('ar', 'العربية'),
    ('en', 'English'),
]

# مسار ملفات الترجمة
LOCALE_PATHS = [BASE_DIR / 'locale']

# تفعيل الترجمة
USE_I18N = True
USE_L10N = True
```

### في urls.py:
```python
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # ... باقي المسارات
]
```

---

## 🐛 حل المشاكل

### المشكلة: النصوص لا تترجم
**الحل:**
1. تأكد من وجود `{% load i18n %}` في أعلى Template
2. تأكد من تجميع الترجمات: `python manage.py compilemessages`
3. أعد تشغيل السيرفر

### المشكلة: JavaScript لا يترجم
**الحل:**
1. تأكد من تحميل `translator.js` في الصفحة
2. تأكد من وجود المفتاح في `ar.json` و `en.json`
3. افحص Console للأخطاء

### المشكلة: RTL/LTR لا يعمل
**الحل:**
1. تأكد من وجود `dir="..."` في `<html>`
2. تأكد من تحميل Bootstrap RTL للعربية
3. افحص CSS

---

## 📚 مراجع

- [Django i18n Documentation](https://docs.djangoproject.com/en/stable/topics/i18n/)
- [gettext Documentation](https://www.gnu.org/software/gettext/manual/)
- [Bootstrap RTL](https://getbootstrap.com/docs/5.3/getting-started/rtl/)

---

## ✅ قائمة التحقق

عند إضافة صفحة جديدة:

- [ ] إضافة `{% load i18n %}` في أعلى الصفحة
- [ ] استخدام `{% trans %}` لجميع النصوص
- [ ] إضافة مبدل اللغة (إذا لزم الأمر)
- [ ] دعم RTL/LTR
- [ ] استخدام `t()` في JavaScript
- [ ] إضافة المفاتيح في JSON
- [ ] تشغيل `makemessages`
- [ ] ترجمة النصوص في .po
- [ ] تشغيل `compilemessages`
- [ ] اختبار في كلا اللغتين

---

**تم إعداده بواسطة:** فريق تطوير SH Parts  
**آخر تحديث:** 2025-10-20

