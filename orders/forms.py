from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items']

    def clean_items(self):
        items = self.cleaned_data['items']
        for item in items.split('\n'):
            try:
                _, price = item.rsplit('-', 1)
                float(price.strip())
            except (ValueError, IndexError):
                raise forms.ValidationError(
                    "Каждая строка должна быть в формате 'Название - Цена', например: 'Борщ - 150'"
                )
        return items
