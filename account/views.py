from django.shortcuts import render, redirect
from .form import UserForm
from .models import User, profile
from vendor.models import Vendor
from vendor.form import VendorForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from account.utils import detectUser, send_email
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify

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
        return redirect('myAccount')
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
            subject = 'please confirm your verification link to activate your account'
            template = 'accounts/emails/email_verification.html'
            send_email(request, user, subject, template)
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
            print('invalid form')
            print(form.errors)
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
            vendor_name = vendor_form.cleaned_data['vendor_name'].strip()
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            profile_user = profile.objects.get(user=user)
            vendor.user_profile = profile_user
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            vendor.save()
            subject = 'please confirm your verification link to activate your account'
            template = 'accounts/emails/email_verification.html'
            send_email(request, user, subject, template)
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

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except:
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'congratulation account is activated successfully')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activate link')
        return redirect('myAccount')
    
    
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        is_exist = User.objects.filter(email=email).exists()
        
        if is_exist:
            user = User.objects.get(email__exact=email)
            subject = 'Reset Your Password'
            template = 'accounts/emails/email_reset_password.html'
            send_email(request, user, subject, template)
            messages.success(request, 'Password  reset link has been sent successfully')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgot_password.html')

def resetPasswordValidate(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User._default_manager.get(pk=uid)
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'please reset your password')
        return redirect('resetPassword')
    else:
        messages.info(request, 'This link has been expired')
        return redirect('myAccount')        

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match')
            return redirect('resetPassword')
    return render(request, 'accounts/reset_password.html')




 