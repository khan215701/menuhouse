from django.urls import path, include
from account import views as AccountView
from . import views 

urlpatterns = [
    path('', AccountView.vendorDashboard, name='vendor'),
    path('profile/', views.vendorProfile, name='vendorProfile'),
    path('menu-builders/', views.menuBuilder, name='menuBuilder'),
    path('menu-builder/category/<int:pk>', views.fooditemsByCategory, name='fooditems_by_category'),
]
