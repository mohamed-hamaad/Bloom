from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Catalog

    path('', home, name='home'), #✅
    path('products/all/', all_products, name='products_all'),
    path('products/<str:category>/', products, name='products'), #✅
    path('product/<int:product_id>/', product_detail, name='product_detail' ), #✅ 
    
    # Authintication
    path('register/', register, name='register'), #✅ 
    path('login/', login_view, name='login'), #✅ 
    path('logout/', logout_view, name='logout'), #✅ 
    
    # Cart
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'), #✅ 
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'), #✅ 
    path('update_cart/<int:product_id>/', update_cart, name='update_cart'), #✅ 
    path('cart/', cart, name='cart'), #✅ 
    path('checkout/', checkout, name='checkout'), #✅
    
    # Admin
    path('dashboard/', dashboard , name='dashboard'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)