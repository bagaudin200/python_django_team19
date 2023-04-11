from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase


from app_cart.models import Cart, ProductInCart
from app_goods.models import Product, Image
from app_goods.services.product_services import ProductService
from app_order.models import Order
from app_order.services import OrderService

DELIVERY_TYPES = [
    ('regular', 'обычная доставка'),
    ('express', 'экспресс-доставка')
]


User = get_user_model()


class OrderServiceTestCase(TestCase):
    fixtures = ['fixtures/categories', 'fixtures/products', 'fixtures/images']

    def setUp(self):
        self.user = User.objects.create(full_name='TestUserName')
        self.product = Product.objects.get(id=1)
        self.order_service = OrderService(self.client)
        cart = Cart.objects.create(
            user=self.user
        )
        ProductInCart.objects.create(
            product=self.product,
            cart=cart,
            quantity=1,
        )
        self.Order = Order

    def test_get_info_about_delivery_and_payment(self):
        for i_num in range(2):
            delivery_name = self.Order.DELIVERY_TYPES_DICT.get(self.Order.DELIVERY_TYPES[i_num][1])
            payment_name = self.Order.PAYMENT_TYPES_DICT.get(self.Order.DELIVERY_TYPES[i_num][1])
            print(delivery_name)
            print(payment_name)


    # def test_check_update_quantity_product_true(self):
    #     cart = Cart.objects.create(
    #         user=self.user
    #     )
    #     product = ProductInCart.objects.create(
    #         product=Product.objects.get(id=1),
    #         cart=cart,
    #         quantity=1,
    #     )
    #     result = self.product_service.get_update_quantity_product()
    #     self.assertTrue(result)
    #     product.delete()
    #
    #     cart = Cart.objects.create(
    #         user=self.user
    #     )
    #     ProductInCart.objects.create(
    #         product=Product.objects.get(id=2),
    #         cart=cart,
    #         quantity=1,
    #     )
    #     result = self.product_service.get_update_quantity_product()
    #     self.assertFalse(result)
    #
    # def test_get_product_quantity(self):
    #     quantity = self.product.quantity
    #     result = self.product_service.get_product_quantity()
    #     self.assertEqual(quantity, result)
    #
    # def test_get_images(self):
    #     images = Image.objects.filter(product=self.product)
    #     result = self.product_service.get_images()
    #     self.assertEqual(type(images), type(result))
    #     self.assertEqual(images.count(), result.count())

# class OrderService:
#     """Сервис для работы с заказами"""
#
#     def __init__(self, request):
#         self.request = request
#         self.cart = CartServices(request).cart
#

#
#     def get_info_about_delivery_and_payment(self):
#         """Получение информации из сессии о типе доставки и оплаты"""
#         delivery_name = Order.DELIVERY_TYPES_DICT.get(self.request.session['delivery'])
#         payment_name = Order.PAYMENT_TYPES_DICT.get(self.request.session['payment'])
#         return delivery_name, payment_name
#
#     def get_total_price(self):
#         """Получение информации об общей стоимости заказа"""
#         total_price = self.cart.products.only('quantity', 'price').aggregate(total=Sum(F('quantity') *
#                                                                                        F('product__price')))[
#             'total']
#         if total_price < 100:
#             total_price += SiteSettings.load().standard_order_price
#         if self.request.session.get('delivery') == 'express':
#             total_price += SiteSettings.load().express_order_price
#         return total_price
#
#     def get_format_phone_number(self):
#         """Получение отформатированного номера телефона"""
#         if self.request.user.phoneNumber:
#             phone_number = '+7 ({}{}{}) {}{}{}-{}{}-{}{}'.format(
#                 self.request.user.phoneNumber[0],
#                 self.request.user.phoneNumber[1],
#                 self.request.user.phoneNumber[2],
#                 self.request.user.phoneNumber[3],
#                 self.request.user.phoneNumber[4],
#                 self.request.user.phoneNumber[5],
#                 self.request.user.phoneNumber[6],
#                 self.request.user.phoneNumber[7],
#                 self.request.user.phoneNumber[8],
#                 self.request.user.phoneNumber[9],
#             )
#             return phone_number
#         else:
#             return ''





















