from django import forms

from .models import Friend

class DateInput(forms.DateInput):
    input_type = 'date'

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        # Exclude "user" since we don't want that edited
        fields = ['first_name', 'last_name',
                  'phone', 'birthday', 'last_contact']
        widgets = {
            # We want an `input` instead of a `textarea`
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'birthday': DateInput(),
            'phone': forms.TextInput(),
            'last_contact': DateInput(),
        }

class CheckinsForm(forms.Form):
    """
    Form for checking in on friends.
    This is meant to be a helpful page to view, not just for updates.
    """
    def __init__(self, user, *args, **kwargs):
        # Initialize before touching self.fields
        super(CheckinsForm, self).__init__(*args, **kwargs)

        self.user = user
        self.id_list = []

        for friend in Friend.objects.filter(user=self.user):
            self.id_list.append(friend.id)
            self.fields['last_contact_%s' % friend.id] = forms.DateField(
                widget=DateInput(
                    attrs={
                        'data-initial': friend.last_contact,
                        'onchange': 'if (this.dataset.initial != this.value) { this.parentElement.classList.add("changed"); } else { this.parentElement.classList.remove("changed"); }'
                        }
                ),
                required=False,
                label=friend.get_full_name(),
                initial=friend.last_contact
            )