from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    
    path('forgot_password/', views.forgotPassword, name='forgotPassword'),
    path('reset_password/<uidb64>/<token>', views.resetPasswordValidate, name='resetPassword'),
    path('reset_password/', views.resetPassword, name='resetPassword'),
    
    path('vendor/', include('vendor.urls')),
    path('customer/', include('customers.urls')),
]
