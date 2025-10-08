# إعداد النظام للسوق المصري
## دليل التخصيص والعملات المتعددة

---

## ✨ المميزات الجديدة

### 1. دعم العملات المتعددة
النظام الآن يدعم 5 عملات رئيسية:
- 🇪🇬 **الجنيه المصري (EGP)** - الافتراضي
- 🇸🇦 الريال السعودي (SAR)
- 🇦🇪 الدرهم الإماراتي (AED)
- 🇺🇸 الدولار الأمريكي (USD)
- 🇪🇺 اليورو (EUR)

### 2. إعدادات مرنة للضرائب
- إمكانية تفعيل/تعطيل الضرائب
- تحديد نسبة الضريبة (مثل: 14% في مصر، 15% في السعودية)
- إضافة الرقم الضريبي للشركة

### 3. تخصيص معلومات الشركة
- اسم الشركة (عربي وإنجليزي)
- معلومات الاتصال (هاتف، بريد، عنوان)
- المدينة والدولة

### 4. إعدادات إقليمية
- اختيار المنطقة الزمنية
- اختيار اللغة الافتراضية
- تنسيق التواريخ والأرقام حسب المنطقة

---

## 🚀 البدء السريع

### الخطوة 1: تطبيق التهجيرات
```bash
cd "/home/zakee/shalah projevt"
source venv/bin/activate
python manage.py migrate
```

### الخطوة 2: تهيئة الإعدادات للسوق المصري
```bash
python manage.py init_settings
```

سيتم تلقائياً:
- ✅ تعيين العملة: الجنيه المصري (EGP)
- ✅ تعيين الضريبة: 14%
- ✅ تعيين المنطقة الزمنية: Africa/Cairo
- ✅ تعيين الدولة: مصر

### الخطوة 3: تشغيل النظام
```bash
python manage.py runserver
```

---

## ⚙️ إدارة الإعدادات

### من لوحة الإدارة (الطريقة الموصى بها)

1. **الدخول للوحة الإدارة**
   ```
   http://localhost:8000/admin/
   ```

2. **الذهاب إلى "إعدادات النظام"**
   - ستجد قسم "Core" → "إعدادات النظام"
   - اضغط على الإعدادات الموجودة (لا يمكن إنشاء أكثر من إعداد واحد)

3. **تغيير العملة**
   - في قسم "إعدادات العملة والمنطقة"
   - اختر العملة المطلوبة من القائمة المنسدلة
   - احفظ التغييرات

4. **تحديث معلومات الشركة**
   - اسم الشركة بالعربية والإنجليزية
   - معلومات الاتصال
   - العنوان والمدينة

5. **إعدادات الضرائب**
   - تفعيل/تعطيل الضريبة
   - نسبة الضريبة (%)
   - الرقم الضريبي

### برمجياً (للمطورين)

```python
from core.models import SystemSettings

# الحصول على الإعدادات
settings = SystemSettings.get_settings()

# تغيير العملة
settings.currency = 'SAR'  # أو 'EGP', 'AED', 'USD', 'EUR'
settings.save()

# تغيير نسبة الضريبة
settings.tax_rate = 15.00  # 15%
settings.save()

# الحصول على رمز العملة
print(settings.currency_symbol)  # مثال: ج.م

# الحصول على اسم العملة
print(settings.currency_name)  # مثال: الجنيه المصري - Egyptian Pound (EGP)
```

---

## 🔄 كيف يعمل النظام

### تطبيق العملة في الواجهة الأمامية

يتم تحميل إعدادات العملة تلقائياً عند فتح أي صفحة:

```javascript
// في JavaScript
const settings = app.getSettings();
console.log(settings.currency);        // 'EGP'
console.log(settings.currency_symbol); // 'ج.م'

// تنسيق الأرقام
app.formatCurrency(1500.50);  // '1,500.50 ج.م'
```

### تطبيق العملة في القوالب (Templates)

```django
<!-- في HTML/Django -->
{{ system_settings.currency }}         <!-- EGP -->
{{ currency_symbol }}                  <!-- ج.م -->
{{ system_settings.currency_name }}    <!-- الجنيه المصري -->
```

### تطبيق العملة في API

```python
# في Views/Serializers
from core.models import SystemSettings

settings = SystemSettings.get_settings()
currency = settings.currency
currency_symbol = settings.currency_symbol
```

---

## 📊 نماذج الضريبة حسب الدولة

| الدولة | نسبة الضريبة | كود العملة |
|--------|--------------|------------|
| 🇪🇬 مصر | 14% | EGP |
| 🇸🇦 السعودية | 15% | SAR |
| 🇦🇪 الإمارات | 5% | AED |
| 🇯🇴 الأردن | 16% | JOD |
| 🇰🇼 الكويت | 0% | KWD |

---

## 🔧 إضافة عملات جديدة

### الخطوة 1: تحديث الموديل

في `core/models.py`:

```python
CURRENCY_CHOICES = [
    ('EGP', 'الجنيه المصري - Egyptian Pound (EGP)'),
    ('SAR', 'الريال السعودي - Saudi Riyal (SAR)'),
    # أضف عملة جديدة
    ('JOD', 'الدينار الأردني - Jordanian Dinar (JOD)'),
]

CURRENCY_SYMBOLS = {
    'EGP': 'ج.م',
    'SAR': 'ر.س',
    # أضف رمز العملة
    'JOD': 'د.أ',
}
```

### الخطوة 2: إنشاء وتطبيق التهجير

```bash
python manage.py makemigrations
python manage.py migrate
```

### الخطوة 3: تحديث الترجمات

في `static/js/translations/ar.json`:

```json
{
  "currency_jod": "الدينار الأردني"
}
```

---

## 📱 استخدام العملة في الفواتير

عند إنشاء فاتورة، سيتم استخدام العملة المحددة تلقائياً:

```python
# مثال في models.py للمبيعات
from core.models import SystemSettings

class Sale(models.Model):
    # ...
    
    def get_currency_display(self):
        settings = SystemSettings.get_settings()
        return settings.currency_symbol
    
    def get_total_with_tax(self):
        settings = SystemSettings.get_settings()
        if settings.tax_enabled:
            tax_amount = self.subtotal * (settings.tax_rate / 100)
            return self.subtotal + tax_amount
        return self.subtotal
```

---

## 🌍 التخصيص لأسواق أخرى

### للسوق السعودي

```bash
# من لوحة الإدارة:
# 1. العملة: SAR
# 2. الضريبة: 15%
# 3. المنطقة الزمنية: Asia/Riyadh
# 4. الدولة: السعودية
```

### للسوق الإماراتي

```bash
# من لوحة الإدارة:
# 1. العملة: AED
# 2. الضريبة: 5%
# 3. المنطقة الزمنية: Asia/Dubai
# 4. الدولة: الإمارات
```

---

## 🔍 الكاش والأداء

الإعدادات يتم تخزينها في الكاش (Cache) لمدة ساعة لتحسين الأداء:

```python
# مسح الكاش يدوياً
from django.core.cache import cache
cache.delete('system_settings')

# أو من Django shell
python manage.py shell
>>> from core.models import SystemSettings
>>> SystemSettings.get_settings()  # جلب من الكاش
>>> # تحديث الإعدادات يمسح الكاش تلقائياً
```

---

## 🛠️ استكشاف الأخطاء

### العملة لا تظهر صحيحة في الواجهة

1. **تأكد من إعادة تحميل الصفحة** (Ctrl+F5)
2. **افحص console في المتصفح**:
   ```javascript
   app.getSettings()  // يجب أن يعرض العملة الصحيحة
   ```
3. **تأكد من تطبيق التهجيرات**:
   ```bash
   python manage.py migrate
   ```

### الإعدادات لا تحفظ

1. **تأكد من الصلاحيات**:
   - يجب أن تكون مسجل دخول كـ Admin
   - افحص صلاحيات المستخدم

2. **افحص السجلات**:
   ```bash
   python manage.py runserver
   # شاهد رسائل الأخطاء في Terminal
   ```

---

## 📚 API للإعدادات

### الحصول على الإعدادات

```http
GET /api/settings/

Response:
{
    "currency": "EGP",
    "currency_symbol": "ج.م",
    "currency_name": "الجنيه المصري - Egyptian Pound (EGP)",
    "tax_enabled": true,
    "tax_rate": 14.0,
    "default_language": "ar",
    "timezone": "Africa/Cairo",
    "company_name": "SH Parts - قطع غيار السيارات",
    "company_name_en": "SH Parts - Auto Parts"
}
```

---

## ✅ قائمة التحقق

عند إعداد النظام لسوق جديد:

- [ ] تشغيل `python manage.py init_settings`
- [ ] تحديث العملة من لوحة الإدارة
- [ ] تحديث نسبة الضريبة
- [ ] تحديث المنطقة الزمنية
- [ ] تحديث معلومات الشركة
- [ ] تحديث العنوان والمدينة
- [ ] اختبار تنسيق العملة في الواجهة
- [ ] اختبار حسابات الضريبة في الفواتير
- [ ] تحديث الترجمات إذا لزم الأمر

---

## 🆘 الدعم

إذا واجهت أي مشاكل:

1. راجع ملف `DOCUMENTATION_AR.md`
2. راجع ملف `DEPLOYMENT_GUIDE.md`
3. تواصل مع الدعم الفني

---

**آخر تحديث**: 8 يناير 2024
**الإصدار**: 1.1.0 (دعم العملات المتعددة)
