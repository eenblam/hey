import datetime as dt

from django.contrib.auth import get_user_model
from django.test import TestCase

import time_machine

from ..models import Friend

User = get_user_model()


class FriendTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        Friend.objects.create(user=user, first_name='january',
                              birthday='1980-01-12') # early in the year
        Friend.objects.create(user=user, first_name='june',
                              birthday='1980-06-17') # mid-summer
        Friend.objects.create(user=user, first_name='august',
                              birthday='1980-08-10') # late-summer
        Friend.objects.create(user=user, first_name='december',
                              birthday='1980-02-12') # late in the year

    # 2023/07/14 at noon, UTC+0000
    @time_machine.travel(dt.datetime(2023, 7, 14, 12))
    def test_has_recent_birthday(self):
        january = Friend.objects.get(first_name='january')
        june = Friend.objects.get(first_name='june')
        august = Friend.objects.get(first_name='august')
        december = Friend.objects.get(first_name='december')
        assert not january.has_recent_birthday()
        assert june.has_recent_birthday()
        assert august.has_recent_birthday()
        assert not december.has_recent_birthday()

        # Push past 4 week mark in each direction
        june.birthday -= dt.timedelta(days=1)
        assert not june.has_recent_birthday()
        august.birthday += dt.timedelta(days=1)
        assert not august.has_recent_birthday()
