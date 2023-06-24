from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import FriendForm
from .models import Friend

# Create your views here.

class FriendsView(LoginRequiredMixin, generic.ListView):
    model = Friend

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)

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


class FriendUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Friend
    form_class = FriendForm


class FriendDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Friend
    success_url = reverse_lazy("hey:friends")