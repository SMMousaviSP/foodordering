from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    city = models.CharField(max_length=255)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Restaurant(models.Model):
    manager = models.OneToOneField(User, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, blank=False, null=False)
    food_type = models.CharField(max_length=255, blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=1024, blank=False, null=False)
    open_time = models.TimeField(blank=False, null=False)
    close_time = models.TimeField(blank=False, null=False)


class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, blank=False, null=False)
    current_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    is_organic = models.BooleanField(default=False, blank=False, null=False)
    is_vegan = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return "<{}: {}$>".format(self.name, self.current_price)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    foods = models.ManyToManyField(Food)
    is_accepted = models.BooleanField(default=False, blank=False, null=False)
    time_to_deliver = models.IntegerField(
        validators=[MinValueValidator(1)], blank=False, null=False, default=30
    )
