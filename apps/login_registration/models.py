from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

# regex to test whether given name contains letters only and contains at least 3 characters
name_regex = re.compile(r'[A-Za-z]{3,}')
# regex to test whether given email is valid
email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-z]*$')
# regex to test whether given password is at least 8 characters long
password_regex = re.compile(r'(?=.{8,})')

class UserManager(models.Manager):
    def register(self, postData):
        # runs validation test
        errors = self.validate(postData)
        # creates a hashed password
        # sets user authority level
        # and stores user information into a new User object
        if not errors:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=hashed_password
            )
            return user
        else:
            return errors

    # searches for Users matching the given email and tests whether the given
    # password matches the stored password
    def login(self, postData):
        user = User.objects.filter(email=postData['email'])
        if not user:
            return False
        if bcrypt.hashpw(postData['password'].encode(), user[0].password.encode()) != user[0].password.encode():
            return False
        else:
            return user[0]

    # deletes the session attached to the given user id
    def logout(self, session):
        del session
        return True

    # tests whether given user first name, last name, email, and password
    # are all valid
    def validate(self, postData):
        errors = []
        try:
            user = User.objects.get(email=postData['email'])
            errors.append("Email already exists! Please log in!")
        except:
            if not re.match(name_regex, postData['first_name']):
                errors.append("First name must be more than 3 characters!")
            if not re.match(name_regex, postData['last_name']):
                errors.append("Last name must be more than 3 characters!")
            if not re.match(email_regex, postData['email']):
                errors.append("Email must be more than 3 characters!")
            if not re.match(password_regex, postData['password']):
                errors.append("Password is invalid!")
            elif postData['password'] != postData['confirm_password']:
                errors.append("Passwords do not match!")
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
