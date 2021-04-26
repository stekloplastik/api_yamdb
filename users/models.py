from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    CUSTOMUSER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = ((CUSTOMUSER, 'user'),
             (MODERATOR, 'moderator'),
             (ADMIN, 'admin')
             )

    username = models.CharField(
        verbose_name="Никнейм", unique=True, max_length=100
    )

    email = models.EmailField(verbose_name="Почта", null=False, unique=True)

    role = models.CharField(
        verbose_name="Права(установлены админом)",
        choices=ROLES, default=CUSTOMUSER, max_length=15
    )
    bio = models.TextField(verbose_name="О себе", max_length=300, blank=True)
    first_name = models.TextField(
        verbose_name="Имя", max_length=100, blank=True
    )
    last_name = models.TextField(
        verbose_name="Фамилия", max_length=100, blank=True
    )
    confirmation_code = models.CharField(max_length=10, default='0000000000')

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_upperclass(self):
        return self.role in (self.MODERATOR, self.ADMIN)

    class Meta:
        ordering = ['id']
