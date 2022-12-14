import json

from django.shortcuts import render, redirect

from backend.forms import MonthStatForm
from backend.models import Cage, MonthStat
from backend.tables import *


# tables["6-8"]["1500-2500"]["mort"]

# ALL CAGE MANAGING
def all_cages(request):
    cages = Cage.objects.all().order_by('-cage_id')
    return render(request, "all_cages.html", context={"cages": cages})


def new_cage(request):
    cage_id = len(Cage.objects.all()) if not Cage.objects.filter(
        cage_id=len(Cage.objects.all())).first() else find_smallest_cage_id()
    cage = Cage.objects.create(cage_id=cage_id)

    cages = Cage.objects.all().order_by('-cage_id')
    return render(request, "all_cages.html", context={"cages": cages, "new_cage_id": cage.cage_id})


def find_smallest_cage_id():
    cages = Cage.objects.all()
    counter = 1
    while Cage.objects.filter(cage_id=counter):
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

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        next_month_fishes = form.cleaned_data['num_fishes']
        next_month_medium_weight = form.cleaned_data['medium_weight']

        update_previous_month_data(form.cleaned_data['month_name'], form.cleaned_data['year'], next_month_fishes,
                                   next_month_medium_weight)
        form.save()

    return render(request, "individual_cage.html",
                  context={"cage": cage,
                           "monthstats": sorted(cage.monthstat_set.all(),
                                                key=lambda x: (x.year, months.index(x.month_name)),
                                                reverse=True), "form": form,
                           "temperature_tables": json.dumps(values_tables),
                           "month_temperature_table": json.dumps(month_temperature_table)})


def update_previous_month_data(month, year, new_month_num_fishes, new_month_medium_weight):
    previous_month = months[months.index(month) - 1]

    if previous_month == "Dezembro":
        previous_year = year - 1
    else:
        previous_year = year

    previous_monthstat = MonthStat.objects.filter(month_name=previous_month, year=previous_year)

    if len(previous_monthstat) == 0:
        return

    previous_monthstat[0].biomass_increase_with_mortality = new_month_medium_weight * new_month_num_fishes - getattr(
        previous_monthstat[0], "medium_weight") * getattr(previous_monthstat[0], "num_fishes")

    previous_monthstat[0].real_fc_with_mortality = getattr(previous_monthstat[0], "real_30_days_feeding") / getattr(
        previous_monthstat[0], "biomass_increase_with_mortality") if getattr(previous_monthstat[0], "biomass_increase_with_mortality") else 0

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

    return render(request, 'update_monthstat.html', {'form': form})


def delete_monthstat(request, monthstat_id, cage_id):
    monthstat = MonthStat.objects.get(pk=monthstat_id)
    monthstat.delete()
    return redirect("/cage/" + str(cage_id))


def statistics(request):
    return render(request, "statistics.html")
