from django.urls import path
from . import views

urlpatterns = [
    path('', views.dasboard, name="dashboard" ),
    path('customer/', views.customer, name="customer" ),
    path('products/', views.products, name="products" ),
]