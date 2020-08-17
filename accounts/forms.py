from django.forms import ModelForm
from .models import Order, Product, Tag, Customer

# *** Regitration and Login ***
from django.contrib.auth.forms import UserCreationForm
from django import forms # ?
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__' # '__all__' is equal to ['customer', 'product', 'date_created', 'status']


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__' 


# *** Regitration and Login ***

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# * Account page
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']