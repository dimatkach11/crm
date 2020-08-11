from django.urls import path
from . import views

urlpatterns = [
    path('', views.dasboard, name="dashboard" ),
    path('products/', views.products, name="products" ),
    path('customer/<str:pk_test>/', views.customer, name="customer" ),
]