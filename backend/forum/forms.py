from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user credentials
    """
    remove_profile_pic = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['avatar', 'email', 'name', 'bio']

    def save(self, commit=True):
        instance = super(UserUpdateForm, self).save(commit=False)
        if self.cleaned_data.get('remove_profile_pic'):
            instance.avatar = None
        if commit:
            instance.save()
        return instance


class UserSignUpForm(UserCreationForm):
    """
    Form for sign up
    """
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password1', 'password2',)
