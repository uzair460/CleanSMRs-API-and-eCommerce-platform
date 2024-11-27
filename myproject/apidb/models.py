from django.db import models

class WeatherData(models.Model):
    date = models.DateField()  # ISO 8601 format: YYYY-MM-DD
    time = models.TimeField()  # ISO 8601 format: hh:mm:ss
    timezone_offset = models.CharField(max_length=10)  # e.g., UTC-10:00
    latitude = models.FloatField()
    longitude = models.FloatField()
    water_temperature = models.FloatField()
    ambient_air_temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()
    precipitation = models.FloatField()
    haze = models.FloatField()
    becquerel = models.FloatField()

    def __str__(self):
        return f"{self.date} {self.time}"
