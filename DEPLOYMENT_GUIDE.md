# دليل النشر السريع - Quick Deployment Guide
## نظام SH Parts

---

## التشغيل المحلي - Local Development

### البدء السريع
```bash
# الانتقال للمشروع
cd "/home/zakee/shalah projevt"

# تفعيل البيئة الافتراضية
source venv/bin/activate

# تشغيل الخادم
python manage.py runserver
```

### الوصول للنظام
- الصفحة الرئيسية: http://localhost:8000/
- لوحة الإدارة: http://localhost:8000/admin/
- واجهة API: http://localhost:8000/api/

### البيانات الافتراضية
```
Email: admin@shparts.com
Password: admin123
```

---

## النشر بـ Docker - Docker Deployment

### 1. بناء وتشغيل الحاويات
```bash
cd "/home/zakee/shalah projevt"

# بناء الصور
docker-compose build

# تشغيل الخدمات
docker-compose up -d

# مشاهدة السجلات
docker-compose logs -f
```

### 2. تهيئة قاعدة البيانات
```bash
# تطبيق التهجيرات
docker-compose exec web python manage.py migrate

# استيراد بيانات السيارات
docker-compose exec web python manage.py import_cars_data

# إنشاء مستخدم إداري
docker-compose exec web python manage.py createsuperuser
```

### 3. الوصول للنظام
- http://localhost:8000/

### 4. إيقاف الخدمات
```bash
docker-compose down
```

---

## النشر على خادم لينكس - Linux Server Deployment

### المتطلبات
```bash
sudo apt update
sudo apt install -y python3.13 python3-pip python3-venv \
    postgresql postgresql-contrib nginx redis-server git
```

### 1. إعداد PostgreSQL
```bash
# إنشاء قاعدة البيانات والمستخدم
sudo -u postgres psql << EOF
CREATE DATABASE sh_parts_db;
CREATE USER sh_parts_user WITH PASSWORD 'YourStrongPassword123!';
ALTER ROLE sh_parts_user SET client_encoding TO 'utf8';
ALTER ROLE sh_parts_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sh_parts_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sh_parts_db TO sh_parts_user;
EOF
```

### 2. إعداد المشروع
```bash
# إنشاء مجلد المشروع
sudo mkdir -p /var/www/sh_parts
sudo chown $USER:$USER /var/www/sh_parts

# نسخ الملفات
cd /var/www/sh_parts
# ضع ملفات المشروع هنا

# إنشاء بيئة افتراضية
python3 -m venv venv
source venv/bin/activate

# تثبيت المكتبات
pip install -r requirements.txt
pip install gunicorn
```

### 3. إعداد ملف .env للإنتاج
```bash
cat > .env << 'EOF'
SECRET_KEY=generate-a-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

DB_ENGINE=django.db.backends.postgresql
DB_NAME=sh_parts_db
DB_USER=sh_parts_user
DB_PASSWORD=YourStrongPassword123!
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0

LANGUAGE_CODE=ar-sa
TIME_ZONE=Asia/Riyadh
EOF
```

### 4. تهيئة Django
```bash
# تطبيق التهجيرات
python manage.py migrate

# استيراد البيانات
python manage.py import_cars_data

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# إنشاء مستخدم إداري
python manage.py createsuperuser
```

### 5. إعداد Gunicorn كخدمة
```bash
sudo tee /etc/systemd/system/sh_parts.service << 'EOF'
[Unit]
Description=SH Parts Gunicorn Daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/sh_parts
Environment="PATH=/var/www/sh_parts/venv/bin"
ExecStart=/var/www/sh_parts/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/sh_parts/sh_parts.sock \
    --timeout 120 \
    --access-logfile /var/log/sh_parts/access.log \
    --error-logfile /var/log/sh_parts/error.log \
    sh_parts.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# إنشاء مجلد السجلات
sudo mkdir -p /var/log/sh_parts
sudo chown www-data:www-data /var/log/sh_parts

# تعيين الصلاحيات
sudo chown -R www-data:www-data /var/www/sh_parts

# تفعيل الخدمة
sudo systemctl start sh_parts
sudo systemctl enable sh_parts
sudo systemctl status sh_parts
```

### 6. إعداد Nginx
```bash
sudo tee /etc/nginx/sites-available/sh_parts << 'EOF'
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

    location /static/ {
        alias /var/www/sh_parts/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/sh_parts/media/;
        expires 7d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/sh_parts/sh_parts.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
EOF

# تفعيل الموقع
sudo ln -s /etc/nginx/sites-available/sh_parts /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. إعداد SSL مع Let's Encrypt
```bash
# تثبيت Certbot
sudo apt install -y certbot python3-certbot-nginx

# الحصول على شهادة SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# التجديد التلقائي (يعمل تلقائياً)
sudo certbot renew --dry-run
```

### 8. إعداد Celery (للمهام في الخلفية)
```bash
sudo tee /etc/systemd/system/sh_parts_celery.service << 'EOF'
[Unit]
Description=SH Parts Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/var/www/sh_parts
Environment="PATH=/var/www/sh_parts/venv/bin"
ExecStart=/var/www/sh_parts/venv/bin/celery -A sh_parts worker -l info

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl start sh_parts_celery
sudo systemctl enable sh_parts_celery
```

---

## النسخ الاحتياطي - Backup

### نسخ احتياطي يومي تلقائي
```bash
# إنشاء سكريبت النسخ الاحتياطي
sudo tee /usr/local/bin/backup_sh_parts.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/sh_parts"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# نسخ قاعدة البيانات
sudo -u postgres pg_dump sh_parts_db | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# نسخ الملفات
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" /var/www/sh_parts/media/

# حذف النسخ الأقدم من 30 يوم
find "$BACKUP_DIR" -type f -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

sudo chmod +x /usr/local/bin/backup_sh_parts.sh

# إضافة مهمة cron (يومياً الساعة 2 صباحاً)
sudo crontab -e
# أضف السطر التالي:
# 0 2 * * * /usr/local/bin/backup_sh_parts.sh
```

### استعادة النسخة الاحتياطية
```bash
# استعادة قاعدة البيانات
gunzip -c /backups/sh_parts/db_YYYYMMDD_HHMMSS.sql.gz | \
    sudo -u postgres psql sh_parts_db

# استعادة الملفات
tar -xzf /backups/sh_parts/media_YYYYMMDD_HHMMSS.tar.gz -C /
```

---

## المراقبة - Monitoring

### مشاهدة السجلات
```bash
# سجلات Gunicorn
sudo tail -f /var/log/sh_parts/access.log
sudo tail -f /var/log/sh_parts/error.log

# سجلات Systemd
sudo journalctl -u sh_parts -f
sudo journalctl -u sh_parts_celery -f

# سجلات Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### فحص حالة الخدمات
```bash
sudo systemctl status sh_parts
sudo systemctl status sh_parts_celery
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis
```

### إعادة تشغيل الخدمات
```bash
# بعد تحديث الكود
sudo systemctl restart sh_parts
sudo systemctl restart sh_parts_celery

# بعد تحديث إعدادات Nginx
sudo nginx -t && sudo systemctl reload nginx
```

---

## التحديثات - Updates

### تحديث المشروع
```bash
cd /var/www/sh_parts

# جلب آخر التحديثات
git pull origin main

# تفعيل البيئة الافتراضية
source venv/bin/activate

# تحديث المكتبات
pip install -r requirements.txt --upgrade

# تطبيق التهجيرات الجديدة
python manage.py migrate

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# إعادة تشغيل الخدمات
sudo systemctl restart sh_parts
sudo systemctl restart sh_parts_celery
```

---

## الأمان - Security

### قائمة فحص الأمان
- ✅ DEBUG=False في الإنتاج
- ✅ SECRET_KEY طويل وعشوائي
- ✅ SSL/TLS مفعّل
- ✅ كلمات مرور قوية لقاعدة البيانات
- ✅ جدار ناري مفعّل (ufw/firewalld)
- ✅ تحديثات أمنية منتظمة
- ✅ نسخ احتياطية يومية
- ✅ صلاحيات ملفات صحيحة (www-data)

### جدار الحماية
```bash
# تثبيت وإعداد UFW
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
sudo ufw status
```

---

## الاستكشاف وحل المشاكل - Troubleshooting

### المشكلة: الموقع لا يعمل
```bash
# فحص حالة الخدمات
sudo systemctl status sh_parts
sudo systemctl status nginx

# فحص السجلات
sudo journalctl -u sh_parts -n 50
sudo tail -100 /var/log/nginx/error.log
```

### المشكلة: 502 Bad Gateway
```bash
# التأكد من عمل Gunicorn
sudo systemctl restart sh_parts
ps aux | grep gunicorn

# التأكد من وجود ملف Socket
ls -la /var/www/sh_parts/sh_parts.sock
```

### المشكلة: الملفات الثابتة لا تعمل
```bash
# جمع الملفات الثابتة مرة أخرى
cd /var/www/sh_parts
source venv/bin/activate
python manage.py collectstatic --noinput

# التأكد من الصلاحيات
sudo chown -R www-data:www-data /var/www/sh_parts/staticfiles/
```

### المشكلة: قاعدة البيانات لا تتصل
```bash
# فحص PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql -l

# فحص الاتصال
sudo -u postgres psql sh_parts_db -c "SELECT 1;"
```

---

## الموارد - Resources

### الروابط المفيدة
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [PostgreSQL Manual](https://www.postgresql.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)

### معلومات الاتصال
- **التوثيق الكامل**: `DOCUMENTATION_AR.md`
- **الدعم الفني**: support@shparts.com

---

**تم إنشاؤه**: 8 يناير 2024
**الإصدار**: 1.0.0
