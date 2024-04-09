from django.db import models
from base.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        db_table="catogries"


def get_default_product_category():
    return Category.objects.get_or_create(name="Others")[0]

class Products(BaseModel):
    seller = models.ForeignKey(User, related_name="products", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        related_name="product_list",
        on_delete=models.SET(get_default_product_category),
    )
    name = models.CharField(max_length=200)
    desc = models.TextField(("Description"), blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
    class Meta:
        db_table="product"