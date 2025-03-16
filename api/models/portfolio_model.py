from django.db import models
from custom_viewset.models.abstracts import CommonInfoModel, SoftDeleteModel
import auto_prefetch


class Portfolio(SoftDeleteModel, CommonInfoModel):
    outfit = auto_prefetch.ForeignKey('Outfit', on_delete=models.CASCADE, db_constraint=False)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    image = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name