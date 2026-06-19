from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    @property
    def is_admin_role(self):
        return self.role == 'admin'

    @property
    def is_manager_role(self):
        return self.role in ['admin', 'manager']