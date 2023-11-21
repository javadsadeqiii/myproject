from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError




class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
  
    
    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email = email).exists()
        if user:
            raise ValidationError(" ایمیل وارد شده قبلا ثبت شده ")
        return email 
    
    
    
    
    
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username = username).exists()
        if user:
            raise ValidationError(" نام کاربری وارد شده قبلا ثبت شده ")
        return username
        
            
    

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    