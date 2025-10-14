from django.db import migrations
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password


def populate_usernames_and_create_admin(apps, schema_editor):
    User = apps.get_model('authentication', 'User')

    # Populate username for existing users if missing
    for user in User.objects.filter(username__isnull=True):
        base = None
        if user.email:
            base = user.email.split('@')[0]
        if not base:
            base = f"user{user.id}"
        candidate = slugify(base) or f"user{user.id}"
        unique = candidate
        idx = 1
        while User.objects.filter(username=unique).exists():
            idx += 1
            unique = f"{candidate}{idx}"
        user.username = unique
        user.save(update_fields=['username'])

    # Create default superuser if not exists
    if not User.objects.filter(username='admin').exists():
        admin = User(
            username='admin',
            email=None,
            first_name='Admin',
            last_name='User',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        admin.password = make_password('admin123')
        admin.save()


def reverse_create_admin(apps, schema_editor):
    User = apps.get_model('authentication', 'User')
    # Do not delete admin on reverse; it's safer to keep data
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_add_username'),
    ]

    operations = [
        migrations.RunPython(populate_usernames_and_create_admin, reverse_create_admin),
    ]

