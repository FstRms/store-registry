from django.contrib import admin
from .models import Schedule, Store, StoreSchedule

# Register your models here.

# admin.site.register(Schedule)


class StoreScheduleInline(admin.StackedInline):
    """Stacked form for Store schedule"""

    model = StoreSchedule
    extra = 0
    can_delete = False


class StoreAdmin(admin.ModelAdmin):
    """Store model with Schedules"""

    model = Store
    inlines = [StoreScheduleInline]


admin.site.register(Schedule)
admin.site.register(Store, StoreAdmin)
