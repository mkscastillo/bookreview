from django.db import models
import re, bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self,postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['fname'] = "First name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors['lname'] = "Last name should be at least 2 characters"
        if postData['birthday'] >= datetime.today().strftime('%Y-%m-%d'):
            errors['birthday'] = "Birthday is not in the past"
        if not EMAIL_REGEX.match(postData['email_r']):
            errors['email_r'] = "Please enter a valid email"
        if User.objects.filter(email=postData['email_r']):
            errors['email_r'] = "Email is taken"
        if len(postData['password_r']) < 8:
            errors['password_r'] = "Password should be at least 8 characters"
        if postData['password_r'] != postData['conf_password']:
            errors['conf_password_r'] = "Passwords must match"
        return errors
    
    def login_validator(self,postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email"
        else:
            user = User.objects.filter(email=postData['email']).first()
            if user:
                pw_hash = user.password
                if not bcrypt.checkpw(postData['password'].encode(), pw_hash.encode()):
                    errors['password'] = "Incorrect Password"
            else:
                errors['email'] = "Please check if you have registered"
        return errors

class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author,related_name="books_authored")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    user = models.ForeignKey(User, related_name="list_of_reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)