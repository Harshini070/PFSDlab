from django.shortcuts import render, redirect
from .models import Customer, Order, Product  # Removed wildcard import
from .forms import OrderForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import CreateUserForm

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request, 'home.html', {'name': 'Harshini'})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add(request):
    try:
        val1 = int(request.POST.get('num1', 0))
        val2 = int(request.POST.get('num2', 0))
        val3 = val1 + val2
    except ValueError:
        val3 = "Invalid input! Please enter valid numbers."
    return render(request, 'result.html', {'result': val3})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    return render(request, 'dashboard.html', {'customers': customers, 'orders': orders})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def products(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'cust': customer, 'orders': orders, 'ordcount': order_count}
    return render(request, 'customer.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createOrder(request):
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'delete.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, "Password does not follow the rules.")  # Changed to error
    context = {'form': form}
    return render(request, 'register.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Username or password is incorrect")  # Changed to error
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutPage(request):
    logout(request)
    return redirect('login')
