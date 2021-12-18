# Django
from django.db import models
from django.utils import timezone

# Utils
import math

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self):
        """ Return a matrix filled of booleans with the "standard distribution" 
        in a vehicle, from top to bottom and left to right.
        a Vehicle can have "n" rows with a maximum of 2 passengers per row.
        the rows number depends on the vehicle max capacity."""

        seats_rows = math.ceil(self.vehicle_type.max_capacity / 2)
        distribution = [[True, True] for row in range(seats_rows)]
        
        if self.passengers % 2 > 0:
            distribution[-1][-1] = False
        
        return distribution

                


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"
    
    def is_finished(self):
        """ Return True if today's date is greater or equal than the end of 
        the journey. """
        if self.end:
            return True if timezone.now().date() >= self.end else False
        else:
            return False
        
