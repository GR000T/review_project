from django import forms
from django.contrib.auth import (
                authenticate,
                get_user_model
)

from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    email=forms.EmailField(label='email', widget=forms.TextInput(attrs={'class':'form-control _ge_de_ol', 'id':'email','placeholder':'Enter Email','name':'email'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control _ge_de_ol', 'id':'password','placeholder':'Enter Password','name':'password'}))
    def clean(self,*args,**kwargs):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')

        if email and password:
            user=authenticate(email=email,password=password)
            if not user:
                raise forms.ValidationError('user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('user is not active')
        return super(UserLoginForm,self).clean(*args,**kwargs)


class UserRegisterForm(forms.ModelForm):
    username=forms.CharField(label='username', widget=forms.TextInput(attrs={'class':'form-control', 'id':'username','placeholder':'Username'}))
    email=forms.EmailField(label='email',widget=forms.EmailInput(attrs={'class':'form-control', 'id':'email','placeholder':'Your Email'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'password','placeholder':'Password'}))
    password_confirm=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'confirm_password','placeholder':'Confirm Password'}))

    class Meta:
        model=User
        fields= [
            'username',
            'email',
            'password',
            'password_confirm'
        ]

        def clean(self):
            email=self.cleaned_data.get('email')
            password=self.cleaned_data.get('password')
            password_confirm=self.cleaned_data.get('password_confirm')
            
            email_qs=User.objects.filter(email=email)
            if email_qs.exists():
                raise forms.ValidationError('email already exists')
            return email
