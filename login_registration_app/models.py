from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def reg_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$")
        NAME_REGEX = re.compile('^[A-Za-z]{2,}$')

        if not NAME_REGEX.match(postData['first_name']):
            errors["fname"] = "First name should contain letters only and be at least 2 characters"
        if not NAME_REGEX.match(postData['last_name']):
            errors["lname"] = "Last name should contain letters only and be at least 2 characters" 
        
        if not postData['email']:
            errors["email"] = "Email is required"
        elif User.objects.filter(email=postData['email']):
            errors['email'] = "Email already exists"
        elif not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Invalid email address"

        if not postData['birthday']:
            errors['birthday'] = "Date of birth is required"
        elif datetime.strptime(postData['birthday'],'%Y-%m-%d') > datetime.today():
            errors["birthday"] = "Date of birth should be in the past"

        if not PASSWORD_REGEX.match(postData['password']):
            errors["password"] = "Password should be at least 8 characters, and contain at least one uppercase, one lowercase, one digit and one special character"
        if not postData['confirm_pw']:
            errors["confirm_password"] = "Please confirm password"
        elif postData['password'] != postData['confirm_pw']:
            errors["password_match"] = "Passwords don't match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


#This method creates the User object and stores the hashed password
def registration(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    birthday = request.POST['birthday']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=first_name, last_name=last_name, email=email, birthday=birthday, password=pw_hash)
    logged_user = User.objects.get(email=email)
    request.session['logged_user'] = logged_user.id

# this method checks if password entered at login matches the hashed password in DB
def is_authenticated(request, logged_user):
    return bcrypt.checkpw(request.POST['login_pw'].encode(), logged_user.password.encode())
