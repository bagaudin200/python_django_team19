from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from app_cart.services import Cart


@require_POST
def cart_add(request):
    """Функция заглушка для получения данных в корзину"""
    # product = request.POST.get['id_product']
    # quantity = request.POST.get['quantity']
    # def add(self, product: object, quantity: int = 1, update_quantity: bool = False) -> None:
    messages.success(request, 'Товар добавлен в корзину!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

