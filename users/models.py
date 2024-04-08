from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from base.models import BaseModel
from django_countries.fields import CountryField

User = get_user_model()

class Address(BaseModel):
    # Address options
    BILLING = "B"
    SHIPPING = "S"

    ADDRESS_CHOICES = ((BILLING, _("billing")), (SHIPPING, _("shipping")))

    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=10, null= True)
    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()