from account.models import profile
from .models import Vendor
from menu.models import Category, FoodItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from account.form import profileForm
from .form import VendorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from account.views import check_role_vendor

# Create your views here.

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorProfile(request):
    user_profile = get_object_or_404(profile, user=request.user)
    vendor = get_object_or_404(Vendor)
    
    if request.method == 'POST':
        profile_form = profileForm(request.POST, request.FILES, instance=user_profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'settings successfully')
            return redirect('vendorProfile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:       
        profile_form = profileForm(instance=user_profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'user_profile': user_profile,
        'vendor' : vendor,
        'profile_form': profile_form,
        'vendor_form' : vendor_form
    }
    return render(request, 'vendor/vendorProfile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menuBuilder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menuBuilder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditemsByCategory(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    foodItem = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'category': category,
        'fooditems' : foodItem
    }
    return render(request, 'vendor/fooditemsByCategory.html', context)
