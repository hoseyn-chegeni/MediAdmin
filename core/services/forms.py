from django import forms
from .models import Service

class ServiceSelectionForm(forms.Form):
    services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=forms.CheckboxSelectMultiple)
    percentage_change = forms.DecimalField(label='Percentage Change (%)')
