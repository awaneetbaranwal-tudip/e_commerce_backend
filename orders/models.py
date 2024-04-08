from django.db import models
from base.models import BaseModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from users.models import Address
User = get_user_model()

class Orders(BaseModel):
    PENDING = "P"
    COMPLETED = "C"
    STATUS_CHOICES = ((PENDING,_("pending")), (COMPLETED, _("completed")))
    price = models.IntegerField(default=0)
    buyer = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    # created_by = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE, null=True)
    shipping_address = models.ForeignKey(
        Address,
        related_name="shipping_orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    billing_address = models.ForeignKey(
        Address,
        related_name="billing_orders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    # orders = models.ForeignKey(Orders, related_name='master_orders', 
    #                            on_delete=models.CASCADE)
    class Meta:
        db_table = "orders"
    def __str__(self):
        return f"Orders - ID: {self.id}, User: {self.user}"    
    # def __str__(self):
    #     return f"Order - ID: {self.id}, Buyer: {self.buyer}"
