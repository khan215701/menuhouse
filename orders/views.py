from django.shortcuts import render, redirect
from marketplace.models import Cart
from .models import Order
from marketplace.context_processor import get_cart_amount
from .forms import orderForm
import simplejson as json    # first install simplejson then import
# Create your views here.
def placeOrder(request):
    cart_item = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_item.count()
    if cart_count <= 0:
        return render('marketplace')
    subtotal = get_cart_amount(request)['subtotal']
    total_tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    tax_data = get_cart_amount(request)['tax_dict']
    print(tax_data,grand_total,total_tax,subtotal)
    
    if request.method == 'POST':
        form = orderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = request.POST['first_name']
            order.last_name = request.POST['last_name']
            order.email = request.POST['email']
            order.phone = request.POST['phone']
            order.address = request.POST['address']
            order.country = request.POST['country']
            order.state = request.POST['state']
            order.city = request.POST['city']
            order.pin_code = request.POST['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.order_number = '123'
            order.save()
            return redirect('placeOrder')
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')