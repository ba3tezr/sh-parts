from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vin', 'make', 'model', 'year', 'color', 'mileage',
            'condition', 'purchase_price', 'intake_notes'
        ]
        widgets = {
            'intake_notes': forms.Textarea(attrs={'rows': 3})
        }


class VehicleUpdateForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'color', 'mileage', 'condition', 'purchase_price', 'intake_notes'
        ]
        widgets = {
            'intake_notes': forms.Textarea(attrs={'rows': 3})
        }


class VehicleDismantleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['is_dismantled', 'dismantled_date']


class VehicleDeleteConfirmForm(forms.Form):
    confirm = forms.BooleanField(label='تأكيد الحذف')

