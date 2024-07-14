from django import forms
from .models import MealRecord

class MealRecordForm(forms.ModelForm):
    class Meta:
        model = MealRecord
        fields = ['date', 'breakfast', 'lunch', 'dinner', 'snack', 'weight', 'notes']


class SearchForm(forms.Form):
    query = forms.CharField(label='メニュー検索', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
