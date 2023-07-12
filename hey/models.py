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

class Group(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    frequency = models.PositiveIntegerField(default=1)

    # Unit
    WEEK = "W"
    MONTH = "M"
    UNIT_CHOICES = [(WEEK, "Week"), (MONTH, "Month")]
    unit = models.TextField(
        max_length = 1,
        choices=UNIT_CHOICES,
        default=WEEK,
    )

    # This will be used automatically by CreateView/UpdateView
    # to redirect after a successful form submission.
    def get_absolute_url(self):
        return reverse('hey:group-detail', kwargs={'pk': self.pk})
