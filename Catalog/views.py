from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import RegisterForm, LoginForm, ProductForm
from .models import *
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .filters import *
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
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
        
    products_queryset = Product.objects.all().order_by('id')
    my_filter = ProductFilter(request.GET, queryset=products_queryset)
    filtered_products = my_filter.qs

    paginator = Paginator(filtered_products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    featured_count = Product.objects.filter(is_featured=True).count()
    categories_count = Product.objects.values('category').distinct().count()
    
    context = {
        'page_obj': page_obj,
        'myFilter': my_filter,
        'total_products_count': filtered_products.count(),
        'featured_count': featured_count,
        'categories_count': categories_count
    }

    if request.GET.get('ajax') == '1':
        return render(request, 'admin/partials/products_table.html', context)
        
    return render(request, 'admin/dashboard.html', context)


ProductImageFormSet = inlineformset_factory(
    Product, 
    ProductImage, 
    fields=('image',), 
    extra=3, 
    can_delete=True
)

# ANCHOR add product
@login_required
def add_product(request):
    if not request.user.is_staff:
        return redirect('home')
        
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            product = form.save() 
            formset.instance = product
            formset.save() 
            return redirect('dashboard')
    else:
        form = ProductForm()
        formset = ProductImageFormSet()
        
    return render(request, 'admin/product_form.html', {'form': form, 'formset': formset, 'action': 'Add'})

# ANCHOR edit product
@login_required
def edit_product(request, product_id):
    if not request.user.is_staff:
        return redirect('home')
        
    product = get_object_or_404(Product, id=product_id)
    
    existing_images_count = product.images.count()

    if existing_images_count == 1:
        dynamic_extra = 2
    elif existing_images_count == 2:
        dynamic_extra = 1
    elif existing_images_count >= 3:
        dynamic_extra = 0
    else: 
        dynamic_extra = 3

    DynamicImageFormSet = inlineformset_factory(
        Product, 
        ProductImage, 
        fields=('image',), 
        extra=dynamic_extra, # 👈 السحر هنا
        can_delete=True
    )
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = DynamicImageFormSet(request.POST, request.FILES, instance=product)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
        formset = DynamicImageFormSet(instance=product)
        
    return render(request, 'admin/product_form.html', {
        'form': form, 
        'formset': formset, 
        'action': 'Edit', 
        'product': product
    })

# ANCHOR delete product
@login_required
@require_POST
def delete_product(request, product_id):
    if not request.user.is_staff:
        return redirect('home')
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('dashboard')
