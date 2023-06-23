from django.shortcuts import render
from django.views import generic

from .models import Friend

# Create your views here.

class FriendsView(generic.ListView):
    model = Friend

class FriendView(generic.DetailView):
    model = Friend