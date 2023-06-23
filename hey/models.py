from django.db import models

# Create your models here.
class Friend(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    birthday = models.DateTimeField("birthday")
    #TODO don't want to restrict by char count for internationalization
    phone = models.TextField()
