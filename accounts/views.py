from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def dasboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/dashboard.html', context)


def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    total_orders = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
    }
    return render(request, 'accounts/customer.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


# *** CRUD ***
from .forms import OrderForm
from django.shortcuts import redirect

# * CReate
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


# * Update
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) # istance == mostra le informazioni dell'ordine selezionato
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) # istance == modifica l'ordine con le informazioni inviate dal post e non ne crea uno nuovo 
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)


# * Delete
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item': order
    }
    return render(request, 'accounts/delete.html', context)