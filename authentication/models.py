from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username field must be set'))
        if email:
            email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, password, email=email, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('ADMIN', _('Administrator')),
        ('MANAGER', _('Manager')),
        ('SALES', _('Sales')),
        ('WAREHOUSE', _('Warehouse')),
    ]

    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, default='SALES')

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), null=True, blank=True)

    two_factor_enabled = models.BooleanField(_('2FA enabled'), default=False)
    two_factor_secret = models.CharField(_('2FA secret'), max_length=32, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
