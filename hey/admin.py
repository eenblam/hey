from django.contrib import admin

from .models import Account, Friend, Group

admin.site.register(Account)
admin.site.register(Friend)
admin.site.register(Group)
