from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name is too Short"
        if postData['first_name'].isalpha() == False:
            errors['fname_alpha'] = "First name can only contain letters"


        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name is too Short"
        if postData['last_name'].isalpha() == False:
            errors['lname_alpha'] = "Last name can only contain letters"

        if len(postData['email']) < 5:
            errors['email'] = "Email is too Short"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not  EMAIL_REGEX.match(postData['email']):
            errors['email_format'] = "Not a valid email address"
        match = User.objects.filter(email=postData['email'])
        if len(match) > 0:
            errors['exists'] = "This account already exists"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too Short"
        if postData['password'] != postData['password_conf']:
            errors['match'] = "Passwords do not match"
        return errors
    
    # def login_validator (self, postData):


    
    # def login_validator:

class User(models.Model):
    first_name = models.CharField(max_length= 45)
    last_name = models.CharField(max_length= 45)
    email = models.CharField(max_length= 255)
    password = models.CharField(max_length= 45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()