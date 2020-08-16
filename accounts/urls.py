from django.urls import path
from . import views

urlpatterns = [
    # *** Register, Login and Logout User ***
    path('register/', views.registerPage, name="register" ),
    path('login/', views.loginPage, name="login" ),
    path('logout/', views.logoutUser, name="logout" ),

    # *** User Page ***
    path('user/', views.userPage, name='user'),

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