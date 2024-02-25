from django.contrib import admin

from .models import Department, Location, Shift, Schedule, TimeClock

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'longitude', 'latitude')
    search_fields = ('name', 'address')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('day', 'department', 'location', 'start_time', 'end_time', 'max_employees')
    list_filter = ('day', 'department', 'location')
    search_fields = ('department__name', 'location__name')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('user', 'shift', 'date', 'created_at', 'updated_at')
    list_filter = ('user', 'shift', 'date')
    search_fields = ('user__username',)

@admin.register(TimeClock)
class TimeClockAdmin(admin.ModelAdmin):
    list_display = ('user', 'shift', 'clock_in', 'clock_out', 'total_hours')
    list_filter = ('user', 'shift')
    search_fields = ('user__username',)