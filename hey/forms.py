from django import forms

from .models import Friend

class DateInput(forms.DateInput):
    input_type = 'date'

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['first_name', 'last_name', 'birthday', 'phone']
        widgets = {
            'birthday': DateInput()
        }