from django.db import models
from custom_viewset.models.abstracts import CommonInfoModel
from custom_viewset.models.abstracts import SoftDeleteModel

class OutfitCategory(SoftDeleteModel, CommonInfoModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name