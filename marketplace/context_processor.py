from marketplace.models import Cart, Tax
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cartitems = Cart.objects.filter(user=request.user)
            if cartitems:
                for item in cartitems:
                    cart_count += item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)
    

def get_cart_amount(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    tax_dict = {}
    
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
        for item in cart_item:
            food_item = FoodItem.objects.get(pk=item.foodItem.id)
            subtotal += (food_item.price * item.quantity)
            
        
        get_tax = Tax.objects.filter(is_active = True)
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((subtotal * i.tax_percentage)/100, 2) 
            tax_dict.update({tax_type: {tax_percentage : tax_amount}})
        tax = sum(x for key in tax_dict.values() for x in key.values())
        grand_total = subtotal + tax
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total, tax_dict=tax_dict)