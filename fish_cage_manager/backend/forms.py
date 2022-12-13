from django import forms

from backend.models import MonthStat


class MonthStatForm(forms.ModelForm):
    class Meta:
        model = MonthStat
        fields = "__all__"
        widgets = {
            'cage': forms.HiddenInput(),
        }

