from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db import models
import datetime

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    email_otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']




class MonthlyPick(models.Model):
    MONTH_CHOICES = [(str(i), datetime.date(1900, i, 1).strftime('%B')) for i in range(1, 13)]

    month = models.CharField(max_length=2, choices=MONTH_CHOICES)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='top_destinations/', blank=True, null=True)

    class Meta:
        verbose_name = "Monthly Destination Pick"
        verbose_name_plural = "Monthly Destination Picks"
        ordering = ['month']

    def __str__(self):
        return f"{self.city}, {self.country} ({self.get_month_display()})"



class Tour(models.Model):
    TOUR_TYPES = [
        ('adventure', 'Adventure'),
        ('leisure', 'Leisure'),
        ('family', 'Family'),
        ('cultural', 'Cultural'),
    ]
    FOOD_CHOICES = [('veg', 'Veg'), ('nonveg', 'Non-Veg'), ('both', 'Both')]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    food_type = models.CharField(max_length=10, choices=FOOD_CHOICES)
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPES)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    availability_date = models.DateField()
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='tours/')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
