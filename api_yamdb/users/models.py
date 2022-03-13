from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import EmailValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Сохраняет пользователя только с емаил, ником, паролем
        """
        if not email:
            raise ValueError('Необходимо указать email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.Roles.ADMIN)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    class Roles(models.Model):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'
        ROLES_CHOICES = [
            (USER, USER),
            (MODERATOR, MODERATOR),
            (ADMIN, ADMIN),
        ]

    roles = models.CharField(
        verbose_name='Роли пользователей',
        help_text='Вот такие вот бывают',
        max_length=20,
        choices=Roles.ROLES_CHOICES,
        default=Roles.USER,
    )

    username = models.CharField(
        verbose_name='Никнейм',
        help_text='По русски - погоняло',
        blank=False,
        unique=True,
        max_length=30,
    )
    email = models.EmailField(
        verbose_name='Почта',
        help_text='Почта@почта.ru',
        blank=False,
        unique=True,
        validators=(EmailValidator,),
        max_length=254,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        help_text='Как мама с папой назвали?',
        blank=True,
        max_length=30,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Скорее всего как у папы',
        blank=True,
        max_length=50,
    )
    bio = models.TextField(
        verbose_name='О себе',
        help_text='Чем живешь, что ешь?',
        blank=True,
        max_length=500,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        help_text='Даёт разные разрешения',
        max_length=30,
        default=Roles.USER,
        choices=roles.choices,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    objects = UserManager()

    @property
    def is_user(self):
        return self.role == User.Roles.USER

    @property
    def is_admin(self):
        return self.role == User.Roles.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.Roles.MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
