from django.urls import path
from . import views
urlpatterns = [
    path('marketplace', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_details, name='vendor_details'),
    
    # carts url
    path('add_to_cart/<int:food_id>', views.add_to_cart, name='add_to_cart'),
]