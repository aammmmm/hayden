from django.db import models
from custom_viewset.models.abstracts import CommonInfoModel, SoftDeleteModel
import auto_prefetch


class Transaction(SoftDeleteModel, CommonInfoModel):
    outfit = auto_prefetch.ForeignKey('Outfit', on_delete=models.CASCADE, db_constraint=False)
    user = auto_prefetch.ForeignKey('CustomUser', on_delete=models.CASCADE)
    package = auto_prefetch.ForeignKey('Package', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    total_usher = models.IntegerField()
    event_date = models.DateField()
    venue = models.CharField(max_length=255)
    wo = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.IntegerField()
    payment_status = models.CharField(max_length=50)