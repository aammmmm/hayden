# from django.db import models

# from custom_viewset.utils.user_threading_util import get_current_user


# class UserTrackingModel(models.Model):
#     """
#     Abstract model that adds additional fields to a model regarding model creation/updation related user

#     Related user usually can be:
#     - "udomain - display_name" (most of the time)
#     - "AnonymousUser" (if allowed anonymous alteration)
#     - "Api Key" or "Api Key appname" (if allowed api key alteration)
#     - "" (empty string, rarely happens, usually from misconfiguration of user_threading_middleware)
#     """

#     created_by = models.TextField(blank=True)
#     updated_by = models.TextField(blank=True)

#     def set_created_updated_by(self):
#         """
#         This method must be called in the `save` method in the related class.
#         Otherwise, `created_by` and `updated_by` won't be processed
#         """
#         current_user: str = get_current_user()

#         # id exists, model already in database
#         if self.id:
#             self.updated_by = current_user  # do update

#         # id not exists, model not in database
#         else:
#             self.created_by = current_user  # do create

#     class Meta:
#         abstract = True
