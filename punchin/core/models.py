from django.db import models
from datetime import timedelta, datetime
from django.utils.timezone import now
from django.contrib.auth.models import User

class Organization(models.Model):
    name = models.CharField(max_length=100)
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_of')

    def __str__(self):
        return self.name
    
class Position(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField( null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='positions')


    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='employees')
    avatar = models.ImageField(upload_to='employees/avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    address = models.CharField(blank=True, max_length=255)
    primary_color = models.CharField(blank=True, max_length=25)
    secondary_color = models.CharField(blank=True, max_length=25)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=15.00)
    overtime_hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=22.50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} employee of - {self.organization}"



class Location(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Shift(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    hours = models.IntegerField(null=True, blank=True)
    extra_hours = models.IntegerField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    note = models.TextField(blank=True, max_length=255, null=True)


    def save(self, *args, **kwargs):
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        
        # Handle cases where end time is before start time (e.g., overnight shifts)
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)  # Add one day to end time
        
        duration = end_datetime - start_datetime
        self.hours = round(duration.total_seconds() / 3600)
       
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.hours} hrs shift ({self.start_time} - {self.end_time})"


class ScheduleManager(models.Manager):
    def get_weekly_schedule(self, employee, start_date):
        end_date = start_date + timedelta(days=6)
        return self.filter(employee=employee, shift__day__range=[start_date, end_date])

    def get_daily_schedule(self, employee, date):
        return self.filter(employee=employee, shift__day=date)

class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="schedules")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ScheduleManager()

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee} - {self.shift}"
        

class TimeClock(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    total_hours = models.IntegerField( null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.clock_out is not None:
            duration = self.clock_out - self.clock_in
            self.total_hours = abs(round(duration.total_seconds() / 3600))
        else:
            # If clock-out time is not set, calculate the total hours based on the current time
            now_time = now()
            duration = now_time - self.clock_in
            self.total_hours = abs(round(duration.total_seconds() / 3600))

        super().save(*args, **kwargs)
    class Meta:
        ordering = ['clock_in']

    
    def __str__(self):
        return f"{self.employee} - Clock In: {self.clock_in}, Clock Out: {self.clock_out} ({self.total_hours} hrs)"
