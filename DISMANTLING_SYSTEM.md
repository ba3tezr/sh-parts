# 🔧 نظام تفكيك السيارات - Vehicle Dismantling System

## التاريخ: 9 أكتوبر 2025

---

## 📋 نظرة عامة

نظام متكامل لتفكيك السيارات مع:
- ✅ اختيار تلقائي للماركات والموديلات من API مجاني
- ✅ قائمة القطع القياسية (100+ قطعة)
- ✅ Checklist لتفكيك السيارة
- ✅ تدريج تلقائي للقطع في المخزون
- ✅ ربط القطع بالماركة والموديل والسنة

---

## 🌐 API Integration

### NHTSA VPIC API (مجاني 100%)

**المصدر**: https://vpic.nhtsa.dot.gov/api/

#### Endpoints المستخدمة:

1. **Get All Makes**
```
GET /api/cars-data/makes/
→ Returns: جميع ماركات السيارات
```

2. **Get Models for Make**
```
GET /api/cars-data/models/{make_name}/
→ Returns: جميع موديلات الماركة
```

3. **Get Years**
```
GET /api/cars-data/years/{make}/{model}/
→ Returns: السنوات المتاحة (1990-2026)
```

4. **Decode VIN**
```
GET /api/cars-data/decode-vin/{vin}/
→ Returns: معلومات السيارة من VIN
```

5. **Get Standard Parts**
```
GET /api/cars-data/standard-parts/
→ Returns: جميع القطع القياسية (100+)
```

6. **Get Part Categories**
```
GET /api/cars-data/part-categories/
→ Returns: فئات القطع (المحرك، الهيكل، إلخ)
```

---

## 🔩 القطع القياسية (Standard Parts)

### الفئات الرئيسية:

#### 1. المحرك (Engine) - 14 قطعة
- محرك كامل
- بلوك المحرك
- رأس المحرك
- سلسلة التوقيت
- سير التوقيت
- طرمبة الزيت
- طرمبة الماء
- دينامو
- سلف
- طرمبة البنزين
- ردياتير
- مروحة الردياتير
- كمبروسر المكيف
- تيربو

#### 2. ناقل الحركة (Transmission) - 5 قطع
- قير كامل
- دبرياج كامل
- فولان
- عامود الدوران
- عامود نصف

#### 3. نظام التعليق (Suspension) - 8 قطع
- مساعد أمامي/خلفي
- سوست أمامي/خلفي
- مقص
- بلية
- طرف عايق
- عامود تثبيت

#### 4. الفرامل (Brakes) - 6 قطع
- كاليبر فرامل أمامي/خلفي
- ديسك فرامل أمامي/خلفي
- اسطوانة فرامل رئيسية
- طرمبة ABS

#### 5. الإطارات والجنوط (Wheels) - 4 قطع
- جنط ألمنيوم
- جنط حديد
- إطار
- إطار احتياطي

#### 6. الهيكل (Body) - 14 قطعة
- صدام أمامي/خلفي
- كبوت
- أبواب (4)
- شنطة/باب خلفي
- رفرف أمامي يمين/يسار
- ربع سيارة
- عتبة
- سقف

#### 7. الزجاج (Glass) - 7 قطع
- زجاج أمامي/خلفي
- زجاج باب
- زجاج صغير
- مرآة يمين/يسار
- فتحة سقف

#### 8. الإضاءة (Lighting) - 6 قطع
- فانوس أمامي يمين/يسار
- فانوس خلفي يمين/يسار
- كشاف ضباب
- إشارة انعطاف

#### 9. الداخلية (Interior) - 12 قطعة
- تابلوه
- عجلة القيادة
- كراسي (3)
- حزام أمان
- تابلوه باب
- موكيت
- صندوق التابلوه
- كونسول
- حاجب شمس
- ذراع الجير

#### 10. الإلكترونيات (Electronics) - 10 قطع
- كمبيوتر المحرك
- كمبيوتر ABS
- كمبيوتر الوسائد
- عداد
- راديو
- شاشة ملاحة
- كنترول مكيف
- مفتاح الزجاج
- كنترول الأقفال
- موتور المساحات

#### 11. الكهرباء (Electrical) - 3 قطع
- بطارية
- علبة الفيوزات
- أسلاك كهربائية

#### 12. متفرقات (Misc) - 5 قطع
- شكمان حفاز
- منفولد
- كاتم صوت
- تنك البنزين
- جاك وعدة

**الإجمالي**: 100+ قطعة قياسية

---

## 📝 عملية التفكيك (Dismantling Process)

### الخطوات:

#### 1. اختيار السيارة
```javascript
// اختيار الماركة (تلقائي من API)
GET /api/cars-data/makes/
→ عرض: Toyota, Honda, Nissan, Ford, ...

// اختيار الموديل (حسب الماركة)
GET /api/cars-data/models/Toyota/
→ عرض: Camry, Corolla, RAV4, Prius, ...

// اختيار السنة
GET /api/cars-data/years/Toyota/Camry/
→ عرض: 1990, 1991, ..., 2025, 2026
```

#### 2. إدخال معلومات السيارة
- VIN (اختياري - يملأ البيانات تلقائياً)
- اللون
- الممعداد (Mileage)
- الحالة
- سعر الشراء

#### 3. عرض Checklist القطع
```
☐ محرك كامل
☐ قير كامل
☐ صدام أمامي
☐ كبوت
☐ باب أمامي يمين
☐ باب أمامي يسار
...
```

#### 4. التفكيك
- المستخدم يحدد القطع المتوفرة
- كل قطعة يتم check لها
- يحدد الحالة والسعر لكل قطعة

#### 5. التدريج في المخزون
```javascript
// لكل قطعة محددة، يتم إنشاء:
InventoryItem.create({
    part: selected_part,
    vehicle_source: vehicle,
    condition: 'USED_GOOD',  // حسب الاختيار
    quantity: 1,
    selling_price: user_input,
    location: warehouse_location,
    status: 'AVAILABLE'
})

// مع حركة مخزون
StockMovement.create({
    type: 'IN',
    reason: 'تفكيك سيارة'
})
```

---

## 🎯 مثال عملي

### السيناريو: تفكيك تويوتا كامري 2018

#### الخطوة 1: اختيار السيارة
```
الماركة: Toyota
الموديل: Camry
السنة: 2018
VIN: 4T1BF1FK5JU123456 (اختياري)
```

#### الخطوة 2: معلومات إضافية
```
اللون: أبيض
المسافة المقطوعة: 125,000 كم
الحالة: جيدة
سعر الشراء: 45,000 EGP
```

#### الخطوة 3: Checklist التفكيك
```
☑ محرك كامل - حالة: ممتازة - السعر: 12,500 EGP
☑ قير كامل - حالة: جيدة - السعر: 8,000 EGP
☑ صدام أمامي - حالة: مقبولة - السعر: 1,200 EGP
☑ كبوت - حالة: جيدة - السعر: 2,500 EGP
☑ باب أمامي يمين - حالة: ممتازة - السعر: 3,500 EGP
☐ باب أمامي يسار - تالف
☑ فانوس أمامي يمين - حالة: ممتازة - السعر: 850 EGP
☑ فانوس أمامي يسار - حالة: ممتازة - السعر: 850 EGP
...
```

#### الخطوة 4: التدريج
```
تم إضافة 15 قطعة إلى المخزون:
- SKU-001: محرك كامل - تويوتا كامري 2018
- SKU-002: قير كامل - تويوتا كامري 2018
- SKU-003: صدام أمامي - تويوتا كامري 2018
...

إجمالي قيمة القطع: 42,750 EGP
سعر الشراء: 45,000 EGP
الفرق: -2,250 EGP
```

---

## 💻 استخدام في الكود

### JavaScript Example

```javascript
// 1. تحميل الماركات
const makes = await app.apiRequest('/api/cars-data/makes/');
makes.results.forEach(make => {
    console.log(make.name); // Toyota, Honda, ...
});

// 2. تحميل الموديلات
const models = await app.apiRequest('/api/cars-data/models/Toyota/');
models.results.forEach(model => {
    console.log(model.name); // Camry, Corolla, ...
});

// 3. تحميل القطع القياسية
const parts = await app.apiRequest('/api/cars-data/standard-parts/');
parts.results.forEach(part => {
    console.log(part.name_ar, part.name_en);
});

// 4. فك تشفير VIN
const vinInfo = await app.apiRequest('/api/cars-data/decode-vin/4T1BF1FK5JU123456/');
console.log(vinInfo.make, vinInfo.model, vinInfo.year);
```

---

## 📊 قاعدة البيانات

### الجداول المرتبطة:

```sql
-- السيارات المستلمة
Vehicle {
    vin VARCHAR(17) UNIQUE
    make_id FK
    model_id FK
    year INT
    color VARCHAR
    mileage INT
    condition VARCHAR
    purchase_price DECIMAL
    received_by FK(User)
    is_dismantled BOOLEAN
}

-- المخزون
InventoryItem {
    sku VARCHAR UNIQUE
    part_id FK
    vehicle_source_id FK(Vehicle)
    condition VARCHAR
    quantity INT
    selling_price DECIMAL
    location_id FK
    status VARCHAR
}

-- حركات المخزون
StockMovement {
    inventory_item_id FK
    movement_type VARCHAR
    quantity INT
    reference_number VARCHAR
    performed_by FK(User)
}
```

---

## 🚀 الميزات المستقبلية

1. **Auto-Pricing**
   - اقتراح أسعار تلقائية بناءً على:
     - الماركة والموديل والسنة
     - الحالة
     - أسعار السوق (ML Model)

2. **Photos Upload**
   - رفع صور لكل قطعة أثناء التفكيك
   - QR Code لكل قطعة يربط بالصور

3. **Dismantling Video**
   - تسجيل فيديو عملية التفكيك
   - Timestamps للقطع المهمة

4. **Parts Condition AI**
   - استخدام AI لتقييم حالة القطعة من الصورة
   - اقتراح السعر تلقائياً

5. **Inventory Forecasting**
   - تنبؤ بالقطع الأكثر مبيعاً
   - اقتراحات لشراء سيارات معينة

---

## 📝 ملاحظات للمطورين

### Cache Strategy:
```python
# الماركات - 30 يوم
cache.set('car_makes_all', makes, 60 * 60 * 24 * 30)

# الموديلات - 30 يوم
cache.set(f'car_models_{make_name}', models, 60 * 60 * 24 * 30)

# VIN - 365 يوم (لا يتغير)
cache.set(f'vin_{vin}', info, 60 * 60 * 24 * 365)
```

### Error Handling:
```python
try:
    response = requests.get(url, timeout=10)
except requests.exceptions.Timeout:
    # استخدام بيانات محلية
    return local_fallback_data()
except requests.exceptions.ConnectionError:
    # API غير متاح
    return cached_data_or_empty()
```

---

**الحالة**: ✅ API جاهز ومتكامل  
**التاليات**: صفحة تفكيك السيارة Frontend
