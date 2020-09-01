from django.db import models
import re, bcrypt
from datetime import datetime, timedelta

# Create your models here.
class UserManager(models.Manager):
    def registerVal(self, postData):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['firstName']) < 1:
            errors['firstName'] = "Enter First Name"
        if len(postData['lastName']) < 1:
            errors['lastName'] = "Enter Last Name"
        if not EMAIL_REGEX.match(postData['email']): 
            errors['emailpattern'] = "Invalid Email Address" 
        user = User.objects.filter(email=postData['email'])
        if user:
            register_user = user[0]
            errors['existid'] ="Eamil Address is already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['confirm'] != postData['password']:
            errors['confirm'] = "Password and confirm PW must match"
        return errors

    def loginVal(self, postData):
        errors= {}
        user = User.objects.filter(email=postData['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                pass
            else:
                errors['wrongpw'] ="Password does not match"
        else:
            errors['unregistered'] = "User not registered. Try agian"
        return errors

    def updateVal(self, postData):
        errors= {}
        if len(postData['password']) < 1:
            errors['password'] = "Enter Current Password"
        if len(postData['newpw']) != 0:
            if len(postData['newpw']) < 8:
                errors['newpw'] = "Password must be at least 8 characters"
        if postData['confirm'] != postData['newpw']:
            errors['confirm'] = "New Password and confirm PW must match"
        return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    hometown = models.CharField(max_length=255, default = None, blank=True, null=True)
    work = models.CharField(max_length=255, default = None, blank=True, null=True)
    home = models.CharField(max_length=255, default = None, blank=True, null=True)
    cover = models.ImageField(upload_to="", default='/coverdefault.jpg', blank=True, null=True)
    pic = models.ImageField(upload_to="", default='/Default.png', blank=True, null=True)
    relationships = models.ManyToManyField('User', through='Friend', symmetrical=False, related_name='friends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    content = models.TextField(max_length=255)
    image = models.FileField(upload_to="", default=None, blank=True, null=True)
    p_creater = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    p_to = models.ForeignKey(User, related_name="post_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Comment(models.Model):
    content = models.TextField(max_length=255)
    c_creater = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    c_message = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Friend(models.Model):
    creater = models.ForeignKey(User, related_name="friend", on_delete=models.CASCADE)
    flist = models.ForeignKey(User, related_name="friendlist", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
