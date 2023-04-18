from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin import widgets
from .models import User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name",
                  "last_name", "designation", "gender", "address", "phone_number")


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True},),
            'designation': forms.TextInput(attrs={'readonly': True},),
        }
        fields = ("username", "email", "first_name","last_name", "designation", "gender", "address", "phone_number")

class EditProfileAdminForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True},),
            'designation': forms.TextInput(attrs={'readonly': True},),
        }
        fields = ("username", "email", "first_name","last_name", "designation", "gender", "address", "phone_number")
