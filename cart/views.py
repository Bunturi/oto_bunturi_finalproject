from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product, Order, Customer
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Product Added To Cart...")
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        # return redirect('cart_summary')
        messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        # return redirect('cart_summary')
        messages.success(request, "Your Cart Has Been Updated...")
        return response

def cart_checkout(request):
    if request.method == 'POST':
        cart = Cart(request)
        if cart.__len__() == 0:
            messages.error(request, "Your cart is empty.")
            return redirect('cart:cart_summary')

        customer = Customer.objects.get(user=request.user)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()

        for product in cart_products:
            quantity = quantities[str(product.id)]
            total_price = product.sale_price if product.is_sale else product.price
            total_price *= quantity

            Order.objects.create(
                product=product,
                customer=customer,
                quantity=quantity,
                total_price=total_price,
                date=timezone.now(),
            )

        # Clear the cart
        cart.clear()


        messages.success(request, "Order placed successfully!")
        return redirect('cart:order_history')
    else:
        return redirect('cart:cart_summary')


def order_history(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-date')
        return render(request, 'order_history.html', {'orders': orders})
    else:
        messages.error(request, "Please log in to view your order history.")
        return redirect('store:login')