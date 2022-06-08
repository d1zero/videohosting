from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from authentication.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    username = models.CharField(verbose_name='Username', max_length=255, unique=True)
    date_of_creation = models.DateField(verbose_name='Date of creation', auto_now=False, auto_now_add=True)
    image = models.ImageField(verbose_name='Image', upload_to='users/images', blank=True)

    is_active = models.BooleanField(verbose_name='Activated', default=False)
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

