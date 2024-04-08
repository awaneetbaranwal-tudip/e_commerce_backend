from django.db import models
from products.models import Products
from base.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10,default=0)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"Cart - ID: {self.id}, User: {self.user}"
    class Meta:
        db_table = "cart"
