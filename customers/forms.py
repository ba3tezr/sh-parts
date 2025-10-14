from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'notes', 'is_active']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

