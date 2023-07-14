from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from ..forms import CheckinsForm
from ..models import Friend

User = get_user_model()

class CheckinsView(LoginRequiredMixin, generic.TemplateView):
    def get(self, request, **kwargs):
        form = CheckinsForm(user=request.user)
        return render(request, "hey/checkins.html", {'form': form.get_context()})

    def post(self, request, **kwargs):
        form = CheckinsForm(data=request.POST, user=request.user)
        if not form.is_valid():
            return HttpResponse(status=400)

        try: # Get list of friend ids to filter results by
            friend_ids = [int(friend_id.strip('last_contact_'))
                        for friend_id, _ in form.cleaned_data.items()
                        if friend_id.startswith('last_contact_')] # don't add id again for other fields
        except ValueError: # friend_id wasn't an int => bad request, abort
            return HttpResponse(status=400)

        #TODO enforce maximum number of friends updated at once

        changed_friends = []
        friends = Friend.objects.filter(pk__in=friend_ids)
        for f in friends:
            try:
                last_contact = form.cleaned_data[f'last_contact_{f.id}']
                status = form.cleaned_data[f'status_{f.id}']
            except KeyError:
                continue
            if f.last_contact == last_contact and f.status == status:
                continue
            f.last_contact = last_contact
            f.status = status
            changed_friends.append(f)

        Friend.objects.bulk_update(changed_friends, ['last_contact', 'status'])

        print(f'Updated {len(changed_friends)} friends for user {request.user.id} ({request.user})')
        return HttpResponseRedirect(reverse_lazy("hey:checkins"))
