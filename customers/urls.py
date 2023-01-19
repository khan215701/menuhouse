from django.urls import path
from account import views as AccountView
from . import views
urlpatterns = [
    path('', AccountView.customerDashboard, name='customer' ),
    path('profile/', views.customerProfile, name='profile'),
]
