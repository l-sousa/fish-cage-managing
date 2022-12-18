from django import forms

from backend.models import MonthStat


class MonthStatForm(forms.ModelForm):
    class Meta:
        model = MonthStat

        fields = '__all__'

        widgets = {
            'cage': forms.HiddenInput(),
            'biomass_increase_with_mortality': forms.HiddenInput(),
            'real_fc_with_mortality': forms.HiddenInput(),
            'month_name': forms.Select(choices=(
                ('', 'Selecionar mês'),
                ('Janeiro', 'Janeiro'),
                ('Fevereiro', 'Fevereiro'),
                ('Março', 'Março'),
                ('Abril', 'Abril'),
                ('Maio', 'Maio'),
                ('Junho', 'Junho'),
                ('Julho', 'Julho'),
                ('Agosto', 'Agosto'),
                ('Setembro', 'Setembro'),
                ('Outubro', 'Outubro'),
                ('Novembro', 'Novembro'),
                ('Dezembro', 'Dezembro'),
            ), attrs={'class': 'form-control'}),

        }


class WeightRange(forms.Form):
    classe_tamanho = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                       choices=(('', 'Selecionar'),
                                                ('0-10', '0-10'),
                                                ('10-50', '10-50'),
                                                ('50-100', '50-100'),
                                                ('100-200', '100-200'),
                                                ('200-350', '200-350'),
                                                ('350-500', '350-500'),
                                                ('500-600', '500-600'),
                                                ('600-700', '600-700'),
                                                ('700-1', '700-1'),
                                                ('1-1,5', '1-1,5')))