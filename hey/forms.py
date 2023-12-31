from django import forms

from .models import Account, Friend, Group

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['timezone']


class DateInput(forms.DateInput):
    input_type = 'date'

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        # Exclude "user" since we don't want that edited
        fields = ['first_name', 'last_name', 'pronouns',
                  'phone', 'birthday', 'last_contact', 'status', 'group']
        widgets = {
            # We want an `input` instead of a `textarea`
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'pronouns': forms.TextInput(),
            'birthday': DateInput(),
            'phone': forms.TextInput(),
            'last_contact': DateInput(),
            'status': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        """Ensure user can only view and add to their own groups.

        If this wasn't here, the user could see all existing groups in the form,
        or post a request assigning a friend to an arbitrary group.
        This prevents both.
        """
        self.user = kwargs.pop('user')

        super(FriendForm, self).__init__(*args, **kwargs)

        if self.user:
            self.fields['group'].queryset = self.user.group_set.all()
        else:
            raise RuntimeError("User not set")

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        # Exclude "user" since we don't want that edited
        fields = ['name', 'frequency', 'unit']


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

        # Prefetch groups for timedeltas in Friend.is_overdue()
        for friend in Friend.objects.filter(user=self.user).select_related('group'):
            if not friend.is_overdue():
                continue

            self.id_list.append(friend.id)

            last_contact = forms.DateField(
                widget=DateInput(
                    attrs={
                        'data-initial': friend.last_contact,
                        'onchange': 'if (this.dataset.initial != this.value) { this.parentElement.parentElement.classList.add("changed"); } else { this.parentElement.parentElement.classList.remove("changed"); }'
                        }
                ),
                required=False,
                label=friend.get_full_name(),
                initial=friend.last_contact
            )
            last_contact.group = friend.id
            self.fields['last_contact_%s' % friend.id] = last_contact

            status = forms.CharField(
                widget=forms.TextInput(
                    attrs={
                        'data-initial': friend.status,
                        'onchange': 'if (this.dataset.initial != this.value) { this.parentElement.parentElement.classList.add("changed"); } else { this.parentElement.parentElement.classList.remove("changed"); }'
                        }
                ),
                required=False,
                label="Status:",
                initial=friend.status
            )
            status.group = friend.id
            self.fields['status_%s' % friend.id] = status

    def get_context(self, **kwargs):
        context = super(CheckinsForm, self).get_context(**kwargs)
        fields = {}
        for bound_field in context['fields']:
            f = bound_field[0]
            fields[f.id_for_label.lstrip('id_')] = f

        data = [{
                'last_contact': fields[f'last_contact_{x}'],
                'status': fields[f'status_{x}']
                } for x in self.id_list]
        context['subforms'] = data
        return context
