
"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'hey'

urlpatterns = [
    path('', views.CheckinsView.as_view(), name='checkins'),
    path('friends/', views.FriendsView.as_view(), name='friends'),
    path('friends/add/', views.FriendCreateView.as_view(), name='friend-add'),
    path('friends/<int:pk>/', views.FriendView.as_view(), name='friend-detail'),
    path('friends/<int:pk>/delete', views.FriendDeleteView.as_view(), name='friend-delete'),
    path('friends/<int:pk>/update', views.FriendUpdateView.as_view(), name='friend-update'),
    path('groups/', views.GroupsView.as_view(), name='groups'),
    path('groups/add/', views.GroupCreateView.as_view(), name='group-add'),
    path('groups/<int:pk>/', views.GroupView.as_view(), name='group-detail'),
    path('groups/<int:pk>/delete', views.GroupDeleteView.as_view(), name='group-delete'),
    path('groups/<int:pk>/update', views.GroupUpdateView.as_view(), name='group-update'),
]
