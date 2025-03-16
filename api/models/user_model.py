from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from custom_viewset.models.abstracts import SoftDeleteModel

class CustomUser(AbstractUser, SoftDeleteModel):
    """
    Custom user model with soft-delete functionality.
    - Uses email for authentication
    - Has roles: 'user' (default) and 'admin'
    """

    username = models.CharField(max_length=150, unique=True, default="Aam")  # Username sebagai pengganti name
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(
        max_length=10,
        choices=[('user', 'User'), ('admin', 'Admin')],
        default='user'
    )

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username', 'phone_number']

    def get_related_objects(self):
        # Implement related object deletion if necessary
        return []
    
    def __str__(self):
        return self.username
