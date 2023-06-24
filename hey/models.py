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
    phone = models.TextField(blank=True)

    def __str__(self):
        if self.last_name != "":
            return f'{self.first_name} {self.last_name}'
        return self.first_name

    # This will be used automatically by CreateView/UpdateView
    # to redirect after a successful form submission.
    def get_absolute_url(self):
        return reverse('hey:friend-detail', kwargs={'pk': self.pk})