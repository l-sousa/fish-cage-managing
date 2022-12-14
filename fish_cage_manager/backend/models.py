from django.db import models

cage_counter = 0


class Cage(models.Model):
    cage_id = models.IntegerField(primary_key=True, default=1)


class MonthStat(models.Model):
    cage = models.ForeignKey(Cage, on_delete=models.CASCADE)
    year = models.IntegerField()
    month_name = models.CharField(max_length=20)
    temperature = models.FloatField()
    num_fishes = models.IntegerField()
    medium_weight = models.FloatField()
    biomass = models.FloatField()
    percent_feeding = models.FloatField()

    # food_portion
    food_portion_kg = models.FloatField()
    food_portion_bags = models.FloatField()
    food_portion_total_30_days = models.FloatField()

    fc = models.FloatField()

    # theoric_30_days
    theoric_30_days_biomass_increase = models.FloatField()
    theoric_30_days_biomass_total = models.FloatField()
    theoric_30_days_medium_weight = models.FloatField()

    theoric_medium_weight_with_real_feeding = models.FloatField()

    # real_30_days
    real_30_days_feeding = models.FloatField()
    real_30_days_medium_weight_with_real_feeding = models.FloatField()
    real_30_days_real_medium_weight = models.FloatField()
    real_30_days_biomass = models.FloatField()

    # mortality
    mortality_theoric_percentage = models.FloatField()
    mortality_theoric_number = models.FloatField()
    mortality_real_percentage = models.FloatField()
    mortality_real_number = models.FloatField()


    #calibration
    calibration_goes_to = models.IntegerField()
    calibration_came_from = models.IntegerField()

    biomass_increase_with_mortality = models.IntegerField(default=0)
    real_fc_with_mortality = models.FloatField(default=0)







