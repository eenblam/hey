from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.urls import reverse_lazy
from django.views import generic

from ..cache import delete_user_tz
from ..forms import AccountForm
from ..models import Account

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

    def form_valid(self, form):
        # purge timezone from cache if changed
        if 'timezone' in form.changed_data:
            delete_user_tz(self.request.user)
        return super().form_valid(form)


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
