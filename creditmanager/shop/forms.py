from django import forms
from .models import Customer, Entry

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number']  # include phone_number
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['goods', 'amount', 'remarks', 'is_payment']
