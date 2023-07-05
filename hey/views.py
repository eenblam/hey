from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import FriendForm, CheckinsForm
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


class CheckinsView(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, **kwargs):
        form = CheckinsForm(user=request.user)
        return render(request, "hey/checkins.html", {'form': form})

    def post(self, request, **kwargs):
        form = CheckinsForm(data=request.POST, user=request.user)
        if not form.is_valid():
            return HttpResponse(status=400)

        friends = []
        for k,v in form.cleaned_data.items():
            if not k.startswith('last_contact_'):
                continue
            try:
                friend_id = int(k.lstrip('last_contact_'))
                friend = Friend.objects.get(pk=friend_id, user=request.user)
                # Only bulk update on change
                if friend.last_contact != v:
                    friend.last_contact = v
                    friends.append(friend)
            except ValueError: # friend_id wasn't an int => bad request, abort
                return HttpResponse(status=400)
            except Friend.DoesNotExist: # user has no such friend => bad request, abort
                return HttpResponse(status=400)

        Friend.objects.bulk_update(friends, ['last_contact'])

        print(f'Updated {len(friends)} friends for user {request.user.id} ({request.user})')
        return HttpResponseRedirect(reverse_lazy("hey:checkins"))