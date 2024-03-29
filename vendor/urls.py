from django.urls import path, include
from account import views as AccountView
from . import views 

urlpatterns = [
    path('', AccountView.vendorDashboard, name='vendor'),
    path('profile/', views.vendorProfile, name='vendorProfile'),
    path('menu-builders/', views.menuBuilder, name='menuBuilder'),
    path('menu-builder/category/<int:pk>', views.fooditemsByCategory, name='fooditems_by_category'),
    
    #category CRUD methods
    path('menu-builder/category/add/', views.categoryAdd, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.categoryEdit, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.categoryDelete, name='delete_category'),
    
    #food items CRUD methods
    path('menu-builder/food/add/', views.foodAdd, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.foodEdit, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.foodDelete, name='delete_food'),
    
    #opening Hours urls
    path('opening-hours/', views.openingHours, name='opening_hours'),
    path('opening-hours/add/', views.addHours, name='addHours'),
    path('opening-hours/delete/<int:pk>/', views.deleteHours, name='deleteHours'),
]
