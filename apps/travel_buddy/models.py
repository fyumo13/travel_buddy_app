from __future__ import unicode_literals
from django.db import models
from ..login_registration.models import User
from datetime import datetime
import re

# regex to test whether given date is in valid MM/DD/YYYY format
date_regex = re.compile(r'\d{1,2}\/\d{1,2}\/\d{4}')

class TripManager(models.Manager):
    # creates a Trip object given all user-inputted information is valid
    def add_trip(self, postData, user_id):
        # runs validation test
        errors = self.validate(postData)
        if not errors:
            planner = User.objects.get(id=user_id)
            start_date = datetime.strptime(postData['start_date'], '%m/%d/%Y')
            end_date = datetime.strptime(postData['end_date'], '%m/%d/%Y')
            trip = Trip.objects.create(
                destination=postData['destination'],
                description=postData['description'],
                start_date=start_date,
                end_date=end_date,
                planner=planner
            )
            return trip
        else:
            return errors

    # creates a new Traveler object for a specific trip
    def join_trip(self, trip_id, user_id, first_name, last_name):
        traveler = Traveler.objects.create(
            trip=Trip.objects.get(id=trip_id),
            user=User.objects.get(id=user_id),
            first_name=first_name,
            last_name=last_name
        )
        return traveler

    # tests whether the given destination, description, start date, and end date
    # are all valid and dates are future-dated
    def validate(self, postData):
        errors = []
        if len(postData['destination']) == 0:
            errors.append("Enter a destination!")
        if len(postData['description']) == 0:
            errors.append("Enter a description!")
        if not re.match(date_regex, postData['start_date']):
            errors.append("Start date is invalid!")
        if not re.match(date_regex, postData['end_date']):
            errors.append("End date is invalid!")
        else:
            start_date = datetime.strptime(postData['start_date'], '%m/%d/%Y')
            end_date = datetime.strptime(postData['end_date'], '%m/%d/%Y')
            today = datetime.now()
            today = datetime.replace(today, hour=0, minute=0, second=0, microsecond=0)
            if start_date == end_date:
                errors.append("Start date and end date cannot be the same!")
            if start_date <= today:
                errors.append("Start date cannot be on or before today!")
            if end_date <= today:
                errors.append("End date cannot be on or before today!")
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    start_date = models.DateField()
    end_date = models.DateField()
    planner = models.ForeignKey(User, related_name='user')
    travelers = models.ManyToManyField(User, through='Traveler')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __str__(self):
        return self.destination

class Traveler(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    trip = models.ForeignKey(Trip)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
