from django.contrib import admin

from .models import Position, Location, Shift, Schedule, TimeClock, Employee,Organization


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'longitude', 'latitude')
    search_fields = ('name', 'address')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start_time', 'end_time', 'hours','organization')
    list_filter = ('organization', 'hours')
    search_fields = ('start_time', 'end_time', 'organization__name')



@admin.register(TimeClock)
class TimeClockAdmin(admin.ModelAdmin):
    list_display = ('employee', 'schedule', 'clock_in', 'clock_out', 'total_hours')
    list_filter = ('employee', 'schedule')
    search_fields = ('employee__user__username',)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('employee', 'shift', 'date')
    list_filter = ('employee', 'employee__organization')
    search_fields = ('employee__user__username',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('employee', 'shift', 'employee__organization')

    def weekly_schedule(self, obj):
        # Assuming employee's ID is stored in obj.user_id
        weekly_schedule = Schedule.objects.get_weekly_schedule(obj.user_id, obj.date)
        return ", ".join([str(schedule) for schedule in weekly_schedule])

    def daily_schedule(self, obj):
        # Assuming employee's ID is stored in obj.user_id
        daily_schedule = Schedule.objects.get_daily_schedule(obj.user_id, obj.date)
        return ", ".join([str(schedule) for schedule in daily_schedule])

    weekly_schedule.short_description = "Weekly Schedule"
    daily_schedule.short_description = "Daily Schedule"


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin')
    search_fields = ('name', 'admin__username')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position','organization')
    list_filter = ('position', 'organization')
    search_fields = ('user__username', 'position','organization')

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Schedule, ScheduleAdmin)