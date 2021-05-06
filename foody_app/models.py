from django.db import models
from datetime import datetime
from django_google_maps import fields as map_fields

from django.conf import settings
import re, bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['last_name'] = "Name must be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Name must be at least 2 characters long."
        if len(postData['password']) < 8:
            errors['password'] = "Password cannot be less than 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['match'] = "Passwords do not match."
        if len(postData['email']) < 6:
            errors['email'] = "email is too short"
        EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = "Email in wrong format"
        users_with_email = User.objects.filter(email=postData['email'])
        if len(users_with_email) >= 1:
            errors['dup'] = "Email taken, use another"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    followers= models.ManyToManyField("self", symmetrical=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images')

    objects = UserManager()


class RestaurantManager(models.Manager):
    def restaurant_validator(self, postData):
        errors = {}
        if len(postData['restaurant_name']) < 1:
            errors['restaurant_name'] = "Name must at least 5 characters long."
        if datetime.strptime(postData['date'], '%Y-%m-%d') < datetime.now():
            errors['date'] = 'Date should be future'

        return errors

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=45,blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    message = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="has_created_restaurant", on_delete=models.CASCADE)
    joined_by = models.ManyToManyField(User, related_name="join_restaurant")
    date = models.DateTimeField()
    time = models.TimeField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = RestaurantManager()

def full_name(self):
        return f"{self.first_name} {self.last_name}"
