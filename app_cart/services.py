from decimal import Decimal

from django.conf import settings
from django.views.decorators.http import require_POST, require_GET
from app_goods.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F
from django.shortcuts import render
from app_cart.forms import CartAddProductForm
from app_cart.models import Cart, ProductInCart


class CartServices(object):

    def __init__(self, request):
        """
        Инициализировать корзину.
        """

        self.use_db = False
        self.cart = None
        self.user = request.user
        self.session = request.session
        self.qs = None
        cart = self.session.get(settings.CART_SESSION_ID)
        if self.user.is_authenticated:
            self.use_db = True
            if cart:
                self.save_in_db(cart, request.user)
                self.clear(True)
            cart = Cart.objects.get(user=self.user)
            self.qs = ProductInCart.objects.filter(cart=cart)
        else:
            # сохранить пустую корзину в сеансе
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def get_cart_from_db(self, qs):
        cart = {}
        for item in qs:
            cart[str(item.good.id)] = {'product': item.good, 'quantity': item.quantity, 'price': item.price}
        return cart

    def save_in_db(self, cart, user):
        for key, value in cart.items():
            if Cart.objects.filter(user=user, good=key).exists():
                good = Cart.objects.select_for_update().get(user=user, good=key)
                good.quantity += cart[key]['quantity']
                good.price = cart[key]['price']
                good.save()
            else:
                product = Product.objects.get(id=key)
                Cart.objects.create(
                    user=user,
                    good=product,
                    quantity=value['quantity'],
                    price=value['price'],
                )

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавьте товар в корзину или обновите его количество.
        """
        if self.use_db:
            if self.qs.filter(product=product).exists():
                cart = self.qs.select_for_update().get(product=product)
            else:
                cart = Cart(
                    user=self.user,
                    good=product,
                    quantity=0,
                    price=product.price
                )
            if update_quantity:
                cart.quantity = quantity
            else:
                cart.quantity += quantity
            cart.save()
        else:
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
            if update_quantity:
                self.cart[product_id]['quantity'] += quantity
            else:
                self.cart[product_id]['quantity'] = quantity
            self.save()

    def save(self):
        if not self.use_db:
            # обновить корзину сеансов
            self.session[settings.CART_SESSION_ID] = self.cart
            # пометить сеанс как «измененный», чтобы убедиться, что он сохранен
            self.session.modified = True

    def remove(self, product):
        """
        Удалить товар из корзины
        :param product:
        :return:
        """
        if self.use_db:
            if self.qs.filter(product=product).exists():
                self.qs.filter(product=product).delete()
        else:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

    def __iter__(self):
        """
        Перебирайте товары в корзине, и получайте товары
        из базы данных.
        """
        if self.use_db:
            for product in self.cart.productincart_set.all():
                yield product
        else:
            product_ids = self.cart.keys()
            # получить объекты продукта и добавить их в корзину
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                self.cart[str(product.id)]['product'] = product

            for item in self.cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    # def __len__(self):
    #     """
    #     Подсчитайте все товары в корзине.
    #     """
    #     return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        if self.use_db:
            # total = sum(product.product.price * product.quantity for product in self)

            total = self.qs. \
                only('quantity', 'price'). \
                aggregate(total=Sum(F('quantity') * F('product__price')))['total']
            if not total:
                total = Decimal('0')
            return total.normalize()
        else:
            return sum(Decimal(item['price']) * item['quantity'] for item in
                       self.cart.values())

    def clear(self, only_session=False):
        """
        Удалить корзину из сеанса или из базы данных, если пользователь авторизован
        :return:
        """
        if only_session:
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True
        else:
            if self.qs:
                self.qs.delete()



