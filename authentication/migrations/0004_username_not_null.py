from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_populate_username_and_create_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(_('username'), max_length=150, unique=True, null=False, blank=False),
        ),
    ]

