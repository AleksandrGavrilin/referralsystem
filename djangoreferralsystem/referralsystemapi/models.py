from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    phone = PhoneNumberField(blank=False, null=False)
    invite_code = models.CharField(max_length=6,blank=False, null=False)
    referral_code = models.ForeignKey('self',blank=True, null=True, on_delete=models.DO_NOTHING)


class PhoneCode(models.Model):
    phone = PhoneNumberField(blank=False, null=False)
    code = models.PositiveSmallIntegerField(blank=False, null=False)
