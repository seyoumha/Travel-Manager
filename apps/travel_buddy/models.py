from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Name souuld be more than 2 characters"
        if len(postData['username']) < 2:
            errors["username"] = "Last should be more than 2 characters"    
        if postData['password'] != postData['conf_pw']:
            errors['password_confirm']= "Password and confirm pw must match"
        if len(postData['password']) < 8:
            errors['password'] = "Password shoud be more than 8 characters."
        return errors

    def password_validator(self, postData):
        errors={}
        if len(postData['username']) < 2:
            errors["username"] = "Last should be more than 2 characters" 
        if len(postData['password']) < 8:
            errors['password'] = "Password shoud be more than 8 characters."
        return errors
class TravelManager(models.Manager):
    def travel_add_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors["destination"] = "Destination cannot be blank"
        if len(postData['plan']) < 1:
            errors["plan"] = "Description cannot be blank"    
        if len(postData['from']) < 1:
            errors['from'] = "Please add from date"
        if len(postData['to']) < 1:
            errors['to'] = "Please add to date"
        if postData['to'] < postData['from']:
            errors['travel_dates'] = "Travel from date has to be before travel to date"

        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add = True)
    objects = UserManager()
class Travel(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_at = models.DateField(auto_now_add = True)
    user = models.ForeignKey(User, related_name = "travel")
    objects = TravelManager()
class Trips(models.Model):
    user = models.ForeignKey(User, related_name = "traveler")
    travler = models.ForeignKey(Travel, related_name = "travels")

