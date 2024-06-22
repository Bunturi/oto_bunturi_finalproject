from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Product, Category, Customer
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, ProductForm
import json
from cart.cart import Cart

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    searched = request.GET.get('searched', '')
    if searched:
        products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched)).order_by('id')
        if not products:
            messages.success(request, "That Product Does Not Exist...Please try Again.")
            products = []  # or you can return all products if you prefer
    else:
        products = Product.objects.all().order_by('id')

    paginator = Paginator(products, 8)  # Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {'page_obj': page_obj, 'query': searched})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #shoping cart stuff
            current_user = Customer.objects.get(user__id=request.user.id)
            # get saved cart
            saved_cart = current_user.old_cart
            # convert back to dict
            if saved_cart:
                # convert to dict using json
                converted_cart = json.loads(saved_cart)
                # add cart dict to sesion
                cart = Cart(request)
                #loop the cart + add itms to db
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)


            messages.success(request, ('Logged in'))
            return redirect('store:home')
        else:
            messages.success(request, ('Error, try again'))
            return redirect('store:login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('Logged out'))
    return redirect('store:home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registered successfully'))
            return redirect('store:home')
        else:
            messages.success(request, ('Try again'))
            return redirect('store:register')
    else:
        return render(request, 'register.html', {'form': form})

def category(request, cat):
    cat = cat.replace('-', ' ')
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category).order_by('id')
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        return redirect('store:home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User has been updated")
            return redirect('store:home')

            # we can take user here?????????
        # print((user_form['username'].value()))

        return render(request, "update_user.html", {'user_form': user_form})


def update_password(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password has been updated")
                login(request, current_user)
                return redirect('store:home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('store:update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
    else:
        messages.success(request, "Please log in first")
        return redirect('store:home')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:home')
    else:
        form = ProductForm()
    return render(request, 'add_Product.html', {'form': form})


def delete_product(request, id):
    if request.user.has_perm('mainapp.delete_event'):
        Product.objects.get(pk=id).delete()
    return redirect('store:home')


def offers(request):
    sale_products = Product.objects.filter(is_sale=True).order_by('id')

    paginator = Paginator(sale_products, 8)  # Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {'page_obj': page_obj})