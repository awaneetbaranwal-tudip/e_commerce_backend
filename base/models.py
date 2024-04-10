from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now,blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(blank=True, null=True)
    modified_by = models.IntegerField(blank=True, null=True)
    class Meta:
        abstract = True
