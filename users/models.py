from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from phone_field import PhoneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
    is_doctor = models.BooleanField(default=True)
    

    middle_name = models.CharField(
        _("Middle Name"), max_length=5000, null=True, blank=True
    )

class Doctor(models.Model):
    now = timezone.now()
    fullname= models.CharField(_("Fullname"), max_length=500, blank=True,null=True)
    user = models.OneToOneField(
        User, verbose_name=_("Doctor"), on_delete=models.CASCADE, primary_key=True
    )
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    specialty = models.CharField(
        _("Specialty"), max_length=5000, blank=False, null=False
    )
    hpname = models.CharField(
        _("Hospital Name"), max_length=5000, null=False, blank=False
    )
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    user.is_doctor = True
    staff = models.BooleanField(default=True)
    superuser = models.BooleanField(default=False)
    admin = models.BooleanField(default= False)
    active = models.BooleanField(default=True)
    last_login = now
    date_joined = now


class Patient(models.Model):


    email = models.EmailField(
        _("Email address"), max_length=254, null=False, blank=True
    )
    birthday = models.DateField(_("Date of birth"))
    fullname = models.CharField(_("Fullname"), max_length=255, unique=True)
    phonenumber = PhoneField()
    age = models.IntegerField(_("Age"))
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    

    def __str__(self):
        return "%s" % (self.fullname)



class Questionaire(models.Model):

    date_added = models.DateTimeField(auto_now_add=True)
    


class Comment(models.Model):

    date_added = models.DateTimeField(auto_now_add=False)
    comment = models.TextField(_("recommendation"), max_length=16383)
    

