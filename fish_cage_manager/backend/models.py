from django.db import models

cage_counter = 0


class Cage(models.Model):
    cage_id = models.IntegerField(primary_key=True, default=1)


class FoodPortion(models.Model):
    kg = models.FloatField()
    bags = models.FloatField()
    total_30_days = models.FloatField()


class Theoric30Days(models.Model):
    biomass_increase = models.FloatField()
    biomass_total = models.FloatField()
    medium_weight = models.FloatField()


class Real30Days(models.Model):
    feeding = models.FloatField()
    medium_weight_with_real_feeding = models.FloatField()
    medium_weight = models.FloatField()
    biomass = models.FloatField()


class Mortality(models.Model):
    theoric_percentage = models.FloatField()
    theoric_number = models.IntegerField()
    real_percentage = models.FloatField()
    real_number = models.IntegerField()


class Calibration(models.Model):
    goes_to = models.IntegerField()
    came_from = models.IntegerField()


class MonthStat(models.Model):
    cage = models.ForeignKey(Cage, on_delete=models.CASCADE)
    month_name = models.CharField(max_length=20)
    year = models.IntegerField()
    num_fishes = models.IntegerField()
    medium_weight = models.FloatField()
    biomass = models.FloatField()
    percent_feeding = models.FloatField()
    fc = models.FloatField()
    biomass_increase_with_mortality = models.IntegerField(default=None)
    real_fc_with_mortality = models.FloatField()

    food_portion = models.OneToOneField(
        FoodPortion,
        on_delete=models.CASCADE,
    )

    theoric_30_days = models.OneToOneField(
        Theoric30Days,
        on_delete=models.CASCADE,
    )

    real_30_days = models.OneToOneField(
        Real30Days,
        on_delete=models.CASCADE,
    )

    mortality = models.OneToOneField(
        Mortality,
        on_delete=models.CASCADE,
    )

    calibration = models.OneToOneField(
        Calibration,
        on_delete=models.CASCADE,
    )
