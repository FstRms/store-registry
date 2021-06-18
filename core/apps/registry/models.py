from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class DateTimeTag(models.Model):
    """Base model with create and update fields."""

    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Set"""

        abstract = True


class DayOfWeek(models.Model):
    name = models.CharField(_("name"), max_length=50)

    def __str__(self):
        """Show label on admin"""
        return self.name

    @property
    def day_code(self):
        """Gets 'day of week code' to compare agains datetime module"""
        if self.pk < 7:
            code = self.pk - 1
        else:
            code = 6
        return code

    class Meta:
        """Set verbose names"""

        verbose_name = _("Day of week")
        verbose_name_plural = _("Days of week")


class Schedule(DateTimeTag):
    """Model to store working hours"""

    start_day = models.ForeignKey(
        DayOfWeek,
        related_name="start_day",
        verbose_name=_("start day"),
        on_delete=models.CASCADE,
    )
    end_day = models.ForeignKey(
        DayOfWeek,
        verbose_name=_("end day"),
        related_name="end_day",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    start_time = models.TimeField(_("start_time"), auto_now=False, auto_now_add=False)
    end_time = models.TimeField(_("end_time"), auto_now=False, auto_now_add=False)

    @property
    def short_name(self):
        """Get short name"""
        if self.end_day:
            return f"{self.start_day.name[0:3]} - {self.end_day.name[0:3]}: {self.start_time} - {self.end_time}"
        else:
            return f"{self.start_day.name[0:3]}: {self.start_time} - {self.end_time}"

    @property
    def day_range(self):
        """Gets all days in between the schedule."""
        if self.start_day.day_code == 6 and self.end_day.day_code == 0:
            days = range(0, 7)
            return list(days)
        elif self.start_day.day_code == 6:
            days = range(0, self.end_day.day_code + 1)
            days_list = list(days)
            days_list.append(6)
            return days_list
        else:
            days = range(self.start_day.day_code, self.end_day.day_code + 1)
            return list(days)

    def __str__(self):
        """Show label on admin"""
        return self.short_name

    class Meta:
        """Set verbose names"""

        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")


class Store(DateTimeTag):
    """Model related to a Store"""

    name = models.CharField(max_length=40, verbose_name=_("Store Name"))

    def __str__(self):
        """Show label on admin"""
        return self.name

    class Meta:
        """Set verbose names"""

        verbose_name = _("Store")
        verbose_name_plural = _("Stores")


class StoreSchedule(DateTimeTag):
    """Intermediary model for the many-to-many relation."""

    store = models.ForeignKey(Store, verbose_name=_("store"), on_delete=models.CASCADE)
    schedule = models.ManyToManyField(Schedule, verbose_name=_("schedule"))

    def __str__(self):
        """Show label on admin"""
        return self.store.name

    class Meta:
        """Set verbose names"""

        verbose_name = _("Store Schedule")
        verbose_name_plural = _("Stores Schedule")
