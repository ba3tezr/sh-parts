from django import forms
from .models import Sale, SaleItem


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'discount_amount', 'tax_amount', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['inventory_item', 'quantity', 'unit_price', 'discount_percent', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }


class SaleConfirmForm(forms.Form):
    confirm = forms.BooleanField(label='تأكيد إتمام البيع')


class SaleCancelForm(forms.Form):
    reason = forms.CharField(label='سبب الإلغاء', widget=forms.Textarea(attrs={'rows': 2}), required=False)

