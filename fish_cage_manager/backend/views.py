from django.shortcuts import render

def all_cages(request):
    return render(request, "all_cages.html")


def individual_cage(request, id):
    return render(request, "individual_cage.html")

def statistics(request):
    return render(request, "statistics.html")
    