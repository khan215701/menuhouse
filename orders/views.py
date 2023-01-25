from django.shortcuts import render

# Create your views here.
def placeOrder(request):
    return render(request, 'orders/place_order.html')