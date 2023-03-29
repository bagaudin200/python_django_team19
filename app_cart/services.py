from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F

from app_cart.models import Cart, ProductInCart
from app_goods.models import Product


class CartServices:

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
            try:
                cart = Cart.objects.get(user=self.user)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(user=self.user)
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
        """Перенос корзины из сессии в БД"""
        for key, value in cart.items():
            if Cart.objects.filter(user=user).exists():  # если корзина уже есть в БД
                try:
                    product = ProductInCart.objects.select_for_update().get(product=key)
                    product.quantity += cart[key]['quantity']
                    # product.price = cart[key]['price']
                    product.save()
                except ObjectDoesNotExist:
                    ProductInCart.objects.create(
                        product=Product.objects.get(pk=key),
                        cart=Cart.objects.get(user=user),
                        quantity=cart[key]['quantity']
                    )
            else:  # если корзины еще нет в БД
                product = Product.objects.get(id=key)
                cart_ = Cart.objects.create(user=user)
                ProductInCart.objects.create(
                    product=product,
                    cart=cart_,
                    quantity=value['quantity'],
                )

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавьте товар в корзину или обновите его количество.
        """
        if self.use_db:
            if self.qs.filter(product=product).exists():
                product_in_cart = self.qs.select_for_update().get(product=product)
            else:
                product_in_cart = ProductInCart(
                    product=product,
                    cart=self.cart,
                    quantity=0
                )
            if update_quantity:
                product_in_cart.quantity += quantity
            else:
                product_in_cart.quantity = quantity
            product_in_cart.save()
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
            for product in self.cart.products.all():
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

    def __len__(self):
        """
        Подсчитайте все товары в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        if self.use_db:
            total = self.qs.only('quantity', 'price').aggregate(total=Sum(F('quantity') * F('product__price')))['total']
            if not total:
                total = Decimal('0')
            return total.normalize()
        else:
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

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
