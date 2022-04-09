from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
        class Meta:
                model = Item
                fields = ('description', 'quantity', 'category', 'image', 'freshTill')

class VerifyItemForm(forms.ModelForm):
        class Meta:
                model = Item
                fields = ('isQualityOK', 'isQuantityOK', 'category', 'image', 'freshTill')