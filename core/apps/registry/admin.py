from django.contrib import admin
from .models import DayOfWeek, Schedule, Store

# Register your models here.
admin.site.register(DayOfWeek)
admin.site.register(Schedule)
admin.site.register(Store)
