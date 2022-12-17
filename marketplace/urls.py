from django.urls import path
from . import views
urlpatterns = [
    path('marketplace', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_details, name='vendor_details'),
]