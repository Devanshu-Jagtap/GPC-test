from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.core.exceptions import ValidationError


# Custom Signup Form
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


    def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise ValidationError("This email is already registered.")
            return email


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['category', 'subcategory','title','content', 'publish_date', 'keywords', 'country_of_origin']

    # Custom validation logic for subcategory based on category selection
    def clean_subcategory(self):
        subcategory = self.cleaned_data.get('subcategory')
        category = self.cleaned_data.get('category')
        if subcategory and category:
            if subcategory.category != category:
                raise forms.ValidationError("Subcategory does not belong to the selected category.")
        return subcategory


class NewsImagesForm(forms.ModelForm):
    class Meta:
        model = NewsImages
        fields = ['images']