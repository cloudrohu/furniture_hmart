from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from order.models import ShopCart, Order, OrderForm, OrderProduct
from product.models import Product, Category, Variants
from user.models import UserProfile


def index(request):
    return HttpResponse("Order Page")


@login_required(login_url='/login')
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER', '/')
    current_user = request.user
    product = Product.objects.get(pk=id)

    quantity = int(request.POST.get('quantity', 1))
    variantid = request.POST.get('variantid', None)

    if product.variant != 'None' and variantid:
        cart_item, created = ShopCart.objects.get_or_create(
            user=current_user, product=product, variant_id=variantid
        )
    else:
        cart_item, created = ShopCart.objects.get_or_create(
            user=current_user, product=product
        )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    messages.success(request, f"✅ {product.title} added to your cart.")
    return HttpResponseRedirect(url)



# 🧺 SHOPCART PAGE
@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = sum(rs.amount for rs in shopcart)

    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
    }
    return render(request, 'about.html', context)


# ❌ DELETE FROM CART
@login_required(login_url='/login')
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id, user_id=request.user.id).delete()
    messages.success(request, "Item removed from your cart.")
    return HttpResponseRedirect("/order/shopcart")


# 💳 PLACE ORDER
@login_required(login_url='/login')
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = sum(rs.amount for rs in shopcart)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.country = form.cleaned_data['country']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            data.code = get_random_string(6).upper()
            data.save()

            # Move cart items to order
            for rs in shopcart:
                OrderProduct.objects.create(
                    order=data,
                    user=current_user,
                    product=rs.product,
                    variant=rs.variant,
                    quantity=rs.quantity,
                    price=rs.price,
                    amount=rs.amount,
                )

            ShopCart.objects.filter(user_id=current_user.id).delete()
            messages.success(request, "🎉 Your order has been placed successfully!")
            return render(request, 'Order_Completed.html', {'ordercode': data.code, 'category': category})

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'form': form,
        'profile': profile,
    }
    return render(request, 'Order_Form.html', context)


@csrf_exempt
@login_required(login_url='/login')
def ajax_add_to_cart(request, id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        current_user = request.user
        cart_item, created = ShopCart.objects.get_or_create(
            user=current_user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        total_items = ShopCart.objects.filter(user=current_user).count()
        total_price = sum(item.amount for item in ShopCart.objects.filter(user=current_user))

        return JsonResponse({
            'success': True,
            'cart_count': total_items,
            'cart_html': render_cart_sidebar(current_user),
            'subtotal': total_price,
        })
    return JsonResponse({'success': False})