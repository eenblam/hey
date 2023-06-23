from django.db import models

# Create your models here.
class Friend(models.Model):
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
