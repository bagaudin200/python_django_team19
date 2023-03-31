from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET

from app_cart.models import ProductInCart
from app_goods.models import Product
from django.views.generic import TemplateView
from app_cart.services import CartServices
from app_cart.forms import CartAddProductForm, CartAddProductModelForm


class CartDetail(TemplateView):
    template_name = 'app_cart/cart.jinja2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartServices(self.request)
        context['cart'] = cart
        if self.request.user.is_authenticated:
            context['forms'] = [CartAddProductModelForm(instance=item) for item in cart]
        else:
            for item in cart:
                item['update_quantity_form'] = CartAddProductForm(
                    initial={'quantity': item['quantity'], 'update': False})
        return context


def cart_add(request, pk):
    cart = CartServices(request)
    product = get_object_or_404(Product, id=pk)
    if request.user.is_authenticated:
        product_in_cart = get_object_or_404(ProductInCart, id=pk)
        form = CartAddProductModelForm(request.POST, instance=product_in_cart)
        form.save()
    else:
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'],
                     update_quantity=cd['update'])
    return redirect('cart_detail')


@require_GET
def cart_remove(request, pk):
    cart = CartServices(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    return redirect('cart_detail')


@require_GET
def get_cart_data(request):
    product_id = request.GET.get('product', None)
    cart = CartServices(request)
    response = {
        'total_len': len(cart),
        'total': cart.get_total_price()
    }
    if product_id:
        product = cart.cart[product_id]
        total_item = int(product['quantity']) * Decimal(product['price'])
        response['total_item'] = total_item
    return JsonResponse(response)
