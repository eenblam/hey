from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.views import generic

from ..forms import FriendForm
from ..models import Account, Friend, Group

User = get_user_model()

class FriendsView(LoginRequiredMixin, generic.ListView):
    model = Friend

    def get_queryset(self):
        # We want to sort by group, but always put None/Null at the end.
        # We also need to sort into group in advance so that the template can regroup by group.
        return Friend.objects.filter(user=self.request.user).order_by(
            F('group__unit').asc(nulls_last=True),
            F('group__frequency').asc(nulls_last=True),
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

    def get_form_kwargs(self):
        """Pass user to form."""
        kwargs = super(FriendCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


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

    def get_form_kwargs(self):
        """Pass user to form."""
        kwargs = super(FriendUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class FriendDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Friend
    success_url = reverse_lazy("hey:friends")
