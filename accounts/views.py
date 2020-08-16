from django.shortcuts import render

# *** General import ***
from .models import *
from django.shortcuts import redirect
from django.contrib import messages

# *** CRUD with ModelForm ***
from .forms import OrderForm, ProductForm

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

# *** decorators
from .decorators import unauthenticated_user, allowed_users, admin_only

# *** Group model for different Users
from django.contrib.auth.models import Group


# Create your views here.
# *** Main ***___________________________________________________________

# * Login required decorator for dashboard page
@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
@admin_only
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Hai appena aggiunto il seguente prodotto {name}')
            return redirect('products')

    context = {
        'products': products,
        'form': form
    }
    return render(request, 'accounts/products.html', context)


# *** CRUD with ModelForm ***____________________________________________

# * Create
# * Login required decorator for createOrder page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@unauthenticated_user
def registerPage(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # * Add a flashmessage
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username} ')

            # * associate a group when someone registers
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

# * Login User
@unauthenticated_user
def loginPage(request):
    
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


# *** User Page ***
@login_required
@allowed_users(allowed_roles=['customer'])
def userPage(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/user.html', context)