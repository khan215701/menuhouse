import re
from django.http import HttpResponse

def home(request):
  return HttpResponse('My home')