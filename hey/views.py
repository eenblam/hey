from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

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
    fields = ['first_name', 'last_name', 'birthday', 'phone']

    def form_valid(self, form):
        # Link Friend to user
        form.instance.user = self.request.user
        return super().form_valid(form)