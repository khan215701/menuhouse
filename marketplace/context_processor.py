from marketplace.models import Cart


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
    