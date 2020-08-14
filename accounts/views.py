from django.shortcuts import render

# *** General import ***
from django.http import HttpResponse
from .models import *
from django.shortcuts import redirect
from django.contrib import messages

# *** CRUD with ModelForm ***
from .forms import OrderForm

# *** FILTERS ***
from .filters import OrederFilter

# *** INLINE FORMSET ***
from django.forms import inlineformset_factory

# *** Regitration, Login and Logout User ***
# Registration
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
# authenticate, login and logout User
from django.contrib.auth import authenticate, login, logout

# *** Login required decorator
from django.contrib.auth.decorators import login_required


# Create your views here.
# *** Main ***___________________________________________________________

# * Login required decorator for dashboard page
@login_required(login_url='login')
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


# * Login required decorator for customer page
@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    total_orders = orders.count()

    # *** FILTERS ***
    myFilter = OrederFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    # ***************

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'myFilter': myFilter,
    }
    return render(request, 'accounts/customer.html', context)

# * Login required decorator for products page
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html', context)


# *** CRUD with ModelForm ***____________________________________________

# * Create
# * Login required decorator for createOrder page
@login_required(login_url='login')
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
# * Login required decorator for updateOrder page
@login_required(login_url='login')
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
# * Login required decorator for deleteOrder page
@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item': order
    }
    return render(request, 'accounts/delete.html', context)


#*** INLINE FORMSET ***__________________________________________________
# * Create formset * 
# * Login required decorator for createCustomerOrders page
@login_required(login_url='login')
def createCustomerOrders(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=(
        'product',
        'status'
    ), extra=10)

    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer': customer})
    #formset = OrderFormSet(instance=customer)
    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    
    context = {
        'formset': formset,
        'customer': customer
    }
    return render(request, 'accounts/order_formset.html', context)


# *** Regitration and Login ***__________________________________________

# * Register User
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                # * Add a flashmessage
                user = form.cleaned_data.get('username')
                messages.success(request, f'Account was created for {user} ')
                return redirect('login')
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)

# * Login User
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)

# * Logout User
# * Login required decorator for logoutUser page
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')