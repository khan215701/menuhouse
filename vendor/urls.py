from django.urls import path, include
from account import views as AccountView
from . import views 

urlpatterns = [
    path('', AccountView.vendorDashboard, name='vendor'),
    path('profile/', views.vendorProfile, name='vendorProfile'),
    path('menu-builders/', views.menuBuilder, name='menuBuilder'),
    path('menu-builder/category/<int:pk>', views.fooditemsByCategory, name='fooditems_by_category'),
    
    #CRUD methods
    path('menu-builder/category/add', views.categoryAdd, name='add_category'),
    path('menu-builder/category/edit/<int:pk>', views.categoryEdit, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>', views.categoryDelete, name='delete_category'),
]
