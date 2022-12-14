"""fish_cage_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.all_cages, name="all_cages"),
    path('cage/<int:cage_id>', views.individual_cage, name="individual_cage"),
    path('stats/', views.statistics, name="stats"),
    path('new_cage/', views.new_cage, name="new_cage"),
    path('delete_cage/<int:cage_id>', views.delete_cage, name="delete_cage"),
    path('update/monthstat/<int:monthstat_id>/<int:cage_id>', views.update_monthstat, name="update_monthstat"),
    path('delete/monthstat/<int:monthstat_id>/<int:cage_id>', views.delete_monthstat, name="delete_monthstat"),

]
