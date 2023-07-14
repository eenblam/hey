from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.models import Session
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import AccountForm, CheckinsForm, FriendForm, GroupForm
from .models import Account, Friend, Group

User = get_user_model()

class AccountView(LoginRequiredMixin, generic.DetailView):
    model = Account

    def get_object(self):
        return Account.objects.get(user=self.request.user)


class AccountUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Account
    form_class = AccountForm

    def get_object(self):
        """Fetch user, assuming pk isn't being provided by urlconf"""
        account = Account.objects.get(user=self.request.user)
        return account


class AccountDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Account
    # Doesn't exactly matter - it'll just redirect the user to Login.
    success_url = reverse_lazy("signup")

    def get_object(self):
        """Fetch user, assuming pk isn't being provided by urlconf"""
        account = Account.objects.get(user=self.request.user)
        return account

    def form_valid(self, form):
        """Log user out before deleting"""
        try:
            #user = User.objects.get(id=self.request.user)
            user = self.request.user
            # https://stackoverflow.com/questions/953879/how-to-force-a-user-logout-in-django
            # Lock out
            user.is_active = False
            user.save()
            # Revoke sessions
            # This is tied to using database-backed sessions, which is perhaps not what's best long-term
            [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
            # Finally, delete
            user.delete()
        except User.DoesNotExist:
            pass

        return super().form_valid(form)


class FriendsView(LoginRequiredMixin, generic.ListView):
    model = Friend

    def get_queryset(self):
        # We want to sort by group, but always put None/Null at the end.
        return Friend.objects.filter(user=self.request.user).order_by(
            F('group__name').asc(nulls_last=True),
            F('last_contact').asc(nulls_last=True))

class FriendView(LoginRequiredMixin, generic.DetailView):
    model = Friend

    def get_object(self):
        return Friend.objects.get(user=self.request.user, pk=self.kwargs['pk'])

class FriendCreateView(LoginRequiredMixin, generic.CreateView):
    model = Friend
    form_class = FriendForm

    def form_valid(self, form):
        # Link Friend to user
        form.instance.user = self.request.user
        return super().form_valid(form)


@receiver(post_save, sender=User)
def bootstrap_new_user(sender, **kwargs):
    if kwargs.get('created', False):
        user = kwargs['instance']
        Account.objects.create(user=user) # use default timezone
        Group.objects.bulk_create([
            Group(name="Besties", frequency = 2, unit = Group.DAY, user=user),
            Group(name="Close Friends", frequency = 1, unit = Group.WEEK, user=user),
            Group(name="Friends", frequency = 1, unit = Group.MONTH, user=user)
        ])


class FriendUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Friend
    form_class = FriendForm


class FriendDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Friend
    success_url = reverse_lazy("hey:friends")


class CheckinsView(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, **kwargs):
        form = CheckinsForm(user=request.user)
        return render(request, "hey/checkins.html", {'form': form.get_context()})

    def post(self, request, **kwargs):
        form = CheckinsForm(data=request.POST, user=request.user)
        if not form.is_valid():
            return HttpResponse(status=400)

        try: # Get list of friend ids to filter results by
            friend_ids = [int(friend_id.strip('last_contact_'))
                        for friend_id, _ in form.cleaned_data.items()
                        if friend_id.startswith('last_contact_')] # don't add id again for other fields
        except ValueError: # friend_id wasn't an int => bad request, abort
            return HttpResponse(status=400)

        #TODO enforce maximum number of friends updated at once

        changed_friends = []
        friends = Friend.objects.filter(pk__in=friend_ids)
        for f in friends:
            try:
                last_contact = form.cleaned_data[f'last_contact_{f.id}']
                status = form.cleaned_data[f'status_{f.id}']
            except KeyError:
                continue
            if f.last_contact == last_contact and f.status == status:
                continue
            f.last_contact = last_contact
            f.status = status
            changed_friends.append(f)

        Friend.objects.bulk_update(changed_friends, ['last_contact', 'status'])

        print(f'Updated {len(changed_friends)} friends for user {request.user.id} ({request.user})')
        return HttpResponseRedirect(reverse_lazy("hey:checkins"))

class GroupsView(LoginRequiredMixin, generic.ListView):
    model = Group

    def get_queryset(self):
        # Order groups by (unit, frequency, name)
        #TODO 8 days sorts before 1 week at present
        return Group.objects.filter(user=self.request.user).order_by(
            F('unit').asc(),
            F('frequency').asc(),
            'name')

class GroupView(LoginRequiredMixin, generic.DetailView):
    model = Group

    def get_object(self):
        return Group.objects.get(user=self.request.user, pk=self.kwargs['pk'])

class GroupCreateView(LoginRequiredMixin, generic.CreateView):
    model = Group
    form_class = GroupForm

    def form_valid(self, form):
        # Link Group to user
        form.instance.user = self.request.user
        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Group
    form_class = GroupForm


class GroupDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Group
    success_url = reverse_lazy("hey:groups")
