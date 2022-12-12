from django.shortcuts import render, redirect

from backend.models import Cage


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
    cage = Cage.objects.filter(cage_id=cage_id).first()
    monthstats = cage.monthstat_set.all()
    print(monthstats)
    return render(request, "individual_cage.html", context={"cage": cage})


def statistics(request):
    return render(request, "statistics.html")
