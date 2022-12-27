from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from marketplace.models import Cart
from .context_processor import get_cart_counter
# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendor_count': vendor_count,
        'vendors': vendors
    }
    return render(request,'marketplace/listings.html', context)

def vendor_details(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = 0
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request,'marketplace/vendor_details.html', context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
       if request.is_ajax():
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    check_cart = Cart.objects.get(user=request.user, foodItem=fooditem)
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({'status':'success', 'message':'increased quantity to cart','cart_counter':get_cart_counter(request), 'qty':check_cart.quantity})
                except:
                    check_cart = Cart.objects.create(user=request.user, foodItem=fooditem, quantity=1)
                    return JsonResponse({'status':'success', 'message':'food is add to cart', 'cart_counter':get_cart_counter(request), 'qty':check_cart.quantity})
            except:
                return JsonResponse({'status':'failed', 'message':'food does not avaliable'})
       else:
           return JsonResponse({'status':'failed', 'message':'invalid request'})
    else:
        return JsonResponse({'status':'failed', 'message':'please login to add to cart'})
    
    

def reduce_to_cart(request, food_id):
   if request.user.is_authenticated:
       if request.is_ajax():
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    check_cart = Cart.objects.get(user=request.user, foodItem=fooditem)
                    if check_cart.quantity > 1:
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({'status':'success', 'cart_counter':get_cart_counter(request), 'qty':check_cart.quantity})
                except:
                    return JsonResponse({'status':'Failed', 'message':'you do not have this food in cart'})
            except:
                return JsonResponse({'status':'Failed', 'message':'food does not avaliable'})
       else:
           return JsonResponse({'status':'Failed', 'message':'invalid request'})
   else:
        return JsonResponse({'status':'login_required ', 'message':'please login to add to cart'})