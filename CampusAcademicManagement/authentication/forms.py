from django import forms


class LoginForm(forms.Form):
    rollno = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
