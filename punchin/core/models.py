from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField( null=True, blank=True)
    # Other department-related fields

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    # Other location-related fields

    def __str__(self):
        return self.name

class Shift(models.Model):
    day = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_employees = models.PositiveIntegerField(null=True, blank=True)
    # Other shift-related fields

    def __str__(self):
        return f"{self.day} ( {self.start_time} - {self.end_time}) at {self.location}"


class ScheduleManager(models.Manager):
    def get_weekly_schedule(self, employee, start_date):
        end_date = start_date + timedelta(days=6)
        return self.filter(employee=employee, shift__day__range=[start_date, end_date])

    def get_daily_schedule(self, employee, date):
        return self.filter(employee=employee, shift__day=date)

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ScheduleManager()
    # Other schedule-related fields

    class Meta:
        unique_together = ('user', 'shift', 'date')

    def __str__(self):
        return f"{self.user} - {self.shift} "
        

class TimeClock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # Other timeclock-related fields

    class Meta:
        ordering = ['clock_in']