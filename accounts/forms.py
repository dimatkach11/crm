from django.forms import ModelForm
from .models import Order

# *** Regitration and Login ***
from django.contrib.auth.forms import UserCreationForm
from django import forms # ?
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__' # '__all__' is equal to ['customer', 'product', 'date_created', 'status']


# *** Regitration and Login ***

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']