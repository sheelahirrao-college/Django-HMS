from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Hotel


class HotelRegistrationForm(UserCreationForm):

    class Meta:
        model = Hotel
        fields = ('name', 'contact', 'user')


class HotelLoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Hotel
        fields = ('user',)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Invalid Login")

