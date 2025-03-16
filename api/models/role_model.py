from django.db import models
from custom_viewset.models.abstracts import CommonInfoModel, SoftDeleteModel
from .outfit_model import Outfit
import auto_prefetch


class Role(SoftDeleteModel, CommonInfoModel):
    name = models.CharField()

    def __str__(self):
        return self.name