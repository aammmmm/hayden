from django.db import models
from custom_viewset.models.abstracts import SoftDeleteModel, CommonInfoModel
import auto_prefetch


class Outfit(SoftDeleteModel, CommonInfoModel):
    outfit_category = auto_prefetch.ForeignKey('OutfitCategory', on_delete=models.CASCADE, db_constraint=False)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    image = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name