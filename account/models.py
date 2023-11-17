from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser




# Create your models here.
class User(AbstractUser):
    # phone_number = PhoneNumberField(blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)
    division = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True, max_length=100000, default='', blank=True)

    # REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number', 'street_address', 'district', 'division', 'is_staff', 'image']
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'street_address', 'district', 'division', 'is_staff', 'image']

    def __str__(self) -> str:
        if self.first_name and self.last_login:
            name = f'{self.first_name} {self.last_name}'
        else: 
            name = f'{self.username}'
        return name


