from __future__ import unicode_literals
from ..login.models import User
from django.db import models
from datetime import date, datetime
from dateutil.parser import parse as parse_date

class TripManager(models.Manager):
    def make_trip(self, request):
        errors = self.validate_trip(request)

        if errors:
            return errors

        planner = User.objects.get(id=request.session['user']['user_id'])
        self.create(destination=request.POST['destination'], plan=request.POST['plan'], start_date=request.POST['start_date'], end_date=request.POST['end_date'],planner=planner)
        return errors

    def validate_trip(self,request):
        errors = []
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        try:
            start = parse_date(start_date).date()
            end = parse_date(end_date).date()
            if start > end:
                errors.append('End date cannot be before start date')
            if start <= date.today():
                errors.append('Start date cannot be in the past.')
            if end <= date.today():
                errors.append('End date cannot be in the past.')
            if not request.POST['destination']:
                errors.append('Destination cannot be blank.')
            if not request.POST['plan']:
                errors.append('Please tell us more about the plan.')
        except ValueError:
            if not request.POST['start_date']:
                errors.append('Please select a start date.')
            elif not request.POST['end_date']:
                errors.append('Please select an end date.')
            else:
                errors.append('Please select a start and end date.')
            return(errors)

        if not request.POST['destination']:
            errors.append('Destination cannot be blank.')
        if not request.POST['plan']:
            errors.append('Please tell us more about the plan.')
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    plan = models.CharField(max_length=255)
    travelers = models.ManyToManyField(User, related_name='user_trips')
    planner = models.ForeignKey(User, related_name='planned_trip')
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()