from django.shortcuts import render
from account.form import profileForm, UserInfoForm
# Create your views here.

def customerProfile(request):
    profile_form = profileForm()
    user_form = UserInfoForm()
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
    }
    return render(request, 'customers/customer_profile.html', context)
