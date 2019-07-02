from django.db import models


# class Order(models.Model):
#     PROCEEDED = 'PRD'
#     ACCEPTED = 'ACP'
#     REJECTED = 'RJC'
#     PAID = 'PD'
#     READY = 'RDY'
#     CANCELED = 'CND'
#
#     ORDER_STATUS_CHOICES = (
#         (PROCEEDED, 'обрабатывается'),
#         (ACCEPTED, 'принят'),
#         (REJECTED, 'отклонен'),
#         (PAID, 'оплачен'),
#         (READY, 'готов к выдаче'),
#         (CANCELED, 'отменен'),
#     )
#
#     consumer = models.ForeignKey(
#         'feeduser.FeedUser',
#         on_delete=models.CASCADE
#     )
#
#     created = models.DateTimeField(
#         auto_now_add=True
#     )
#
#     modified = models.DateTimeField(
#         auto_now=True
#     )
#
#     status = models.CharField(
#         max_length=3,
#         choices=ORDER_STATUS_CHOICES,
#         default=PROCEEDED
#     )
#
#     is_active = models.BooleanField(
#         default=True,
#         db_index=True,
#     )
#
#     def total_price(self):
#         meals = self.meals.select_related('meal')
#         return sum(list(map(lambda meal: meal.item_price * meal.quantity, meals)))
#
#     def delete(self, using=None, keep_parents=False):
#         self.is_active = False
#         self.status = 'CND'
#         self.save()
#
#     def __str__(self):
#         return f'ordered by {self.consumer}, cooking by {self.chef}'
#
#     def __repr__(self):
#         return f'ordered by {self.consumer}, cooking by {self.chef}'


class OrderItem(models.Model):
    PROCEEDED = 'PRD'
    ACCEPTED = 'ACP'
    REJECTED = 'RJC'
    PAID = 'PD'
    READY = 'RDY'
    CANCELED = 'CND'

    ORDER_STATUS_CHOICES = (
        (PROCEEDED, 'обрабатывается'),
        (ACCEPTED, 'принят'),
        (REJECTED, 'отклонен'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (CANCELED, 'отменен'),
    )

    consumer = models.ForeignKey(
        'feeduser.FeedUser',
        on_delete=models.CASCADE
    )

    meal = models.ForeignKey(
        'menu.Meal',
        on_delete=models.CASCADE
    )

    chef = models.ForeignKey(
        'feeduser.ProducerProfile',
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    modified = models.DateTimeField(
        auto_now=True
    )

    status = models.CharField(
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=PROCEEDED
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    @property
    def item_price(self):
        return self.meal.price * self.quantity

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.status = 'CND'
        self.save()

    def __str__(self):
        return f'{self.meal.title} / {self.consumer} / {self.chef}'
