from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from user.choices import USER_TYPE_CHOICES, REGIONS

# Create your models here.
from user.choices import USER_TYPE_CHOICES
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.user_type = 'user'
        user.save()
        return user

    def _create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(username=username, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.user_type = 'user'
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(_('Фото профиля'), upload_to='user_avatar/', null=True, blank=True)
    created = models.DateField(_('Дата создания'), auto_now_add=True, null=True, blank=True)
    updated = models.DateField(_('Дата обновления'), auto_now_add=True, null=True, blank=True)
    username = models.CharField(_('Логин'), max_length=255, unique=True)
    fullname = models.CharField(_('Полное имя'), max_length=255, null=True, blank=True)
    lang = models.CharField(_('Язык'), max_length=255, default='ru')
    user_region = models.CharField(_('Регионы'), max_length=255, choices=REGIONS)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    user_type = models.CharField(_('Тип пользователя'),
                                 max_length=25,
                                 choices=USER_TYPE_CHOICES,
                                 default='agent')
    date_joined = models.DateTimeField(auto_now_add=False,
                                       null=True,
                                       blank=True)
    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def __str__(self):
        return str(self.fullname)

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class Deliver(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE,
                             verbose_name='Ползователь',
                             related_name='deliver')
    service_percent = models.FloatField(verbose_name='Пацент услуги достовшика', default=0)
    balance = models.FloatField(verbose_name='Баланс', default=0)

    class Meta:
        verbose_name = 'Доставщик'
        verbose_name_plural = 'Доставщики'


class Agent(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE,
                             verbose_name='Ползователь',
                             related_name='agent')
    service_percent = models.FloatField(verbose_name='Пацент услуги агента', default=0)
    balance = models.FloatField(verbose_name='Баланс', default=0)

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'
