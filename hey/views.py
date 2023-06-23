from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Friend

# Create your views here.

class FriendsView(LoginRequiredMixin, generic.ListView):
    model = Friend

class FriendView(LoginRequiredMixin, generic.DetailView):
    model = Friend