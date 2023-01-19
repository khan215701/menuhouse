from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from vendor.models import Vendor, OpeningHour
from menu.models import Category, FoodItem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from marketplace.models import Cart
from .context_processor import get_cart_counter, get_cart_amount
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date
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
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', 'from_hour')
    print(current_opening_hours)
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
    }
    return render(request,'marketplace/vendor_details.html', context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
       if   request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    check_cart = Cart.objects.get(user=request.user, foodItem=fooditem)
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({'status':'success', 'message':'increased quantity to cart','cart_counter':get_cart_counter(request), 'cart_amount':get_cart_amount(request),'qty':check_cart.quantity})
                except:
                    check_cart = Cart.objects.create(user=request.user, foodItem=fooditem, quantity=1)
                    return JsonResponse({'status':'success', 'message':'food is add to cart', 'cart_counter':get_cart_counter(request), 'cart_amount':get_cart_amount(request), 'qty':check_cart.quantity})
            except Exception as e:
                print(e)
                return JsonResponse({'status':'failed', 'message':'food does not avaliable'})
            
       else:
           return JsonResponse({'status':'failed', 'message':'invalid request'})
    else:
        return JsonResponse({'status':'failed', 'message':'please login to add to cart'})
            

def reduce_to_cart(request, food_id):
   if request.user.is_authenticated:
       if request.headers.get('x-requested-with') == 'XMLHttpRequest':
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
                    return JsonResponse({'status':'success', 'cart_counter':get_cart_counter(request), 'cart_amount':get_cart_amount(request),'qty':check_cart.quantity})
                except:
                    return JsonResponse({'status':'Failed', 'message':'you do not have this food in cart'})
            except:
                return JsonResponse({'status':'Failed', 'message':'food does not avaliable'})
       else:
           return JsonResponse({'status':'Failed', 'message':'invalid request'})
   else:
        return JsonResponse({'status':'login_required ', 'message':'please login to add to cart'})
    
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'success', 'message': 'Cart deleted successfully', 'cart_counter':get_cart_counter(request), 'cart_amount':get_cart_amount(request),})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'cart items does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'request invalid'})   
    else:
        return JsonResponse({'status': 'Failed', 'message': 'please login first'}) 
    

def search(request):
    keyword = request.GET['keyword']
    address = request.GET['address']
    lat = request.GET['lat']
    lng = request.GET['lng']
    
    vendor_by_fooditem = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor')    
    vendors = Vendor.objects.filter(Q(id__in=vendor_by_fooditem) |Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
    vendor_count = vendors.count()
    context = {
        'vendors' : vendors,
        'vendor_count' : vendor_count
    }
    return render(request, 'marketplace/listings.html', context)