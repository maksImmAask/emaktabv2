from django.contrib.auth.models import AbstractUser
from django.db import models
class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("director", "Director"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student",
    )

    @property
    def is_admin_role(self):
        return self.role == "admin"

    @property
    def is_director_role(self):
        return self.role == "director"

    @property
    def is_teacher_role(self):
        return self.role == "teacher"

    @property
    def is_student_role(self):
        return self.role == "student"