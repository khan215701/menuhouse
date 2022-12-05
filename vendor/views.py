from account.models import profile
from .models import Vendor
from menu.models import Category, FoodItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from account.form import profileForm
from .form import VendorForm
from menu.form import categoryForm
from django.contrib.auth.decorators import login_required, user_passes_test
from account.views import check_role_vendor
from django.template.defaultfilters import slugify

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
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
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


# CRUD method views

def categoryAdd(request):
    if request.method == 'POST':
        category_form = categoryForm(request.POST)
        if category_form.is_valid():
            category_name = category_form.cleaned_data['category_name']
            category = category_form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category_form.save()
            messages.success(request, 'category added successfully')
            return redirect('menuBuilder')
        else:
            print(category_form.errors)
    else:
        category_form = categoryForm()
    context = {
        'category_form': category_form,
    }
    return render(request, 'vendor/categoryAdd.html', context)


def categoryEdit(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_form = categoryForm(request.POST, instance=category)
        if category_form.is_valid():
            category_name = category_form.cleaned_data['category_name']
            category = category_form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category_form.save()
            messages.success(request, 'category Updated successfully')
            return redirect('menuBuilder')
        else:
            print(category_form.errors)
    else:
        category_form = categoryForm(instance=category)
    context = {
        'category_form': category_form,
        'category' : category,
    }
    return render(request, 'vendor/categoryEdit.html', context)


def categoryDelete(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'category Updated successfully')
    return redirect('menuBuilder')