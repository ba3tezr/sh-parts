# 🚀 دليل النشر على Cloudflare Tunnel
# Cloudflare Tunnel Deployment Guide

## نظام SH Parts - Car Parts Management System

---

## 📋 المتطلبات | Requirements

### 1. النظام | System
- ✅ Linux, macOS, or Windows WSL
- ✅ Python 3.8+
- ✅ Internet connection

### 2. الأدوات | Tools
- ✅ Python و pip
- ✅ cloudflared (سيتم تثبيته تلقائياً)

---

## 🎯 طريقة التشغيل السريعة | Quick Start

### الخطوة 1: منح صلاحيات التنفيذ
```bash
chmod +x start_with_cloudflare.sh start_production.sh
```

### الخطوة 2: تشغيل التطبيق مع Cloudflare Tunnel
```bash
./start_with_cloudflare.sh
```

### الخطوة 3: انتظر الرابط
بعد 10-20 ثانية، ستحصل على رابط مثل:
```
https://random-name-1234.trycloudflare.com
```

**هذا هو رابطك العام على الإنترنت! 🎉**

---

## 📱 الوصول للتطبيق | Accessing the App

### 🏠 الصفحة الرئيسية | Home
```
https://your-tunnel-url.trycloudflare.com/
```

### 👤 لوحة الإدارة | Admin Panel
```
URL: https://your-tunnel-url.trycloudflare.com/admin/
Email: admin@shparts.com
Password: admin123
```

### 📊 لوحة التحكم | Dashboard
```
https://your-tunnel-url.trycloudflare.com/dashboard/
```

### 🔧 API Documentation
```
https://your-tunnel-url.trycloudflare.com/api/
```

---

## 🛠️ التثبيت اليدوي لـ cloudflared | Manual cloudflared Installation

### Linux (Debian/Ubuntu)
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

### Linux (Other)
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared
```

### macOS
```bash
brew install cloudflared
```

### Windows (WSL)
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared
```

---

## 🔧 التشغيل اليدوي | Manual Startup

### 1. تشغيل سيرفر Django
```bash
# في نافذة Terminal الأولى
./start_production.sh
```

### 2. تشغيل Cloudflare Tunnel
```bash
# في نافذة Terminal الثانية
cloudflared tunnel --url http://localhost:8000
```

---

## 📊 مراقبة السجلات | Monitoring Logs

### عرض سجلات Django
```bash
tail -f logs/django.log
```

### عرض سجلات Cloudflare
```bash
tail -f logs/cloudflare.log
```

### عرض كل السجلات معاً
```bash
tail -f logs/*.log
```

---

## 🛑 إيقاف التشغيل | Stopping the Server

### إيقاف سريع
اضغط `Ctrl + C` في نافذة Terminal

### إيقاف يدوي
```bash
# إيقاف Django
pkill -f gunicorn

# إيقاف Cloudflare Tunnel
pkill -f cloudflared
```

---

## ⚙️ الإعدادات المتقدمة | Advanced Configuration

### تغيير المنفذ | Change Port
عدّل في `start_production.sh`:
```bash
--bind 0.0.0.0:8080  # بدلاً من 8000
```

وفي `start_with_cloudflare.sh`:
```bash
cloudflared tunnel --url http://localhost:8080
```

### زيادة عدد Workers
عدّل في `start_production.sh`:
```bash
--workers 8  # بدلاً من 4
```

### تغيير بيانات المدير
بعد التشغيل الأول:
```bash
python3 manage.py changepassword admin@shparts.com
```

---

## 🔒 الأمان | Security

### ⚠️ ملاحظات مهمة:

1. **الرابط المؤقت**
   - الرابط يتغير في كل مرة تعيد التشغيل
   - هذا طبيعي مع الأنفاق المجانية

2. **بيانات الدخول**
   - غيّر كلمة المرور الافتراضية فوراً
   - استخدم كلمات مرور قوية

3. **قاعدة البيانات**
   - يتم استخدام SQLite (ملف محلي)
   - احفظ نسخة احتياطية من `db.sqlite3`

4. **الملفات المرفوعة**
   - تُحفظ في مجلد `media/`
   - احفظ نسخة احتياطية منها

---

## 🌐 نفق دائم (اختياري) | Permanent Tunnel (Optional)

إذا أردت رابط ثابت لا يتغير:

### 1. إنشاء حساب Cloudflare
```bash
cloudflared tunnel login
```

### 2. إنشاء نفق دائم
```bash
cloudflared tunnel create sh-parts
```

### 3. تكوين النفق
أنشئ ملف `config.yml`:
```yaml
tunnel: <TUNNEL-ID>
credentials-file: /home/user/.cloudflared/<TUNNEL-ID>.json

ingress:
  - hostname: your-domain.com
    service: http://localhost:8000
  - service: http_status:404
```

### 4. تشغيل النفق الدائم
```bash
cloudflared tunnel run sh-parts
```

---

## 🐛 حل المشاكل | Troubleshooting

### المشكلة: cloudflared not found
**الحل:**
```bash
# أعد تثبيت cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

### المشكلة: Django server not responding
**الحل:**
```bash
# تحقق من السجلات
cat logs/django.log

# تحقق من المنفذ
netstat -tulpn | grep 8000

# أعد التشغيل
pkill -f gunicorn
./start_production.sh
```

### المشكلة: No tunnel URL appears
**الحل:**
```bash
# تحقق من سجلات Cloudflare
cat logs/cloudflare.log

# تحقق من الاتصال بالإنترنت
ping cloudflare.com

# أعد تشغيل النفق
pkill -f cloudflared
cloudflared tunnel --url http://localhost:8000
```

### المشكلة: Static files not loading
**الحل:**
```bash
# أعد جمع الملفات الثابتة
python3 manage.py collectstatic --noinput --settings=production_settings
```

### المشكلة: Database errors
**الحل:**
```bash
# أعد تطبيق التهجيرات
python3 manage.py migrate --settings=production_settings
```

---

## 📦 النسخ الاحتياطي | Backup

### نسخ احتياطي سريع
```bash
# إنشاء مجلد النسخ الاحتياطية
mkdir -p backups

# نسخ قاعدة البيانات
cp db.sqlite3 backups/db_$(date +%Y%m%d_%H%M%S).sqlite3

# نسخ الملفات المرفوعة
tar -czf backups/media_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

### استعادة النسخة الاحتياطية
```bash
# استعادة قاعدة البيانات
cp backups/db_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3

# استعادة الملفات المرفوعة
tar -xzf backups/media_YYYYMMDD_HHMMSS.tar.gz
```

---

## 📞 الدعم | Support

### الموارد المفيدة:
- 📖 [Cloudflare Tunnel Docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- 📖 [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
- 📖 [Gunicorn Documentation](https://docs.gunicorn.org/)

---

## ✅ قائمة التحقق | Checklist

قبل النشر، تأكد من:

- [ ] تم تثبيت Python 3.8+
- [ ] تم تثبيت جميع المكتبات من requirements.txt
- [ ] تم منح صلاحيات التنفيذ للسكريبتات
- [ ] يعمل الاتصال بالإنترنت
- [ ] تم تغيير كلمة مرور المدير الافتراضية
- [ ] تم عمل نسخة احتياطية من قاعدة البيانات

---

## 🎉 مبروك!

تطبيقك الآن على الإنترنت ويمكن الوصول إليه من أي مكان في العالم!

Your app is now live and accessible from anywhere in the world!

---

**تم إنشاؤه بواسطة | Created by:** Augment Agent  
**التاريخ | Date:** 2025-10-15  
**النظام | System:** SH Parts - Car Dismantling & Parts Management

