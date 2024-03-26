from django import forms
from logs.models import ClientSMSLog
from client.models import Client


class SMSSendForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ClientSMSLog
        fields = [
            "subject",
            "message",
        ]


class BulkSMSSendForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ClientSMSLog
        fields = ["clients", "message"]
