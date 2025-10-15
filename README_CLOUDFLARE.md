# ☁️ نشر نظام SH Parts على Cloudflare Tunnel
# Deploy SH Parts on Cloudflare Tunnel

<div dir="rtl">

## 🎯 نظرة عامة

تم تجهيز نظام SH Parts للنشر المجاني على الإنترنت باستخدام **Cloudflare Tunnel**. 

### ✨ المميزات:
- ✅ **مجاني 100%** - لا تحتاج لدفع أي شيء
- ✅ **رابط عام على الإنترنت** - يمكن الوصول إليه من أي مكان
- ✅ **سهل التشغيل** - أمر واحد فقط
- ✅ **آمن** - يستخدم HTTPS تلقائياً
- ✅ **سريع** - شبكة Cloudflare العالمية

</div>

---

## 🚀 التشغيل السريع | Quick Start

### خطوة واحدة فقط:

```bash
./start_with_cloudflare.sh
```

**انتظر 20-30 ثانية وستحصل على رابط مثل:**
```
https://random-words-1234.trycloudflare.com
```

---

## 📋 ما تم تجهيزه | What's Included

### الملفات الجديدة:

1. **`production_settings.py`**
   - إعدادات Django للإنتاج
   - مُحسّن للأداء والأمان
   - يستخدم SQLite (بسيط وسريع)

2. **`start_production.sh`**
   - سكريبت تشغيل سيرفر الإنتاج
   - يستخدم Gunicorn (4 workers)
   - يجهز قاعدة البيانات تلقائياً

3. **`start_with_cloudflare.sh`**
   - السكريبت الرئيسي للنشر
   - يثبت cloudflared تلقائياً
   - يشغل Django + Cloudflare Tunnel
   - يعرض الرابط العام

4. **`test_setup.sh`**
   - اختبار الإعداد قبل النشر
   - يتحقق من جميع المتطلبات

5. **الأدلة:**
   - `CLOUDFLARE_DEPLOYMENT_GUIDE.md` - دليل شامل
   - `QUICK_START.md` - دليل سريع
   - `ابدأ_هنا.txt` - تعليمات بالعربية

---

## 🔧 المتطلبات | Requirements

<div dir="rtl">

### ما تحتاجه:
- ✅ Python 3.8+ (موجود ✓)
- ✅ pip (موجود ✓)
- ✅ اتصال بالإنترنت
- ✅ نظام Linux/macOS/WSL

### ما سيتم تثبيته تلقائياً:
- cloudflared (أداة Cloudflare Tunnel)

</div>

---

## 📱 الوصول للتطبيق | Access

<div dir="rtl">

بعد التشغيل، ستحصل على رابط عام. يمكنك الوصول إلى:

</div>

### 🏠 الصفحة الرئيسية
```
https://your-url.trycloudflare.com/
```

### 👤 لوحة الإدارة
```
URL: https://your-url.trycloudflare.com/admin/
Email: admin@shparts.com
Password: admin123
```

### 📊 لوحة التحكم
```
https://your-url.trycloudflare.com/dashboard/
```

### 🔧 API
```
https://your-url.trycloudflare.com/api/
```

---

## 🎬 خطوات التشغيل التفصيلية | Detailed Steps

### 1. اختبار الإعداد (اختياري)
```bash
./test_setup.sh
```

### 2. تشغيل التطبيق
```bash
./start_with_cloudflare.sh
```

### 3. انتظر الرابط
<div dir="rtl">
سيظهر لك رابط مثل:
</div>

```
✅ SUCCESS! Your app is now live!
✅ نجح! تطبيقك الآن على الإنترنت!

🌐 Public URL / الرابط العام:
   https://abc-def-123.trycloudflare.com
```

### 4. شارك الرابط
<div dir="rtl">
يمكنك الآن مشاركة هذا الرابط مع أي شخص في العالم!
</div>

---

## 🛑 إيقاف التشغيل | Stop Server

<div dir="rtl">

### الطريقة السهلة:
اضغط `Ctrl + C` في نافذة Terminal

### الطريقة اليدوية:
</div>

```bash
# إيقاف Django
pkill -f gunicorn

# إيقاف Cloudflare Tunnel
pkill -f cloudflared
```

---

## 📊 مراقبة السجلات | Logs

<div dir="rtl">

يتم حفظ السجلات في مجلد `logs/`:

</div>

```bash
# سجلات Django
tail -f logs/django.log

# سجلات Cloudflare
tail -f logs/cloudflare.log

# كل السجلات
tail -f logs/*.log
```

---

## ⚠️ ملاحظات مهمة | Important Notes

<div dir="rtl">

### 1. الرابط المؤقت
- الرابط يتغير في كل مرة تعيد التشغيل
- هذا طبيعي مع الأنفاق المجانية
- إذا أردت رابط ثابت، راجع قسم "نفق دائم" في الدليل الشامل

### 2. الأمان
- **غيّر كلمة المرور فوراً** بعد أول تسجيل دخول
- استخدم كلمات مرور قوية
- لا تشارك بيانات الدخول

### 3. النسخ الاحتياطي
احفظ نسخة من:
- `db.sqlite3` - قاعدة البيانات
- `media/` - الملفات المرفوعة

### 4. الأداء
- السيرفر يستخدم 4 workers
- مناسب لـ 50-100 مستخدم متزامن
- لزيادة الأداء، عدّل عدد workers في `start_production.sh`

</div>

---

## 🔒 تغيير كلمة المرور | Change Password

```bash
# بعد التشغيل الأول
python3 manage.py changepassword admin@shparts.com --settings=production_settings
```

---

## 💾 النسخ الاحتياطي | Backup

```bash
# نسخ قاعدة البيانات
cp db.sqlite3 backups/db_$(date +%Y%m%d_%H%M%S).sqlite3

# نسخ الملفات المرفوعة
tar -czf backups/media_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

---

## 🐛 حل المشاكل | Troubleshooting

### المشكلة: cloudflared not found
```bash
# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# macOS
brew install cloudflared
```

### المشكلة: Port 8000 already in use
```bash
lsof -ti:8000 | xargs kill -9
```

### المشكلة: Django not responding
```bash
# تحقق من السجلات
cat logs/django.log

# أعد التشغيل
pkill -f gunicorn
./start_production.sh
```

---

## 📖 المزيد من المعلومات | More Info

<div dir="rtl">

للحصول على معلومات تفصيلية، راجع:

</div>

- **`CLOUDFLARE_DEPLOYMENT_GUIDE.md`** - الدليل الشامل
- **`QUICK_START.md`** - الدليل السريع
- **`ابدأ_هنا.txt`** - التعليمات بالعربية

---

## 🎉 مبروك! | Congratulations!

<div dir="rtl">

تطبيقك الآن جاهز للنشر على الإنترنت مجاناً!

فقط نفذ:

</div>

```bash
./start_with_cloudflare.sh
```

<div dir="rtl">

وستحصل على رابط عام يمكنك مشاركته مع العالم! 🌍

</div>

---

**Created by:** Augment Agent  
**Date:** 2025-10-15  
**System:** SH Parts - Car Dismantling & Parts Management

