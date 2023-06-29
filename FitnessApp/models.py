from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Food(models.Model):
    
    name = models.CharField(max_length=100)
    carbs = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    fats = models.FloatField(blank=True, null=True) 
    calories = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Consumption(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    food_consumed = models. ForeignKey(Food,on_delete=models.CASCADE)

class Bmi(models.Model):
    height_in_metres = models.FloatField(blank=True, null=True)
    weight_in_kg = models.FloatField(blank=True, null=True)
    date_measured = models.DateField()

    def __str__(self):
        return self.weight_in_kg / self.height_in_metres ** 2
    
    


