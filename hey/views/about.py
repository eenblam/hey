from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

class AboutView(generic.TemplateView):
    def get(self, request, **kwargs):
        return render(request, "hey/about.html")
