from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.urls import reverse_lazy
from django.views import generic

from ..forms import GroupForm
from ..models import Group

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
