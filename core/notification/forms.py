from django import forms
from logs.models import ClientSMSLog

class SMSSendForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ClientSMSLog
        fields = ['subject','message',]
