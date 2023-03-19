from django.db import models

from app_order.models import Order


class Payment(models.Model):
    """Модель оплаты заказа"""

    REASON_INSUFFICIENT_FUNDS = 'insufficient funds'
    REASON_NO_CONTACT_WITH_BANK = 'no contact with the bank'
    REASON_CARD_BLOCKED = 'card blocked'
    REASON_NONE = ''
    REASONS = [
        (REASON_INSUFFICIENT_FUNDS, 'недостаточно средств'),
        (REASON_NO_CONTACT_WITH_BANK, 'нет связи с банком'),
        (REASON_CARD_BLOCKED, 'карта заблокирована'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name='order')
    reason_for_non_payment = models.CharField(max_length=100, choices=REASONS, default=REASON_NONE,
                                              verbose_name='reason for non payment')

    class Meta:
        db_table = 'payment'
        verbose_name = 'payment'
        verbose_name_plural = 'payments'

    def __str__(self):
        return f"Payment for order #{self.order_id}"
