from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import RegisterForm, LoginForm, ProductForm
from .models import *
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

# ANCHOR home
def home(request):
    featured_products = Product.objects.filter(is_featured=True)
    return render(request, 'home.html', {'featured_products': featured_products})

def all_products(request):
    products = Product.objects.all()
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    return render(request, 'products.html', {'products': products ,'category': 'All Products'} )

# ANCHOR products
def products(request, category):
    category = category.lower()  
    products = Product.objects.filter(category=category)
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    return render(request, 'products.html', {'products': products, 'category': category})  

# ANCHOR product
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('home')

# ANCHOR add to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    
    request.session['cart'] = cart
    return redirect('cart')

# ANCHOR remove from cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    
    return redirect('cart')


# ANCHOR update cart

@require_POST
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))

    if str(product_id) in cart:
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            del cart[str(product_id)]
        request.session['cart'] = cart
    
    return redirect('cart')

# ANCHOR cart
def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    
    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'total': product.price * cart[str(product.id)]
        })
    
    grand_total = sum(item['total'] for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'grand_total': grand_total})

# ANCHOR checkout
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
            'total': product.price * cart[str(product.id)]
        })

    grand_total = sum(item['total'] for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'grand_total': grand_total})

# ANCHOR dashboard

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    products = Product.objects.all()
    featured_count = Product.objects.filter(is_featured=True).count()
    categories_count = Product.objects.values('category').distinct().count()
    return render(request, 'admin/dashboard.html', {
        'products': products,
        'featured_count': featured_count,
        'categories_count': categories_count
    })
# ANCHOR add product
@login_required
def add_product(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'admin/product_form.html', {'form': form, 'action': 'Add'})

@login_required
def edit_product(request, product_id):
    if not request.user.is_staff:
        return redirect('home')
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_form.html', {'form': form, 'action': 'Edit', 'product': product})

# ANCHOR delete product
@login_required
@require_POST
def delete_product(request, product_id):
    if not request.user.is_staff:
        return redirect('home')
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('dashboard')