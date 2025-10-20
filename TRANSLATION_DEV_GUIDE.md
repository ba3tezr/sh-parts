# 🌍 دليل المطورين للترجمة - Translation Developer Guide

## 🚀 البدء السريع / Quick Start

### إضافة نص جديد للترجمة / Adding New Translatable Text

#### 1. في القوالب (Templates):

```django
{% load i18n %}

<!-- نص بسيط / Simple text -->
<h1>{% trans "عنوان الصفحة" %}</h1>
<p>{% trans "هذا نص تجريبي" %}</p>

<!-- نص مع متغيرات / Text with variables -->
{% blocktrans with name=user.name %}
مرحباً {{ name }}، أهلاً بك!
{% endblocktrans %}

<!-- في الخصائص / In attributes -->
<input type="text" placeholder="{% trans 'أدخل الاسم...' %}">
<button title="{% trans 'حفظ التغييرات' %}">{% trans "حفظ" %}</button>
```

#### 2. في Python (Views/Models):

```python
from django.utils.translation import gettext_lazy as _

# في Models
class MyModel(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("الاسم"),
        help_text=_("أدخل الاسم الكامل")
    )

# في Views
from django.contrib import messages
messages.success(request, _("تم الحفظ بنجاح"))

# في Forms
class MyForm(forms.Form):
    name = forms.CharField(
        label=_("الاسم"),
        help_text=_("أدخل اسمك الكامل")
    )
```

#### 3. في JavaScript:

```javascript
// تحميل نظام الترجمة
// (تأكد من تضمين translator.js في base.html)

// استخدام الترجمة
alert(t('success_message'));
confirm(t('confirm_delete'));

// مع متغيرات
const msg = t('hello_user', { name: userName });
```

---

## 🔄 سير العمل الكامل / Complete Workflow

### الخطوة 1: إضافة النصوص
```django
{% trans "النص الجديد" %}
```

### الخطوة 2: استخراج الترجمات
```bash
cd /home/zakee/SH/sh-parts
source .venv/bin/activate
python manage.py makemessages -l ar -l en --ignore=venv --ignore=staticfiles
```

### الخطوة 3: الترجمة
افتح الملفات وترجم:
- `locale/ar/LC_MESSAGES/django.po` - للنصوص الإنجليزية
- `locale/en/LC_MESSAGES/django.po` - للنصوص العربية

```po
# مثال في en/django.po
msgid "النص الجديد"
msgstr "New Text"
```

### الخطوة 4: التجميع
```bash
python manage.py compilemessages
```

### الخطوة 5: إعادة التشغيل
```bash
# أعد تشغيل الخادم لتحميل الترجمات
python manage.py runserver
```

---

## 🛠️ السكريبتات المساعدة / Helper Scripts

### 1. اكتشاف النصوص غير المترجمة

```bash
python3 scripts/find_untranslated_strings.py
```

**النتيجة:** قائمة بجميع النصوص غير المحاطة بـ `{% trans %}`

### 2. إصلاح الترجمات المتطابقة

```bash
python3 scripts/fix_identical_translations.py
```

**النتيجة:** إصلاح النصوص التي msgid = msgstr تلقائياً

### 3. إكمال الترجمات الأساسية

```bash
python3 scripts/complete_remaining_translations.py
```

**النتيجة:** ترجمة النصوص الأساسية من قاموس مدمج

### 4. إضافة {% load i18n %}

```bash
python3 scripts/add_i18n_to_all_templates.py
```

**النتيجة:** إضافة السطر للملفات التي تحتاجه

---

## 📝 أمثلة عملية / Practical Examples

### مثال 1: صفحة بسيطة

```django
{% extends 'base/base.html' %}
{% load static i18n %}

{% block title %}{% trans "الصفحة الرئيسية" %}{% endblock %}

{% block content %}
<div class="container">
    <h1>{% trans "مرحباً بك" %}</h1>
    
    <div class="card">
        <h2>{% trans "الإحصائيات" %}</h2>
        
        <div class="stats">
            <div class="stat">
                <span>{% trans "إجمالي المبيعات" %}</span>
                <strong>{{ total_sales }}</strong>
            </div>
        </div>
    </div>
    
    <button onclick="saveData()">
        {% trans "حفظ" %}
    </button>
</div>

<script>
function saveData() {
    if (confirm(t('confirm_save'))) {
        // حفظ البيانات
        alert(t('success_saved'));
    }
}
</script>
{% endblock %}
```

### مثال 2: Form مع ترجمة

```python
from django import forms
from django.utils.translation import gettext_lazy as _

class CustomerForm(forms.Form):
    name = forms.CharField(
        label=_("اسم العميل"),
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': _('أدخل الاسم الكامل'),
            'class': 'form-control'
        })
    )
    
    phone = forms.CharField(
        label=_("رقم الهاتف"),
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': _('مثال: 0123456789'),
            'class': 'form-control'
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError(
                _("رقم الهاتف يجب أن يحتوي على أرقام فقط")
            )
        return phone
```

---

## 🔍 استكشاف الأخطاء / Troubleshooting

### المشكلة: الترجمة لا تظهر

**الأسباب المحتملة:**

1. **لم يتم تجميع الترجمات:**
   ```bash
   python manage.py compilemessages
   ```

2. **الخادم لم يُعاد تشغيله:**
   ```bash
   # أوقف الخادم (Ctrl+C) ثم
   python manage.py runserver
   ```

3. **ذاكرة المتصفح (Cache):**
   - اضغط Ctrl+Shift+R (Windows/Linux)
   - اضغط Cmd+Shift+R (Mac)

4. **النص ليس في ملف .po:**
   ```bash
   # أعد استخراج الترجمات
   python manage.py makemessages -l ar -l en
   ```

### المشكلة: النص يظهر بالإنجليزي في الصفحة العربية

**السبب:** الترجمة فارغة في `locale/ar/LC_MESSAGES/django.po`

**الحل:**
1. افتح `locale/ar/LC_MESSAGES/django.po`
2. ابحث عن النص الإنجليزي
3. أضف الترجمة العربية
4. شغّل `python manage.py compilemessages`

### المشكلة: RTL/LTR لا يعمل

**الحل:** تأكد من وجود هذا الكود في `base.html`:

```html
<html lang="{{ LANGUAGE_CODE|default:'ar' }}" 
      dir="{% if LANGUAGE_CODE|default:'ar'|slice:":2" == 'ar' %}rtl{% else %}ltr{% endif %}">
```

---

## 📚 قواعد مهمة / Important Rules

### ✅ افعل (DO):

1. **استخدم {% trans %} دائماً:**
   ```django
   ✅ <h1>{% trans "العنوان" %}</h1>
   ❌ <h1>العنوان</h1>
   ```

2. **استخدم gettext_lazy في Python:**
   ```python
   ✅ from django.utils.translation import gettext_lazy as _
   ✅ verbose_name=_("الاسم")
   ❌ verbose_name="الاسم"
   ```

3. **جمّع الترجمات بعد كل تغيير:**
   ```bash
   python manage.py compilemessages
   ```

### ❌ لا تفعل (DON'T):

1. **لا تضع HTML داخل {% trans %}:**
   ```django
   ❌ {% trans "<strong>العنوان</strong>" %}
   ✅ <strong>{% trans "العنوان" %}</strong>
   ```

2. **لا تترجم الأسماء الخاصة:**
   ```django
   ❌ {% trans "admin" %}  # Username
   ❌ {% trans "admin@example.com" %}  # Email
   ✅ admin  # اتركها كما هي
   ```

3. **لا تنسَ إعادة التشغيل:**
   ```bash
   # بعد compilemessages، أعد تشغيل الخادم
   ```

---

## 🎯 نصائح للأداء / Performance Tips

### 1. استخدم gettext_lazy بدلاً من gettext

```python
# ✅ جيد - يُقيّم عند الحاجة
from django.utils.translation import gettext_lazy as _
verbose_name = _("الاسم")

# ❌ سيء - يُقيّم فوراً
from django.utils.translation import gettext as _
verbose_name = _("الاسم")
```

### 2. cache الترجمات في JavaScript

```javascript
// تحميل مرة واحدة
const translations = {
    'save': t('save'),
    'delete': t('delete'),
    'cancel': t('cancel')
};

// استخدام من الذاكرة
button.textContent = translations.save;
```

### 3. تجنب الترجمة المتكررة

```django
<!-- ❌ سيء -->
{% for item in items %}
    <span>{% trans "السعر" %}: {{ item.price }}</span>
{% endfor %}

<!-- ✅ جيد -->
{% trans "السعر" as price_label %}
{% for item in items %}
    <span>{{ price_label }}: {{ item.price }}</span>
{% endfor %}
```

---

## 📦 الملفات المهمة / Important Files

```
sh-parts/
├── locale/
│   ├── ar/
│   │   └── LC_MESSAGES/
│   │       ├── django.po     # ملف الترجمة العربية (تحرير يدوي)
│   │       └── django.mo     # ملف مجمّع (تلقائي)
│   └── en/
│       └── LC_MESSAGES/
│           ├── django.po     # ملف الترجمة الإنجليزية
│           └── django.mo     # ملف مجمّع
├── static/
│   └── js/
│       └── translations/
│           ├── translator.js  # نظام الترجمة JS
│           ├── ar.json       # ترجمات JavaScript العربية
│           └── en.json       # ترجمات JavaScript الإنجليزية
├── templates/
│   └── base/
│       └── base.html         # القالب الأساسي
└── scripts/
    ├── find_untranslated_strings.py
    ├── fix_identical_translations.py
    └── complete_remaining_translations.py
```

---

## 🔗 روابط مفيدة / Useful Links

### الوثائق:
- [Django i18n Documentation](https://docs.djangoproject.com/en/stable/topics/i18n/)
- [Translation Best Practices](https://docs.djangoproject.com/en/stable/topics/i18n/translation/)

### التقارير:
- `TRANSLATION_COMPLETION_REPORT.md` - التقرير الكامل
- `TRANSLATION_SUMMARY_AR.md` - الملخص بالعربية
- `TRANSLATION_STATUS_FINAL.md` - الحالة السابقة

---

**آخر تحديث:** 20 أكتوبر 2025  
**الإصدار:** 1.0  
**المُعد:** Droid AI
