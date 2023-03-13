from app_cart.services import CartServices


def cart(request):
    return {'cart': CartServices(request)}