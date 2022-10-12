from email.policy import default
from mixins import *
from django.db import models
import uuid
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


from django.shortcuts import redirect
# Create your models here.
class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    otp = models.CharField(max_length=100, blank=True, null=True)
    uid=models.CharField(default=f'{uuid.uuid4}',max_length=200)

    
    
    def __str__(self):
        return self.user.username