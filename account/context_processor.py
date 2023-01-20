from vendor.models import Vendor
from account.models import profile
from django.shortcuts import get_object_or_404
from django.conf import settings

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_profile_cover(request):
    user_profile = get_object_or_404(profile, user=request.user)
    return dict(user_profile=user_profile)

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}