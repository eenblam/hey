from django import forms

from .models import Friend

class DateInput(forms.DateInput):
    input_type = 'date'

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['first_name', 'last_name', 'phone', 'birthday']
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'birthday': DateInput(),
            'phone': forms.TextInput()
        }