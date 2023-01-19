from django.shortcuts import render

# Create your views here.

def customerProfile(request):
    return render(request, 'customers/customer_profile.html')
