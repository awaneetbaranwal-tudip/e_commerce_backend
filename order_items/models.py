from django.db import models
from products.models import Products
from base.models import BaseModel
from orders.models import Orders

class OrderItems(BaseModel):

    price = models.IntegerField(default=0)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(null = True)
    # orders = models.ForeignKey('order_items.OrderItems', on_delete=models.CASCADE, related_name='order_items_for_orders',null = True)
    orders = models.ForeignKey(
        Orders, related_name="order_items", on_delete=models.CASCADE, null =True
    )

    def __str__(self):
        return f"Order - ID: {self.id}, User: {self.user}"
    class Meta:
        db_table = "order_items"


