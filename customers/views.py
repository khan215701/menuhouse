from django.shortcuts import render, get_object_or_404
from account.form import profileForm, UserInfoForm
from account.models import profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def customerProfile(request):
    profile_user = get_object_or_404(profile, user=request.user)
    profile_form = profileForm(instance=profile_user)
    user_form = UserInfoForm()
    context = {
        'profile': profile_user,
        'profile_form': profile_form,
        'user_form': user_form,
    }
    return render(request, 'customers/customer_profile.html', context)
