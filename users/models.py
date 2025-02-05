from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('alumno', 'Alumno'),
        ('profesor', 'Profesor'),
    )

    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=10, choices=ROLES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []