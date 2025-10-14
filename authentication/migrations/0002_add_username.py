from django.db import migrations, models
import django.utils.timezone
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        # Add username field (temporarily nullable to avoid requiring a default)
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(_('username'), max_length=150, unique=True, null=True, blank=True),
        ),
        # Make email optional (we still keep it unique if provided)
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(_('email address'), max_length=254, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(_('first name'), max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(_('last name'), max_length=150, blank=True),
        ),
    ]

