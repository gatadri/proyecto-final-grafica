from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError('El email es requerido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('role', 'director')
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('director', 'Director'),
        ('profesor', 'Profesor'),
        ('padre', 'Padre'),
    ]

    nombre   = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    carnet   = models.CharField(max_length=50, blank=True)
    email    = models.EmailField(unique=True)
    numero   = models.CharField(max_length=20, blank=True)
    role     = models.CharField(max_length=20, choices=ROLES, default='profesor')
    activo   = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.role})'
