from django.db import models

class Cage(models.Model):
    months = [] # MonthStat

class FoodPortion():
    kg = models.FloatField()
    bags = models.FloatField()
    total_30_days = models.FloatField()

class Theoric30Days():
    biomass_increase = models.FloatField()
    biomass_total = models.FloatField()
    medium_weight = models.FloatField()

class Real30Days():
    feeding = models.FloatField()
    medium_weight_with_real_feeding = models.FloatField()
    medium_weight = models.FloatField()
    biomass = models.FloatField()

class Mortality():
    theoric_percentage = models.FloatField()
    theoric_number = models.IntegerField()
    real_percentage = models.FloatField()
    real_number = models.IntegerField()

class Calibration():
    goes_to = models.IntegerField()
    came_from = models.IntegerField()

class MonthStat(models.Model):
    month_name = models.CharField(max_length=20)
    year = models.IntegerField()
    num_fishes = models.IntegerField()
    medium_weight = models.FloatField()
    biomass = models.FloatField()
    percent_feeding = models.FloatField()
    food_portion = FoodPortion()
    fc = models.FloatField()
    theoric_30_days = Theoric30Days()
    real_30_days = Real30Days()
    mortality = Mortality()
    calibration = Calibration()
    biomass_increase_with_mortality = models.IntegerField(default=None)
    real_fc_with_mortality = models.FloatField()