from django.db import models

# Create your models here.
class YourModel(models.Model):
    country_name = models.CharField(max_length=100)
    year = models.IntegerField()
    gdp_value = models.DecimalField(max_digits=20, decimal_places=2)
    gdp_growth = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.country_name} - {self.year}"