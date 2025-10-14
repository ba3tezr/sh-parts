from django import forms
from cars.models import Part
from .models import InventoryItem, WarehouseLocation, StockMovement


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['name', 'name_ar', 'category', 'part_number', 'description', 'description_ar', 'compatible_models', 'default_image', 'is_universal', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'description_ar': forms.Textarea(attrs={'rows': 3}),
            'compatible_models': forms.SelectMultiple(attrs={'size': 6}),
        }


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            'part', 'vehicle_source', 'condition', 'status', 'quantity', 'min_quantity',
            'location', 'cost_price', 'selling_price', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class StockUpdateForm(forms.Form):
    quantity_delta = forms.IntegerField(min_value=-100000, label='تغيير الكمية (زيادة / نقصان)', help_text='أدخل قيمة موجبة للزيادة أو سالبة للنقصان')


class StockTransferForm(forms.Form):
    item = forms.ModelChoiceField(queryset=InventoryItem.objects.all())
    from_location = forms.ModelChoiceField(queryset=WarehouseLocation.objects.all(), required=False)
    to_location = forms.ModelChoiceField(queryset=WarehouseLocation.objects.all())
    quantity = forms.IntegerField(min_value=1)


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['item', 'movement_type', 'quantity', 'from_location', 'to_location', 'reason', 'reference']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2}),
        }

