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