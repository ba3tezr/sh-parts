# التوثيق الشامل لنظام SH Parts - إدارة قطع غيار السيارات
## دليل المستخدم والمطور الكامل

---

## المحتويات
1. [نظرة عامة](#نظرة-عامة)
2. [المتطلبات والتثبيت](#المتطلبات-والتثبيت)
3. [هيكل المشروع](#هيكل-المشروع)
4. [قاعدة البيانات](#قاعدة-البيانات)
5. [واجهة برمجة التطبيقات API](#واجهة-برمجة-التطبيقات-api)
6. [الواجهة الأمامية](#الواجهة-الأمامية)
7. [دليل الاستخدام](#دليل-الاستخدام)
8. [النشر والإنتاج](#النشر-والإنتاج)

---

## نظرة عامة

### الوصف
نظام SH Parts هو نظام متكامل لإدارة أعمال تفكيك السيارات وبيع قطع الغيار، مصمم خصيصاً للسوق السعودي مع دعم كامل للغة العربية والإنجليزية.

### المميزات الرئيسية
- ✅ إدارة استقبال وتفكيك السيارات
- ✅ إدارة مخزون القطع مع QR Codes
- ✅ نظام مبيعات متكامل مع السلة والدفعات
- ✅ إدارة العملاء مع تتبع الائتمان
- ✅ تقارير وتحليلات شاملة
- ✅ دعم اللغتين العربية والإنجليزية مع RTL
- ✅ 3 ثيمات (أزرق داكن، فاتح، تباين عالي)
- ✅ REST API كامل
- ✅ نظام صلاحيات متعدد المستويات

### التقنيات المستخدمة
- **Backend**: Django 5.2.7, Django REST Framework
- **Database**: PostgreSQL / SQLite
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Authentication**: JWT (JSON Web Tokens)
- **Task Queue**: Celery + Redis
- **Deployment**: Docker, Gunicorn, Nginx

---

## المتطلبات والتثبيت

### المتطلبات
- Python 3.13+
- PostgreSQL 15+ (اختياري، SQLite للتطوير)
- Redis (للمهام في الخلفية)
- Git

### التثبيت السريع

#### 1. استنساخ المشروع
```bash
cd /path/to/your/projects
# المشروع موجود بالفعل في: /home/zakee/shalah projevt
```

#### 2. تفعيل البيئة الافتراضية
```bash
cd "/home/zakee/shalah projevt"
source venv/bin/activate
```

#### 3. تثبيت المكتبات (إذا لزم الأمر)
```bash
venv/bin/pip install -r requirements.txt
```

#### 4. إعداد قاعدة البيانات
```bash
# تطبيق التهجيرات (Migrations)
venv/bin/python manage.py migrate

# استيراد بيانات السيارات والقطع
venv/bin/python manage.py import_cars_data

# إنشاء بيانات تجريبية (اختياري)
venv/bin/python manage.py seed_data
```

#### 5. تشغيل الخادم
```bash
venv/bin/python manage.py runserver
```

#### 6. الوصول للنظام
- **الواجهة الرئيسية**: http://localhost:8000/
- **لوحة الإدارة**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/

### بيانات الدخول الافتراضية
```
البريد الإلكتروني: admin@shparts.com
كلمة المرور: admin123
```

---

## هيكل المشروع

```
sh_parts/
├── authentication/          # نظام المصادقة والمستخدمين
│   ├── models.py           # نموذج المستخدم المخصص
│   ├── serializers.py      # محولات API
│   └── views.py            # العروض
├── cars/                   # إدارة السيارات والقطع
│   ├── models.py           # CarMake, CarModel, Part, Vehicle
│   ├── serializers.py
│   ├── views.py
│   └── admin.py
├── inventory/              # إدارة المخزون
│   ├── models.py           # InventoryItem, WarehouseLocation
│   ├── serializers.py
│   └── views.py
├── customers/              # إدارة العملاء
│   ├── models.py           # Customer, CustomerCredit
│   ├── serializers.py
│   └── views.py
├── sales/                  # إدارة المبيعات
│   ├── models.py           # Sale, SaleItem, Payment, Cart
│   ├── serializers.py
│   └── views.py
├── reports/                # التقارير والتحليلات
│   ├── models.py
│   └── views.py
├── core/                   # الأدوات المشتركة
│   ├── views.py            # لوحة التحكم، تسجيل الدخول
│   └── management/
│       └── commands/       # أوامر إدارية مخصصة
├── templates/              # قوالب HTML
│   ├── base/
│   │   └── base.html      # القالب الأساسي
│   └── pages/
│       ├── dashboard.html  # لوحة التحكم
│       └── login.html      # تسجيل الدخول
├── static/                 # الملفات الثابتة
│   ├── css/
│   │   └── style.css      # الأنماط المخصصة
│   ├── js/
│   │   ├── app.js         # JavaScript الرئيسي
│   │   └── translations/  # ملفات الترجمة
│   └── images/
├── media/                  # ملفات المستخدمين
├── sh_parts/               # إعدادات المشروع
│   ├── settings.py        # الإعدادات
│   ├── urls.py            # التوجيهات الرئيسية
│   └── celery.py          # إعدادات Celery
├── requirements.txt        # المكتبات المطلوبة
├── Dockerfile             # ملف Docker
├── docker-compose.yml     # إعداد Docker Compose
└── README.md              # ملف التعريف
```

---

## قاعدة البيانات

### النماذج (Models) الرئيسية

#### 1. المصادقة (Authentication)
```python
User
- email (EmailField, unique)
- first_name, last_name
- phone
- role (ADMIN, MANAGER, SALES, WAREHOUSE)
- two_factor_enabled
```

#### 2. السيارات (Cars)
```python
CarMake               # ماركات السيارات
- name, name_ar
- logo
- is_active

CarModel              # موديلات السيارات
- make (FK)
- name, name_ar
- year_start, year_end
- body_type

PartCategory          # فئات القطع (هرمية)
- name, name_ar
- parent (FK, nullable)
- icon, sort_order

Part                  # القطع
- name, name_ar
- category (FK)
- part_number
- description
- compatible_models (M2M)
- default_image
- is_universal

Vehicle               # السيارات المستقبلة
- vin (unique)
- make, model, year
- color, mileage, condition
- intake_date
- is_dismantled
```

#### 3. المخزون (Inventory)
```python
WarehouseLocation
- warehouse, aisle, shelf, bin
- description

InventoryItem         # قطع المخزون
- sku (auto-generated, unique)
- part (FK)
- vehicle_source (FK, nullable)
- condition (NEW, USED_EXCELLENT, etc.)
- status (AVAILABLE, RESERVED, SOLD, etc.)
- quantity, min_quantity
- location (FK)
- cost_price, selling_price
- barcode, qr_code (auto-generated)

StockMovement         # حركة المخزون
- item (FK)
- movement_type (IN, OUT, ADJUSTMENT, etc.)
- quantity
- from_location, to_location
- reason, reference
```

#### 4. العملاء (Customers)
```python
Customer
- customer_code (auto-generated)
- customer_type (INDIVIDUAL, BUSINESS)
- first_name, last_name, business_name
- email, phone
- address, city, country
- credit_limit
- @property: total_purchases
- @property: outstanding_balance

CustomerCredit
- customer (FK)
- credit_amount
- reason, reference
- is_used

CustomerNote
- customer (FK)
- note
- is_important
```

#### 5. المبيعات (Sales)
```python
Sale
- invoice_number (auto-generated)
- customer (FK)
- status (DRAFT, CONFIRMED, COMPLETED, CANCELLED)
- payment_status (UNPAID, PARTIAL, PAID)
- subtotal, discount_amount, tax_amount
- total_amount, paid_amount
- @property: balance_due

SaleItem
- sale (FK)
- inventory_item (FK)
- quantity
- unit_price, discount_amount
- total_price

Payment
- payment_number (auto-generated)
- sale (FK)
- amount
- payment_method (CASH, CARD, BANK_TRANSFER, etc.)
- reference_number

Cart & CartItem       # سلة التسوق
- user (FK)
- customer (FK, nullable)
- @property: total_items, total_amount
```

### العلاقات بين الجداول

```
CarMake (1) ──→ (N) CarModel
CarModel (N) ←→ (M) Part (compatible_models)
Part (1) ──→ (N) InventoryItem
Part (N) ──→ (1) PartCategory (هرمية)
Vehicle (1) ──→ (N) InventoryItem (extracted_parts)
Customer (1) ──→ (N) Sale
Sale (1) ──→ (N) SaleItem
Sale (1) ──→ (N) Payment
InventoryItem (1) ──→ (N) SaleItem
WarehouseLocation (1) ──→ (N) InventoryItem
```

---

## واجهة برمجة التطبيقات API

### المصادقة (Authentication)

#### الحصول على Token
```http
POST /api/token/
Content-Type: application/json

{
    "email": "admin@shparts.com",
    "password": "admin123"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### تحديث Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### استخدام Token في الطلبات
```http
GET /api/cars/makes/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### السيارات (Cars API)

#### ماركات السيارات
```http
# قائمة الماركات
GET /api/cars/makes/

# إنشاء ماركة جديدة
POST /api/cars/makes/
{
    "name": "Mercedes-Benz",
    "name_ar": "مرسيدس بنز"
}

# موديلات ماركة معينة
GET /api/cars/makes/{id}/models/
```

#### موديلات السيارات
```http
# قائمة الموديلات
GET /api/cars/models/
GET /api/cars/models/?make=1&year_start=2015

# تفاصيل موديل
GET /api/cars/models/{id}/

# القطع المتوافقة مع موديل
GET /api/cars/models/{id}/compatible_parts/
```

#### القطع
```http
# قائمة القطع
GET /api/cars/parts/
GET /api/cars/parts/?category=1&is_universal=false

# البحث عن قطع حسب السيارة
GET /api/cars/parts/search_by_vehicle/?make=1&model=1&year=2020

# تفاصيل قطعة
GET /api/cars/parts/{id}/
```

#### السيارات
```http
# قائمة السيارات
GET /api/cars/vehicles/
GET /api/cars/vehicles/?is_dismantled=false

# استقبال سيارة جديدة
POST /api/cars/vehicles/
{
    "vin": "JN1BY1AP5FM123456",
    "make": 1,
    "model": 1,
    "year": 2020,
    "color": "أبيض",
    "mileage": 150000,
    "condition": "GOOD",
    "purchase_price": "25000.00",
    "received_by": 1
}

# تفكيك سيارة
POST /api/cars/vehicles/{id}/dismantle/

# القطع المستخرجة من سيارة
GET /api/cars/vehicles/{id}/extracted_parts/

# رفع صورة
POST /api/cars/vehicles/{id}/upload_photo/
```

### المخزون (Inventory API)

```http
# قائمة المخزون
GET /api/inventory/items/
GET /api/inventory/items/?part__category=1&status=AVAILABLE

# القطع منخفضة المخزون
GET /api/inventory/items/low_stock/

# القطع المتاحة
GET /api/inventory/items/available/

# إضافة قطعة للمخزون
POST /api/inventory/items/
{
    "part": 1,
    "vehicle_source": 1,
    "condition": "USED_GOOD",
    "quantity": 1,
    "location": 1,
    "cost_price": "500.00",
    "selling_price": "750.00",
    "added_by": 1
}

# تعديل الكمية
POST /api/inventory/items/{id}/adjust_quantity/
{
    "quantity": 5,
    "reason": "تعديل الجرد"
}

# حركة المخزون
GET /api/inventory/movements/
GET /api/inventory/movements/?movement_type=OUT
```

### العملاء (Customers API)

```http
# قائمة العملاء
GET /api/customers/
GET /api/customers/?is_active=true&customer_type=INDIVIDUAL

# إضافة عميل
POST /api/customers/
{
    "customer_type": "INDIVIDUAL",
    "first_name": "محمد",
    "last_name": "أحمد",
    "phone": "0501234567",
    "email": "mohamed@example.com",
    "city": "الرياض",
    "created_by": 1
}

# سجل المشتريات
GET /api/customers/{id}/purchase_history/

# الائتمان
GET /api/customers/{id}/credits/
POST /api/customers/{id}/add_credit/
{
    "credit_amount": "1000.00",
    "reason": "تعويض عن مرتجع"
}

# الملاحظات
GET /api/customers/{id}/notes/
POST /api/customers/{id}/add_note/
{
    "note": "عميل مميز",
    "is_important": true
}
```

### المبيعات (Sales API)

```http
# قائمة المبيعات
GET /api/sales/
GET /api/sales/?status=COMPLETED&payment_status=PAID

# إنشاء مبيعة
POST /api/sales/
{
    "customer": 1,
    "sales_person": 1,
    "items": [
        {
            "inventory_item": 1,
            "quantity": 1,
            "unit_price": "750.00"
        }
    ]
}

# تأكيد مبيعة
POST /api/sales/{id}/confirm/

# إتمام مبيعة
POST /api/sales/{id}/complete/

# إلغاء مبيعة
POST /api/sales/{id}/cancel/

# الدفعات
GET /api/sales/{id}/payments/
POST /api/sales/{id}/add_payment/
{
    "amount": "500.00",
    "payment_method": "CASH"
}

# سلة التسوق
GET /api/sales/cart/
POST /api/sales/cart/{id}/add_item/
{
    "inventory_item": 1,
    "quantity": 1
}

POST /api/sales/cart/{id}/checkout/
```

---

## الواجهة الأمامية

### نظام الثيمات

يدعم النظام 3 ثيمات قابلة للتبديل:

1. **الثيم الأزرق الداكن (Default)**
   - ألوان داكنة مريحة للعين
   - مناسب للعمل المستمر

2. **الثيم الفاتح**
   - واجهة نظيفة وواضحة
   - مناسب لبيئات العمل المضيئة

3. **التباين العالي**
   - تباين عالٍ بين العناصر
   - مناسب لذوي الاحتياجات الخاصة

#### تغيير الثيم برمجياً
```javascript
// في المتصفح
app.changeTheme('dark-blue');  // أو 'light' أو 'high-contrast'
```

### دعم اللغات

النظام يدعم العربية والإنجليزية مع RTL كامل.

#### تغيير اللغة برمجياً
```javascript
app.changeLanguage('ar');  // أو 'en'
```

#### إضافة ترجمات جديدة
1. افتح ملف `/static/js/translations/ar.json` أو `en.json`
2. أضف المفاتيح الجديدة
3. استخدم attribute `data-translate` في HTML:

```html
<span data-translate="my_key">النص الافتراضي</span>
```

### طلبات API من الواجهة

```javascript
// مثال: جلب بيانات المخزون
async function loadInventory() {
    const data = await app.apiRequest('/api/inventory/items/');
    if (data) {
        // معالجة البيانات
        console.log(data);
    }
}

// مثال: إضافة عميل
async function addCustomer(customerData) {
    const data = await app.apiRequest('/api/customers/', {
        method: 'POST',
        body: JSON.stringify(customerData)
    });
    
    if (data) {
        app.showNotification('تم إضافة العميل بنجاح', 'success');
    }
}
```

### الأدوات المساعدة

```javascript
// تنسيق التاريخ
app.formatDate('2024-01-15T10:30:00');
// النتيجة: ١٥ يناير ٢٠٢٤ ١٠:٣٠ (بالعربية)

// تنسيق الأرقام
app.formatNumber(1234567);
// النتيجة: ١٬٢٣٤٬٥٦٧ (بالعربية)

// تنسيق العملة
app.formatCurrency(1500.50);
// النتيجة: ١٬٥٠٠٫٥٠ ر.س (بالعربية)

// إظهار إشعار
app.showNotification('عملية ناجحة', 'success');
// الأنواع: success, danger, warning, info

// مؤشر التحميل
app.showLoading();
// ... عمليات
app.hideLoading();
```

---

## دليل الاستخدام

### 1. استقبال سيارة جديدة

1. الذهاب إلى قسم "السيارات" → "استقبال مركبة"
2. إدخال بيانات السيارة (VIN، الماركة، الموديل، السنة)
3. تحديد حالة السيارة والسعر (إن وجد)
4. رفع صور السيارة
5. حفظ البيانات
6. سيتم توليد رقم تعريف فريد للسيارة

### 2. تفكيك سيارة وإضافة القطع

1. فتح تفاصيل السيارة
2. الضغط على "تفكيك السيارة"
3. تحديد القطع المتوفرة من القائمة
4. لكل قطعة:
   - تحديد الحالة (جديد، مستعمل ممتاز، إلخ)
   - تحديد موقع التخزين
   - إدخال السعر
   - رفع صور القطعة
5. سيتم إنشاء:
   - رمز SKU فريد
   - رمز QR للطباعة
   - سجل في المخزون

### 3. البحث عن قطعة

**طريقة 1: البحث حسب السيارة**
1. اختر الماركة
2. اختر الموديل
3. اختر السنة
4. سيظهر لك القطع المتوافقة المتوفرة

**طريقة 2: البحث المباشر**
1. اكتب اسم القطعة أو رقم SKU
2. استخدم الفلاتر (الفئة، الحالة، السعر)

### 4. إتمام عملية بيع

1. البحث عن القطع المطلوبة
2. إضافتها للسلة
3. تحديد العميل (أو إضافة عميل جديد)
4. مراجعة السلة
5. إتمام عملية البيع
6. اختيار طريقة الدفع
7. طباعة الفاتورة

### 5. إدارة دفعات العملاء

1. الذهاب إلى "العملاء"
2. اختيار العميل
3. عرض الفواتير المعلقة
4. تسجيل دفعة جديدة
5. طباعة إيصال الدفع

### 6. التقارير

**تقرير المخزون:**
- عرض جميع القطع المتوفرة
- قيمة المخزون الإجمالية
- القطع منخفضة المخزون

**تقرير المبيعات:**
- مبيعات الفترة المحددة
- أكثر القطع مبيعاً
- توزيع المبيعات حسب الفئة

**تقرير الأرباح:**
- الإيرادات والتكاليف
- هامش الربح
- تحليل الربحية

---

## النشر والإنتاج

### استخدام Docker

#### 1. بناء الصور
```bash
docker-compose build
```

#### 2. تشغيل الخدمات
```bash
docker-compose up -d
```

#### 3. تطبيق التهجيرات
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py import_cars_data
```

#### 4. إنشاء مستخدم إداري
```bash
docker-compose exec web python manage.py createsuperuser
```

### النشر على خادم Linux

#### 1. تثبيت المتطلبات
```bash
sudo apt update
sudo apt install python3.13 python3-pip postgresql nginx redis-server
```

#### 2. إعداد PostgreSQL
```bash
sudo -u postgres createdb sh_parts_db
sudo -u postgres createuser sh_parts_user
sudo -u postgres psql -c "ALTER USER sh_parts_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sh_parts_db TO sh_parts_user;"
```

#### 3. إعداد المشروع
```bash
cd /var/www/sh_parts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 4. تحديث .env للإنتاج
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sh_parts_db
DB_USER=sh_parts_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

#### 5. تطبيق التهجيرات وجمع الملفات الثابتة
```bash
python manage.py migrate
python manage.py import_cars_data
python manage.py collectstatic
```

#### 6. إعداد Gunicorn كخدمة
```bash
# /etc/systemd/system/sh_parts.service
[Unit]
Description=SH Parts Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/sh_parts
Environment="PATH=/var/www/sh_parts/venv/bin"
ExecStart=/var/www/sh_parts/venv/bin/gunicorn --workers 3 --bind unix:/var/www/sh_parts/sh_parts.sock sh_parts.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start sh_parts
sudo systemctl enable sh_parts
```

#### 7. إعداد Nginx
```nginx
# /etc/nginx/sites-available/sh_parts
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/sh_parts;
    }
    
    location /media/ {
        root /var/www/sh_parts;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/sh_parts/sh_parts.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/sh_parts /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 8. إعداد SSL مع Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### النسخ الاحتياطي

#### نسخ احتياطي لقاعدة البيانات
```bash
# نسخ
pg_dump -U sh_parts_user sh_parts_db > backup_$(date +%Y%m%d).sql

# استعادة
psql -U sh_parts_user sh_parts_db < backup_20240115.sql
```

#### نسخ احتياطي للملفات
```bash
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### المراقبة

#### سجلات النظام
```bash
# سجلات Gunicorn
sudo journalctl -u sh_parts -f

# سجلات Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# سجلات Django (في الإنتاج، استخدم logging)
```

---

## الدعم والمساعدة

### الأسئلة الشائعة

**س: كيف أضيف موديلات سيارات جديدة؟**
ج: يمكنك إضافتها من لوحة الإدارة في `/admin/cars/carmodel/` أو عبر API

**س: هل يمكن تغيير العملة من SAR إلى عملة أخرى؟**
ج: نعم، قم بتعديل دالة `formatCurrency` في `static/js/app.js`

**س: كيف أطبع رموز QR للقطع؟**
ج: افتح صفحة القطعة، ستجد رمز QR جاهز للطباعة

**س: هل يمكن إضافة أنواع دفع جديدة؟**
ج: نعم، عدل `PAYMENT_METHOD_CHOICES` في `sales/models.py`

### الاتصال
- **البريد الإلكتروني**: support@shparts.com
- **التوثيق الإضافي**: `/api/docs/` (Swagger UI)

---

## الترخيص
جميع الحقوق محفوظة © 2024 SH Parts

---

**آخر تحديث**: 8 يناير 2024
**الإصدار**: 1.0.0
