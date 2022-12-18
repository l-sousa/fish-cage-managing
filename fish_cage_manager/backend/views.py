import json

from django.shortcuts import render, redirect

from backend.forms import MonthStatForm, WeightRange
from backend.models import Cage, MonthStat
from backend.tables import *


# tables["6-8"]["1500-2500"]["mort"]

# ALL CAGE MANAGING
def all_cages(request):
    cages = Cage.objects.all().order_by('-cage_id')
    return render(request, "all_cages.html", context={"cages": cages})


def new_cage(request):
    if Cage.objects.all():
        cage_id = len(Cage.objects.all()) if not Cage.objects.filter(
            cage_id=len(Cage.objects.all())).first() else find_smallest_cage_id()
    else:
        cage_id = 1

    cage = Cage.objects.create(cage_id=cage_id)

    cages = Cage.objects.all().order_by('-cage_id')
    return render(request, "all_cages.html", context={"cages": cages, "new_cage_id": cage.cage_id})


def find_smallest_cage_id():
    cages = Cage.objects.all()
    counter = 1
    while Cage.objects.filter(cage_id=counter).first():
        counter += 1
    return counter


def delete_cage(request, cage_id):
    Cage.objects.filter(cage_id=cage_id).delete()
    return redirect('/')


# SINGLE CAGE MANAGING

def individual_cage(request, cage_id):
    cage = Cage.objects.get(cage_id=cage_id)

    # create object of form
    form = MonthStatForm(request.POST or None, request.FILES or None, initial={'cage': cage_id})

    cages = Cage.objects.all()
    cages_ids = [cage.cage_id for cage in cages]

    obj = None
    # check if form data is valid
    if form.is_valid():
        # save the form data to model

        if MonthStat.objects.all().filter(month_name=form.cleaned_data['month_name'], year=form.cleaned_data['year'],
                                          cage_id=cage.cage_id):
            return render(request, "individual_cage.html",
                          context={"cage": cage,
                                   "monthstats": sorted(cage.monthstat_set.all(),
                                                        key=lambda x: (x.year, months.index(x.month_name)),
                                                        reverse=True), "form": form,
                                   "temperature_tables": json.dumps(values_tables),
                                   "month_temperature_table": json.dumps(month_temperature_table),
                                   "cages": cages,
                                   "cages_ids": cages_ids,
                                   "error": "Está a inserir um mês repetido! Atualizar ou apagar o registo atual."})

        next_month_fishes = form.cleaned_data['num_fishes']
        next_month_medium_weight = form.cleaned_data['medium_weight']

        update_previous_month_data(form.cleaned_data['month_name'], form.cleaned_data['year'], next_month_fishes,
                                   next_month_medium_weight)

        came_from_data = json.loads(form.cleaned_data['calibration_came_from'])
        total_fish_in = 0
        for cage_id, data in came_from_data.items():
            num_fish_out, monthstat_id = data
            m = MonthStat.objects.get(id=monthstat_id)
            current_num_fishes = m.num_fishes - int(num_fish_out)
            total_fish_in += int(num_fish_out)
            m.num_fishes = current_num_fishes
            m.save()

        goes_to_data = json.loads(form.cleaned_data['calibration_goes_to'])

        total_fish_out = 0

        for cage_id, data in goes_to_data.items():
            num_fish_out, monthstat_id = data
            m = MonthStat.objects.get(id=monthstat_id)
            current_num_fishes = m.num_fishes + int(num_fish_out)
            total_fish_out += int(num_fish_out)
            m.num_fishes = current_num_fishes
            m.save()

        obj = form.save()
        monthstat = MonthStat.objects.get(id=obj.pk)
        monthstat.num_fishes += total_fish_in
        monthstat.num_fishes -= total_fish_out
        monthstat.save()

    new_monthstat_pk = None
    if obj:
        new_monthstat_pk = obj.pk

    return render(request, "individual_cage.html",
                  context={"cage": cage,
                           "monthstats": sorted(cage.monthstat_set.all(),
                                                key=lambda x: (x.year, months.index(x.month_name)),
                                                reverse=True), "form": form,
                           "temperature_tables": json.dumps(values_tables),
                           "month_temperature_table": json.dumps(month_temperature_table),
                           "cages": cages,
                           "cages_ids": cages_ids, "new_monthstat_pk": new_monthstat_pk})


def update_previous_month_data(month, year, new_month_num_fishes, new_month_medium_weight):
    previous_month = months[months.index(month) - 1]

    if previous_month == "Dezembro":
        previous_year = year - 1
    else:
        previous_year = year

    previous_monthstat = MonthStat.objects.filter(month_name=previous_month, year=previous_year)

    if len(previous_monthstat) == 0:
        return

    previous_monthstat[
        0].biomass_increase_with_mortality = round(new_month_medium_weight * new_month_num_fishes - getattr(
        previous_monthstat[0], "medium_weight") * getattr(previous_monthstat[0], "num_fishes"), 4)

    previous_monthstat[0].real_fc_with_mortality = round(
        getattr(previous_monthstat[0], "real_30_days_feeding") / getattr(
            previous_monthstat[0], "biomass_increase_with_mortality"), 4) if getattr(previous_monthstat[0],
                                                                                     "biomass_increase_with_mortality") else 0

    previous_monthstat[0].save()

    return


def update_monthstat(request, monthstat_id, cage_id):
    monthstat = MonthStat.objects.get(pk=monthstat_id)

    if request.method == 'POST':

        form = MonthStatForm(request.POST, instance=monthstat)

        if form.is_valid():
            print("valid")
            form.save()
            return redirect("/cage/" + str(cage_id))
    else:
        form = MonthStatForm(instance=monthstat)

    return render(request, 'update_monthstat.html', {'form': form, 'monthstat': monthstat, 'cage_id': cage_id})


def delete_monthstat(request, monthstat_id, cage_id):
    monthstat = MonthStat.objects.get(pk=monthstat_id)
    monthstat.delete()
    return redirect("/cage/" + str(cage_id))


def statistics(request):
    cages = Cage.objects.all()

    total_kgs = {}

    for cage in cages:
        for month in cage.monthstat_set.all():
            y = month.year
            m = month.month_name

            if y in total_kgs and m in total_kgs[y]:
                total_kgs[y][m] += month.food_portion_kg

            elif y in total_kgs:
                total_kgs[y][m] = month.food_portion_kg
            else:
                total_kgs[y] = {}
                total_kgs[y][m] = month.food_portion_kg

            total_kgs[y][m] = round(total_kgs[y][m], 4)

    fish_weight_distribution = {}

    for cage in cages:
        for month in cage.monthstat_set.all():
            y = month.year
            m = month.month_name

            m_mw = month.medium_weight * 1000

            if 0 < m_mw <= 10:
                mw_range = "0-10"
            elif 10 < m_mw <= 50:
                mw_range = "10-50"
            elif 50 < m_mw <= 100:
                mw_range = "50-100"
            elif 100 < m_mw <= 200:
                mw_range = "100-200"
            elif 200 < m_mw <= 350:
                mw_range = "200-350"
            elif 350 < m_mw <= 500:
                mw_range = "350-500"
            elif 500 < m_mw <= 600:
                mw_range = "500-600"
            elif 600 < m_mw <= 700:
                mw_range = "600-700"
            elif 700 < m_mw <= 1000:
                mw_range = "700-1"
            else:
                mw_range = "1-1,5"

            if y in fish_weight_distribution and m in fish_weight_distribution[y]:
                fish_weight_distribution[y][m][mw_range] += month.num_fishes
                fish_weight_distribution[y][m]["mw"] = m_mw

            elif y in fish_weight_distribution:
                fish_weight_distribution[y][m] = {"0-10": 0,
                                                  "10-50": 0,
                                                  "50-100": 0,
                                                  "100-200": 0,
                                                  "200-350": 0,
                                                  "350-500": 0,
                                                  "500-600": 0,
                                                  "600-700": 0,
                                                  "700-1": 0,
                                                  "1-1,5": 0}
                fish_weight_distribution[y][m][mw_range] = month.num_fishes
                fish_weight_distribution[y][m]["mw"] = m_mw

            else:
                fish_weight_distribution[y] = {}
                fish_weight_distribution[y][m] = {"0-10": 0,
                                                  "10-50": 0,
                                                  "50-100": 0,
                                                  "100-200": 0,
                                                  "200-350": 0,
                                                  "350-500": 0,
                                                  "500-600": 0,
                                                  "600-700": 0,
                                                  "700-1": 0,
                                                  "1-1,5": 0}
                fish_weight_distribution[y][m][mw_range] = month.num_fishes
                fish_weight_distribution[y][m]["mw"] = m_mw

    form = WeightRange(request.POST or None, request.FILES or None)

    predictions = {}

    if form.is_valid():
        mw_range = form.cleaned_data["classe_tamanho"]

        for year, data in fish_weight_distribution.items():
            predictions[year] = {}
            for month, mdata in data.items():
                predictions[year][month] = {"biomassa": mdata[mw_range] * mdata["mw"], "num_peixes": mdata[mw_range]}

    print(predictions)
    return render(request, "statistics.html",
                  context={"total_kgs": total_kgs, "fish_weight_distribution": fish_weight_distribution, "form": form,
                           "predictions": predictions})
