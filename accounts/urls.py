from django.urls import path
from . import views

urlpatterns = [
    # *** Register and Login ***
    


    # *** MAIN ***
    path('', views.dasboard, name="dashboard" ),
    path('products/', views.products, name="products" ),
    path('customer/<str:pk_test>/', views.customer, name="customer" ),

    # *** CRUD ***
    path('create_order/', views.createOrder, name="create_order" ),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order" ),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order" ),

    # *** INLINE FORMSET ***
    path('create_order/<str:pk>', views.createCustomerOrders, name="create_customer_orders" ),
]