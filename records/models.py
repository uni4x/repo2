# mealtracker/records/models.py

from django.db import models

class MealRecord(models.Model):
    date = models.DateField()
    breakfast = models.TextField(blank=True, null=True)
    lunch = models.TextField(blank=True, null=True)
    dinner = models.TextField(blank=True, null=True)
    snack = models.TextField(blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date}の記録"