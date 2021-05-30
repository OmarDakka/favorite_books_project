from django.db import models
import re
from datetime import date,datetime
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors["name"] = "First name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        date_time_obj = datetime. strptime(postData['birthday'], '%Y-%m-%d').date()
        if date_time_obj >= date.today():
            errors["date"] = "Date must be in the past" 
        
        return errors
    
    def login_validator(self,postData):
        errors = {}
        user= get_user(email = postData["email"])
        if user is None:
            print("user is none")
            errors["wrong"] = "Email is incorrect, please try again!"
            return errors 
        if user:
            if not bcrypt.checkpw(postData['password'].encode(),user.Password.encode()):
                errors["wrong"] = "Password is incorrect"
            return errors    

class users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    Birthday = models.DateField(default = date.today())
    email = models.CharField(max_length=255, unique=True)
    Password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


def create_users(first_name, last_name, email, Password,Birthday):
    user = users.objects.create(first_name=first_name, last_name=last_name, email=email, Password=Password, Birthday = Birthday)
    return user


def get_user(email):
    user = users.objects.filter(email=email)
    print("this user was grabbed")
    if not user:
        return None
    else :
        return user[0]
