from django import forms
from predict.models import Classification


class ClassificationForm(forms.ModelForm):
    class Meta:
        model = Classification
        fields = ["img"]
