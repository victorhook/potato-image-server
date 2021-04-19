from django.db import models

# Create your models here.
class Sensor(models.Model):
    temperature = models.FloatField()
    moisture = models.IntegerField()

class Sample(models.Model):
    date = models.DateTimeField(primary_key=True)
    temperature = models.FloatField(blank=True, null=True)
    pressure = models.IntegerField(blank=True, null=True)
    humidity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sample'