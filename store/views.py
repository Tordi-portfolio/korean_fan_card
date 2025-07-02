from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

from payment.models import ShippingAddress
from payment.forms import ShippingForm


# Create your views here.

def founders(request):
    return render(request, 'founders.html')

def usage(request):
    return render(request, 'usage.html')

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']

        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.success(request, ('이 상품은 존재하지 않습니다... 다시 시도해 주세요...'))
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched':searched})
            
    else:
        pass
    return render(request, 'search.html', {})


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid():
            form.save(),

            messages.success(request, ('회원 정보가 업데이트되었습니다...'))
            return redirect('home')
        return render(request, 'update_info.html', {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, ('이 페이지에 접근하려면 로그인해야 합니다...'))
        return redirect('home')



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, ('비밀번호가 변경되었습니다... 다시 로그인해 주세요...'))
                login(request, current_user)
                return redirect ('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})

    else:
        messages.success(request, ('해당 페이지를 보려면 로그인해야 합니다...'))
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)

        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save(),

            login(request, current_user)
            messages.success(request, ('프로필이 업데이트되었습니다...'))
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, ('이 페이지에 접근하려면 로그인해야 합니다...'))
        return redirect('home')



def home(request):
    products = Product.objects.all()

    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Lets do some shopping stuffs
            current_user = Profile.objects.get(user__id=request.user.id)
            # get there saved cart from database
            saved_cart = current_user.old_cart
            # convert database string to dictionary
            if saved_cart:
                # convert to dictonary using Json
                converted_cart = json.loads(saved_cart)
                # add the loaded dictionary to session
                cart = Cart(request)
                # let loop through the cart
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ('로그인되었습니다...'))
            return redirect('home')
        else:
            messages.success(request, ('잘못된 자격 증명입니다... 다시 시도해주세요...'))
            return redirect('login')

    else:
        return render(request, 'login.html', {})


def register_user(request):

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login The User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('성공적으로 회원가입 되었습니다...'))
            return redirect('login')
        else:
            messages.success(request, ('잘못된 인증 정보입니다... 다시 시도해주세요...'))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})



def logout_user(request):
    logout(request),
    messages.success(request, ('로그아웃되었습니다...'))
    return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def category(request,foo):
    # Replace hyphens with spaces
    foo = foo.replace('-', ' ')

    # Grab the category from the url
    try:
        # look up yhe category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category': category})

    except:
        messages.success(request, ('해당 카테고리가 존재하지 않습니다...'))
        return redirect('home')



def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})



def customer_service(request):
    return render(request, 'customer_service.html', {})

# views.py

from django.shortcuts import render, redirect
from .models import Payment
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def payment_page(request):
    if request.method == "POST":
        method = request.POST.get("method")
        amount = request.POST.get("amount")
        crypto_currency = request.POST.get("crypto_currency")
        wallet_address = request.POST.get("wallet_address")

        payment = Payment.objects.create(
            user=request.user,
            method=method,
            amount=amount,
            crypto_currency=crypto_currency if method == "crypto" else None,
            wallet_address=wallet_address if method == "crypto" else None,
        )

        if method == "paypal":
            # Redirect to PayPal
            return redirect("https://www.paypal.com")  # Replace with real URL if using PayPal SDK

        return render(request, "payment_success.html", {"payment": payment})

    return render(request, "payment.html")
