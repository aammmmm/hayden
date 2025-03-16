from django.db import models
from custom_viewset.models.abstracts import CommonInfoModel, SoftDeleteModel

class Package(SoftDeleteModel, CommonInfoModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.JSONField(default=list)

    def __str__(self):
        return self.name