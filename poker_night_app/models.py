from django.db import models
from log_reg_app.models import *

# Create your models here.
class EventManager(models.Manager):

    def tournament_validator(self, postData):
        errors = {}
        
        if len(postData['street']) < 5:
            errors['street'] = "Street address is too Short"
        if len(postData['state']) != 2:
            errors['state'] = "State must be at least 2 characters"
        if len(postData['zip_code']) != 5:
            errors['zip_code'] = "Zip code must be 5 characters"
        if len(postData['style']) <1:
            errors['type'] = "Type of Tournament cannot be blank"
        if len(postData['buy_in']) <1:
            errors['buy_in'] = "Buy-in cannot be blank"
        if len(postData['re_entries']) <1:
            errors['re_entries'] = "Number of re-entries cannot be blank"
        if len(postData['levels']) <1 or len(postData['levles']) >3 :
            errors['levels'] = "Level Duration must be between 1 and 3 digits"
        if len(postData['max_players']) <1 or postData['max_players'] < 2 :
            errors['levels'] = "Maximum number of players must be greater than 1"
        return errors

    def cash_game_validator(self, postData):
        errors = {}
        
        if len(postData['street']) < 5:
            errors['street'] = "Street address is too Short"
        if len(postData['state']) != 2:
            errors['state'] = "State must be at least 2 characters"
        if len(postData['zip_code']) != 5:
            errors['zip_code'] = "Zip code must be 5 characters"
        if len(postData['s_blind']) <1:
            errors['s_blind'] = "Small Blind cannot be blank"
        if len(postData['b_blind']) <1:
            errors['s_blind'] = "Big Blind cannot be blank"
        if len(postData['min_buy']) <1:
            errors['min_buy'] = "Minimum buy-in cannot be blank"
        if len(postData['max_buy']) <1:
            errors['max_buy'] = "Minimum buy-in cannot be blank"
        if len(postData['max_players']) <1 or postData['max_players'] < 2 :
            errors['levels'] = "Maximum number of players must be greater than 1"
        return errors



    


class Event(models.Model):
    street = models.CharField(max_length=255)
    street_two = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.IntegerField()
    scheduled_for = models.DateTimeField(auto_now=False)
    max_players = models.IntegerField()
    notes = models.TextField()
    hosted_by = models.ForeignKey(User, related_name="events", on_delete = models.CASCADE)
    attendees = models.ManyToManyField(User, related_name="events_attending")
    is_full = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()

class Tournament(models.Model):
    style = models.CharField(max_length=255)
    buy_in = models.DecimalField( max_digits=9, decimal_places=2)
    re_entries = models.IntegerField()
    levels = models.IntegerField()
    event = models.OneToOneField(Event, related_name="tournament", on_delete = models.CASCADE, null=True, blank=True)
    objects = EventManager()

class Cash_game(models.Model):
    stakes = models.CharField(max_length=7)
    min_buy = models.DecimalField( max_digits=9, decimal_places=2)
    max_buy = models.DecimalField( max_digits=9, decimal_places=2)
    event = models.OneToOneField(Event, related_name="cash_game", on_delete = models.CASCADE, null=True, blank=True)
    objects = EventManager()

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    parent_event = models.ForeignKey(Event, related_name="comments", on_delete = models.CASCADE)

class Reply(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="replies", on_delete = models.CASCADE)
    parent_event = models.ForeignKey(Event, related_name="replies", on_delete = models.CASCADE)
    parent_comment = models.ForeignKey(Comment, related_name="replies", on_delete = models.CASCADE)
