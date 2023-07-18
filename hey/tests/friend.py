import datetime as dt

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

import time_machine

from ..cache import delete_user_tz
from ..models import Friend, Group

User = get_user_model()


class FriendTestCase(TestCase):
    # 2023/07/14 at noon, UTC+0000
    TODAY = dt.datetime(2023, 7, 14, 12)
    TOMORROW_MORNING_3AM_UTC = dt.datetime( 2023, 7, 15, 3)
    TZ_GMT = timezone.get_fixed_timezone(dt.timedelta(hours=0))
    TZ_PST = timezone.get_fixed_timezone(dt.timedelta(hours=-7))

    def setUp(self):
        user = User.objects.create(username='testuser')

        # For has_recent_birthday
        Friend.objects.create(user=user, first_name='january',
                              birthday='1980-01-12') # early in the year
        Friend.objects.create(user=user, first_name='june',
                              birthday='1980-06-17') # mid-summer
        Friend.objects.create(user=user, first_name='august',
                              birthday='1980-08-10') # late-summer
        Friend.objects.create(user=user, first_name='december',
                              birthday='1980-02-12') # late in the year

        # For is_overdue
        user_is_overdue = User.objects.create(username='user_is_overdue')
        group_semidaily = Group.objects.create(user=user, name='semidaily',
                                     frequency=2, unit=Group.DAY)
        group_weekly = Group.objects.create(user=user, name='weekly',
                                     frequency=1, unit=Group.WEEK)
        group_monthly = Group.objects.create(user=user, name='monthly',
                                     frequency=1, unit=Group.MONTH)
        Friend.objects.create(user=user_is_overdue,
                              first_name='lastyear_nogroup',
                              last_contact='2022-07-14')
        Friend.objects.create(user=user_is_overdue, group=group_monthly,
                              first_name='lastmonth_monthly',
                              last_contact='2023-06-17') # 17. See test__is_overdue_week
        Friend.objects.create(user=user_is_overdue, group=group_semidaily,
                              first_name='lastweek_semidaily',
                              last_contact='2023-07-07')
        Friend.objects.create(user=user_is_overdue, group=group_weekly,
                              first_name='lastweek_weekly',
                              last_contact='2023-07-08') # 08. See test__is_overdue_week
        Friend.objects.create(user=user_is_overdue, group=group_semidaily,
                              first_name='two days ago',
                              last_contact='2023-07-12')
        Friend.objects.create(user=user_is_overdue, group=group_semidaily,
                              first_name='yesterday',
                              last_contact='2023-07-13')
        Friend.objects.create(user=user_is_overdue, group=group_semidaily,
                              first_name='today',
                              last_contact='2023-07-14')

    @time_machine.travel(TODAY)
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

    @time_machine.travel(TODAY)
    def test__is_overdue_no_group(self):
        """Test that an ungrouped Friend isn't overdue even a year out of date."""
        lastyear = Friend.objects.get(first_name='lastyear_nogroup')
        assert not lastyear._is_overdue(self.TZ_GMT)

    @time_machine.travel(TODAY)
    def test__is_overdue_day_UTC(self):
        """Test that _is_overdue works in UTC+0000.

        is_overdue() is cache-dependent and not thread-safe for deterministic testing,
        so it should be tested separately with cache-specific code.
        """
        lastweek = Friend.objects.get(first_name='lastweek_semidaily')
        twodays = Friend.objects.get(first_name='two days ago')
        yesterday = Friend.objects.get(first_name='yesterday')
        today = Friend.objects.get(first_name='today')

        assert lastweek._is_overdue(self.TZ_GMT)
        assert twodays._is_overdue(self.TZ_GMT)
        assert not yesterday._is_overdue(self.TZ_GMT)
        assert not today._is_overdue(self.TZ_GMT)

    @time_machine.travel(TOMORROW_MORNING_3AM_UTC)
    def test__is_overdue_day_PST(self):
        """Test that _is_overdue works in Pacific Standard Time.

        Specifically, we check that, when PST and GMT have different dates,
        _is_overdue still works in PST.
        """
        lastweek = Friend.objects.get(first_name='lastweek_semidaily')
        twodays = Friend.objects.get(first_name='two days ago')
        yesterday = Friend.objects.get(first_name='yesterday')
        today = Friend.objects.get(first_name='today')

        assert lastweek._is_overdue(self.TZ_PST)
        assert twodays._is_overdue(self.TZ_PST)
        assert not yesterday._is_overdue(self.TZ_PST)
        assert not today._is_overdue(self.TZ_PST)


    @time_machine.travel(TODAY)
    def test__is_overdue_week(self):
        """Test that week/month cadences are overdue if they expire this week.

        TODAY is Friday, so if talked to lastweek on Saturday,
        they should be overdue since their next_contact() occurs
        before the end of this week. Similar for lastmonth.
        """

        lastmonth = Friend.objects.get(first_name='lastmonth_monthly')
        lastweek = Friend.objects.get(first_name='lastweek_weekly')
        assert lastmonth._is_overdue(self.TZ_GMT)
        assert lastweek._is_overdue(self.TZ_GMT)

        # Push them from Saturday to Monday. They should no longer be overdue.
        lastmonth.last_contact += dt.timedelta(days=2)
        lastweek.last_contact += dt.timedelta(days=2)
        print(lastmonth.last_contact)
        assert not lastmonth._is_overdue(self.TZ_GMT)
        assert not lastweek._is_overdue(self.TZ_GMT)
