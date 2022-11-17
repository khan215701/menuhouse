from django.shortcuts import render, redirect
from .form import UserForm
from .models import User, profile
from vendor.form import VendorForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from account.utils import detectUser
from django.core.exceptions import PermissionDenied

# permission denied for customer
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
# permission denied for vendor
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # store a data using the form
            password = form.cleaned_data['password'].strip()
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            messages.success(request, 'Your account has been registered sucessfully!')
            user.save()
            
            return redirect('registerUser')
          
            # store a data using the create_user
            # first_name = form.cleaned_data['first_name'].strip()
            # last_name = form.cleaned_data['last_name'].strip()
            # username = form.cleaned_data['username'].strip()
            # email = form.cleaned_data['email'].strip()
            # pasword = form.cleaned_data['pasword'].strip()
            # user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
            #                                 email=email, password=password)
            # user.role = User.CUSTOMER
            # user.save()
            # return redirect('registerUser')
    else:
        form = UserForm()
    context = {
    'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)



def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid:
            password = form.cleaned_data['password'].strip()
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            profile_user = profile.objects.get(user=user)
            vendor.user_profile = profile_user
            vendor.save()
            messages.success(request, 'Your account has been registered successfully! please wait for approval!')
            return redirect('registerVendor')
        else:
            print('invalid vendor form')
            print(vendor_form.errors)
    else:
        form = UserForm()
        vendor_form = VendorForm()
    
    context = {
        'form': form,
        'vendor_form' : vendor_form
    }
    return render(request, 'accounts/registerVendor.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You are now logged out')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)

 
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendordashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerdashboard.html')

