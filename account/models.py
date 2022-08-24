from django.db import models

# Create your models here.


class CityWeather(models.Model):
    
    city_key = models.CharField(max_length=16)
    city_name = models.CharField(max_length=100)
    forecast_date = models.DateTimeField(null=True, blank=True)
    headline = models.TextField()
    temperature_min_val = models.FloatField()
    temperature_min_unit = models.CharField(max_length = 8)
    temperature_max_val = models.FloatField()
    temperature_max_unit = models.CharField(max_length = 8)
    day_conditions = models.CharField(max_length=100)
    day_precipitation = models.BooleanField(default = False)
    night_conditions = models.CharField(max_length=100)
    night_precipitation = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
