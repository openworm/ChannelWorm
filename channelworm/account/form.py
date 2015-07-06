from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.forms import ModelForm



class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        password = self.data['password']
        confirm_password = self.data['confirm_password']
        print(make_password(password))
        print(confirm_password)
        if password != confirm_password:
            raise forms.ValidationError("Your password do not match")

        return make_password(password)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.is_active = False  # not active until he opens activation link
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
