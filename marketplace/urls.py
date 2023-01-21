from django.urls import path
from . import views
urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_details, name='vendor_details'),
    
    # carts url
    path('add_to_cart/<int:food_id>', views.add_to_cart, name='add_to_cart'),
    path('reduce_to_cart/<int:food_id>', views.reduce_to_cart, name='reduce_to_cart'),
    path('delete_cart/<int:cart_id>', views.delete_cart, name='delete_cart'),
    
    #checkout cart
    
    path('checkout', views.checkout, name='checkout'),
]