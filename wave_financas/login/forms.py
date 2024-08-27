from django import forms


# CLASSE QUE DEFINE FORMULÁRIO DE LOGIN
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    senha = forms.CharField(widget=forms.PasswordInput, label='Senha')