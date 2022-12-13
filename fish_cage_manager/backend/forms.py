from django import forms

from backend.models import MonthStat


class MonthStatForm(forms.ModelForm):
    class Meta:
        model = MonthStat
        # fields = ["cage",
        #           "year",
        #           "num_fishes",
        #           "theoric_medium_weight_with_real_feeding",
        #           "medium_weight",
        #           "biomass",
        #           "percent_feeding",
        #           "fc",
        #           "biomass_increase_with_mortality",
        #           "real_fc_with_mortality",
        #           "food_portion_kg",
        #           "food_portion_bags",
        #           "food_portion_total_30_days",
        #           "theoric_30_days_biomass_increase",
        #           "theoric_30_days_biomass_total",
        #           "theoric_30_days_medium_weight",
        #           "real_30_days_feeding",
        #           "real_30_days_medium_weight_with_real_feeding",
        #           "real_30_days_real_medium_weight",
        #           "real_30_days_biomass",
        #           "mortality_theoric_percentage",
        #           "mortality_theoric_number",
        #           "mortality_real_percentage",
        #           "mortality_real_number",
        #           "calibration_goes_to",
        #           "calibration_came_from"]

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
