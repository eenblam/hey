from datetime import date, timedelta

from django.db import models
from django.urls import reverse

# Create your models here.
class Friend(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    first_name = models.TextField() # required
    last_name = models.TextField(blank=True)
    #TODO timezones?
    birthday = models.DateField("birthday", blank=True, null=True)
    #TODO don't want to restrict by char count for internationalization
    phone = models.TextField(blank=True, verbose_name="phone number")
    last_contact = models.DateField(blank=True, null=True)
    status = models.TextField(blank=True)
    group = models.ForeignKey('Group', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.last_name != "":
            return f'{self.first_name} {self.last_name}'
        return self.first_name

    # This will be used automatically by CreateView/UpdateView
    # to redirect after a successful form submission.
    def get_absolute_url(self):
        return reverse('hey:friend-detail', kwargs={'pk': self.pk})

    def get_full_name(self):
        if self.last_name != "":
            return f'{self.first_name} {self.last_name}'
        return self.first_name

    def has_recent_birthday(self):
        if self.birthday is None or self.birthday == "":
            return False

        today = date.today()
        m = timedelta(weeks=4)
        today = today.replace(year=self.birthday.year)
        if abs(today - self.birthday) < m: 
            return True
        return False

    def next_contact(self):
        """Returns the date of the next time this friend is due for contact.

        None if the friend has no group or last_contact.
        """
        if self.last_contact is None or self.last_contact == "" or self.group is None:
            return None
        return self.last_contact + self.group.get_timedelta()

    def is_overdue(self):
        """Returns true if the friend is overdue for contact by end of this week"""
        if self.next_contact() is None:
            return False
        today = date.today()
        weekday = today.weekday()
        end_of_week = today + timedelta(days=6 - weekday)
        return self.next_contact() < end_of_week


class Group(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    frequency = models.PositiveIntegerField(default=1)

    # Unit
    DAY = "D"
    WEEK = "W"
    MONTH = "M"
    UNIT_CHOICES = [(DAY, "day"), (WEEK, "week"), (MONTH, "month")]
    unit = models.TextField(
        max_length = 1,
        choices=UNIT_CHOICES,
        default=WEEK,
    )

    def __str__(self):
        return self.name

    # This will be used automatically by CreateView/UpdateView
    # to redirect after a successful form submission.
    def get_absolute_url(self):
        return reverse('hey:group-detail', kwargs={'pk': self.pk})

    def get_timedelta(self):
        match self.unit:
            case self.DAY:
                return timedelta(days=self.frequency)
            case self.WEEK:
                return timedelta(weeks=self.frequency)
            case self.MONTH:
                # Favor 30 day months
                return timedelta(days=30*self.frequency)
