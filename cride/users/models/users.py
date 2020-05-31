""" Users  models """

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from cride.utils.models import CRideModel


class User(CRideModel, AbstractUser):
    """
    User model

    This model extend from Django's AbstractUser and CRideModel. The username
    field is changed to email field, it has been added some extra fields.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        max_length=254,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be in the format +99999999. Up to 15 digits allowed'
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField(
        'client status',
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries'
            'Clients are the main type of user.'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email.'
    )

    def __str__(self):
        """ Return the Username """
        return self.username

    def get_short_name(self):
        """ Return the Username """
        return self.username
