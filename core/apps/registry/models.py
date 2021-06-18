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
        """Get shor name"""
        if self.end_day:
            return f"{self.start_day.name[0:3]} - {self.end_day.name[0:3]}: {self.start_time} - {self.end_time}"
        else:
            return f"{self.start_day.name[0:3]}: {self.start_time} - {self.end_time}"

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
    schedule = models.ManyToManyField(Schedule, verbose_name=_("schedule"))

    def __str__(self):
        """Show label on admin"""
        return self.name

    class Meta:
        """Set verbose names"""

        verbose_name = _("Store")
        verbose_name_plural = _("Stores")
