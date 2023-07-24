import datetime as dt

from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.test import Client, TestCase

import time_machine

from ..forms import CheckinsForm
from ..models import Friend, Group

User = get_user_model()

class CheckinsTest(TestCase):
    TODAY = dt.datetime(2023, 7, 14, 12)
    USERNAME = 'checkins_test'
    PASSWORD = 'coffeeteaacuporthree'
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username=self.USERNAME, password=self.PASSWORD)
        group = Group.objects.create(user=self.user, name='semidaily',
                                     frequency=2, unit=Group.DAY)
        # Today. Shouldn't show.
        Friend.objects.create(user=self.user, group=group,
                              first_name='dailyfriend1',
                              last_contact='2023-07-14')
        # Yesterday. Shouldn't show.
        Friend.objects.create(user=self.user, group=group,
                              first_name='dailyfriend2',
                              last_contact='2023-07-13')
        Friend.objects.create(user=self.user, group=group,
                              first_name='dailyfriend3',
                              last_contact='2023-07-12')
        Friend.objects.create(user=self.user, group=group,
                              first_name='dailyfriend4',
                              last_contact='2023-07-11')

    #TODO test form errors
    # https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.SimpleTestCase.assertFormError

    @time_machine.travel(TODAY)
    def test_checkins_form(self):
        c = self.client
        login = c.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(login)

        response = c.get('/')
        self.assertContains(response=response,
                            text='dailyfriend3',
                            status_code=200)
        self.assertContains(response=response, text='dailyfriend4')
        # Today and yesterday don't show
        self.assertNotContains(response=response, text='dailyfriend1')
        self.assertNotContains(response=response, text='dailyfriend2')

        friend3 = Friend.objects.get(first_name='dailyfriend3')
        friend4 = Friend.objects.get(first_name='dailyfriend4')

        # Update friend3 (re-use friend4's data)
        post_response = c.post("/", data={
                                   f"last_contact_{friend3.id}": "2023-07-14",
                                   f"status_{friend3.id}": "had a chat",
                                   f"last_contact_{friend4.id}": '2023-07-11',
                                   f"status_{friend4.id}": '',
                                })

        # Check status and redirect
        self.assertEqual(302, post_response.status_code)
        location = post_response.get('location')
        self.assertEqual('/', location)
        # Checkins form should now contain only one friend
        response = c.get(location)
        print(response.content)
        self.assertContains(response=response, text='dailyfriend4', status_code=200)
        # Missing now that friend has been updated
        self.assertNotContains(response=response, text='dailyfriend3')
