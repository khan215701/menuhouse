from django.shortcuts import render, redirect
from .form import UserForm
from .models import User, profile
from vendor.form import VendorForm
from django.contrib import messages

# Create your views here.

def registerUser(request):
    if request.method == 'POST':
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
    if request.method == 'POST':
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
