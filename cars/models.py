from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CarMake(models.Model):
    name = models.CharField(_('make name'), max_length=100, unique=True)
    name_ar = models.CharField(_('make name (Arabic)'), max_length=100, blank=True)
    logo = models.ImageField(_('logo'), upload_to='car_makes/', blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('car make')
        verbose_name_plural = _('car makes')
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models', verbose_name=_('make'))
    name = models.CharField(_('model name'), max_length=100)
    name_ar = models.CharField(_('model name (Arabic)'), max_length=100, blank=True)
    year_start = models.IntegerField(_('production start year'))
    year_end = models.IntegerField(_('production end year'), null=True, blank=True)
    body_type = models.CharField(_('body type'), max_length=50, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('car model')
        verbose_name_plural = _('car models')
        ordering = ['make', 'name']
        unique_together = ['make', 'name', 'year_start']

    def __str__(self):
        return f"{self.make.name} {self.name}"


class PartCategory(models.Model):
    name = models.CharField(_('category name'), max_length=100, unique=True)
    name_ar = models.CharField(_('category name (Arabic)'), max_length=100, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='subcategories', verbose_name=_('parent category'))
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icon class'), max_length=50, blank=True)
    sort_order = models.IntegerField(_('sort order'), default=0)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('part category')
        verbose_name_plural = _('part categories')
        ordering = ['sort_order', 'name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


class Part(models.Model):
    name = models.CharField(_('part name'), max_length=200)
    name_ar = models.CharField(_('part name (Arabic)'), max_length=200, blank=True)
    category = models.ForeignKey(PartCategory, on_delete=models.PROTECT, 
                                 related_name='parts', verbose_name=_('category'))
    part_number = models.CharField(_('part number'), max_length=100, blank=True)
    description = models.TextField(_('description'), blank=True)
    description_ar = models.TextField(_('description (Arabic)'), blank=True)
    
    compatible_models = models.ManyToManyField(CarModel, related_name='compatible_parts', 
                                               verbose_name=_('compatible models'), blank=True)
    
    default_image = models.ImageField(_('default image'), upload_to='parts/', blank=True, null=True)
    is_universal = models.BooleanField(_('universal part'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('part')
        verbose_name_plural = _('parts')
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Vehicle(models.Model):
    CONDITION_CHOICES = [
        ('EXCELLENT', _('Excellent')),
        ('GOOD', _('Good')),
        ('FAIR', _('Fair')),
        ('POOR', _('Poor')),
        ('SALVAGE', _('Salvage')),
    ]

    vin = models.CharField(_('VIN'), max_length=17, unique=True)
    make = models.ForeignKey(CarMake, on_delete=models.PROTECT, verbose_name=_('make'))
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT, verbose_name=_('model'))
    year = models.IntegerField(_('year'))
    color = models.CharField(_('color'), max_length=50, blank=True)
    mileage = models.IntegerField(_('mileage'), null=True, blank=True)
    condition = models.CharField(_('condition'), max_length=20, choices=CONDITION_CHOICES)
    
    intake_date = models.DateTimeField(_('intake date'), auto_now_add=True)
    intake_notes = models.TextField(_('intake notes'), blank=True)
    purchase_price = models.DecimalField(_('purchase price'), max_digits=10, decimal_places=2, 
                                        null=True, blank=True)
    
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, 
                                   related_name='received_vehicles', verbose_name=_('received by'))
    
    is_dismantled = models.BooleanField(_('dismantled'), default=False)
    dismantled_date = models.DateTimeField(_('dismantled date'), null=True, blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('vehicle')
        verbose_name_plural = _('vehicles')
        ordering = ['-intake_date']

    def __str__(self):
        return f"{self.year} {self.make.name} {self.model.name} - {self.vin}"


class VehiclePhoto(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, 
                               related_name='photos', verbose_name=_('vehicle'))
    image = models.ImageField(_('image'), upload_to='vehicles/')
    caption = models.CharField(_('caption'), max_length=200, blank=True)
    is_primary = models.BooleanField(_('primary photo'), default=False)
    uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)

    class Meta:
        verbose_name = _('vehicle photo')
        verbose_name_plural = _('vehicle photos')
        ordering = ['-is_primary', '-uploaded_at']

    def __str__(self):
        return f"Photo for {self.vehicle.vin}"
