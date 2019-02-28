from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
class RegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    first_name=forms.CharField( widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))

    class Meta:
        model= User
        fields=['first_name','last_name','username','email','date_joined','password','confirm_password']
    def clean_password(self):
        password=self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if(len(password)<8):
            raise forms.ValidationError(("The length of the password should be minimum 8 characters"))

        return password
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if(validate_email(email)==False):
            raise forms.ValidationError("The Email Format is In Correct")
        return email
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if (password != confirm_password):
            raise forms.ValidationError('Password doesn\'t match')


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)




