from django.shortcuts import render, get_object_or_404, redirect
from account.form import profileForm, UserInfoForm
from account.models import profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='login')
def customerProfile(request):
    profile_user = get_object_or_404(profile, user=request.user)
    if request.method == 'POST':
        profile_form = profileForm(request.POST, request.FILES, instance=profile_user)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'successfully updated your profile')
            return redirect('profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        profile_form = profileForm(instance=profile_user)
        user_form = UserInfoForm(instance=request.user)
            
    
    context = {
        'profile': profile_user,
        'profile_form': profile_form,
        'user_form': user_form,
    }
    return render(request, 'customers/customer_profile.html', context)
