from django.db import models


class CommonInfoModel(models.Model):
    """
    Abstract model that adds additional timestamp regarding model creation/updation
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
