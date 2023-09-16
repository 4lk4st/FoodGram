from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _

from backend.settings import EMAIL_LENGTH, NAME_LENGTH
from .managers import FoodUserManager


class FoodUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        max_length=EMAIL_LENGTH,
    )
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='name',
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain '
                                        'only letters, numbers '
                                        'and @/./+/-/_ characters.'),
                                      'invalid'), ],
    )
    first_name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='first name'
    )
    last_name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='last name'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    objects = FoodUserManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.email


class Subscription(models.Model):
    user = models.ForeignKey(
        FoodUser,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    subscription = models.ForeignKey(
        FoodUser,
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    class Meta:
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscription'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user} ->>> {self.subscription}'
