from django.urls import path, include
from account import views as AccountView
from . import views 

urlpatterns = [
    path('', AccountView.vendorDashboard, name='vendor'),
    path('profile/', views.vendorProfile, name='vendorprofile'),
]
