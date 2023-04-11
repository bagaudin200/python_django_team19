from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F

from app_cart.models import Cart, ProductInCart
from app_goods.models import Product
from app_users.models import User


class CartServices:

    def __init__(self, request):
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
                cart = Cart.objects.get(user=self.user, is_active=True)
            except ObjectDoesNotExist:
                cart = Cart.objects.create(user=self.user)
            self.qs = ProductInCart.objects.filter(cart=cart)
        else:
            # сохранить пустую корзину в сеансе
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save_in_db(self, cart: dict, user: User) -> None:
        """
        Перенос корзины из сессии в БД
        :param cart: корзина из сессии
        :param user: пользователь
        :return: None
        """
        try:
            cart_ = Cart.objects.get(user=user, is_active=True)
            cart_exists = True
        except ObjectDoesNotExist:
            cart_exists = False

        for key, value in cart.items():
            if cart_exists:
                try:
                    product = ProductInCart.objects.filter(cart=cart_).select_for_update().get(product=key)
                    product.quantity += cart[key]['quantity']
                    product.save()
                except ObjectDoesNotExist:
                    ProductInCart.objects.create(
                        product=Product.objects.get(pk=key),
                        cart=Cart.objects.filter(user=user, is_active=True).first(),
                        quantity=cart[key]['quantity']
                    )
            else:
                product = Product.objects.get(id=key)
                cart_ = Cart.objects.update_or_create(user=user)
                ProductInCart.objects.create(
                    product=product,
                    cart=cart_,
                    quantity=value['quantity'],
                )

    def add(self, product: Product, quantity: int = 1, update_quantity: bool = False) -> None:
        """
        Добавляет товар в корзину и обновляет его количество
        :param product: товар
        :param quantity: количество
        :param update_quantity: флаг, указывающий, нужно ли обновить товар (True) либо добавить его (False)
        :return: None
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

    def save(self) -> None:
        """
        Сохранение корзины в сессии
        :return: None
        """
        if not self.use_db:
            # обновить корзину сеансов
            self.session[settings.CART_SESSION_ID] = self.cart
            # пометить сеанс как «измененный», чтобы убедиться, что он сохранен
            self.session.modified = True

    def remove(self, product: Product) -> None:
        """
        Удаление товара из корзины
        :param product: товар
        :return: None
        """
        if self.use_db:
            product_ = self.qs.filter(product=product)
            if product_.exists():
                product_.delete()
        else:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

    def __iter__(self):
        """
        Перебор товаров из корзины
        :return:
        """
        # if self.use_db:
        #     return self.cart.products.all()

        product_ids = self.cart.keys()
        # получить объекты продукта и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:
        """
        Считает количество товаров в корзине
        :return: количество товаров в корзине
        """
        if self.use_db:
            result = ProductInCart.objects.filter(cart=self.cart).aggregate(Sum('quantity'))['quantity__sum']
            return result if result else 0
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        """
        Считает итоговую цену товаров корзины
        :return: цена товаров в корзине
        """
        if self.use_db:
            total = self.qs.only('quantity', 'price').aggregate(total=Sum(F('quantity') * F('product__price')))['total']
            if not total:
                total = Decimal('0')
            return total.quantize(Decimal('1.00'))
        else:
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self, only_session: bool = False) -> None:
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
