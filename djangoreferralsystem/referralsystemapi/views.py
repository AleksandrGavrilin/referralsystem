from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError, JsonResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.db.models import Q
from .models import User, PhoneCode
from phonenumber_field.validators import validate_international_phonenumber
from time import sleep
from random import randint, choices
from string import ascii_lowercase, digits



# Conditional sending of an authorization code (for testing purposes).

def send_sms(phone_number, code):
    print(f'Ваш код для авторизации: {code}')
    sleep(2)



# Generating a random authorization code.

def get_random_code():
    return randint(1000, 9999)



# Create an invite code.

def get_ivite_code():
    string_init = ascii_lowercase + digits
    code_invite = ''.join(choices(string_init, k=6))
    return code_invite



# Sending an authorization code, adding a user (phone number) to the database "Phonecode".
def phone_auth(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phonenumber', None)
        if phone_number is None:
            return HttpResponseBadRequest("Phone number required!")
        try:
            validate_international_phonenumber(phone_number)
        except:
            return HttpResponseBadRequest("Phone number isn't correct!")
        new_code = get_random_code()
        try:
            PhoneCode.objects.get(phone=phone_number)
            return HttpResponseNotAllowed("Phone is already used.")
        except ObjectDoesNotExist:
            PhoneCode.objects.create(phone=phone_number, code=new_code)
            send_sms(phone_number=phone_number, code=new_code)
            return HttpResponse('OK')
        except DatabaseError:
            return HttpResponseServerError('Error of data base.')
    else:
        return HttpResponseBadRequest('Only method "GET" supported.')



# Sending an invitation code, adding a user (phone number, invite code) to the "User" database.

def phone_code(request):
    if request.method == 'GET':
        phone_code = request.GET.get('phonecode', None)
        phone_number = request.GET.get('phonenumber', None)
        if phone_code is None:
            return HttpResponseBadRequest('Code requried!')
        if phone_number is None:
            return HttpResponseBadRequest('Phone number required!')
        try:
            validate_international_phonenumber(phone_number)
        except:
            return HttpResponseBadRequest("Phone number isn't correct!")
        try:
            user_code = PhoneCode.objects.get(phone=phone_number)
            if str(user_code.code) == phone_code:
                new_invite = get_ivite_code()
                User.objects.create(phone=phone_number,invite_code=new_invite, referral_code=None)
                return JsonResponse({'referralcode': new_invite})
            else:
                return HttpResponseForbidden("Сode does not match!")
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Unknown phone number.")
        except DatabaseError:
            return HttpResponseServerError('Error of data base.')
    else:
        return HttpResponseBadRequest('Only method "GET" supported.')



# Processes the received invite code.

def invite(request):
    if request.method == 'GET':
        user_code = request.GET.get('usercode', None)
        phone_number = request.GET.get('phonenumber', None)
        invite_code = request.GET.get('invitecode', None)
        if user_code is None:
            return HttpResponseBadRequest('Code requried!')
        if phone_number is None:
            return HttpResponseBadRequest('Phone number required!')
        if invite_code is None:
            return HttpResponseBadRequest('Invite code required!')
        try:
            current_user = User.objects.get(Q(invite_code=user_code) & Q(phone=phone_number))
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("This user doesn't exist!")
        except DatabaseError:
            return HttpResponseServerError("Error of data base.")
        if current_user.referral_code is None:
            try:
                invite_user = User.objects.get(invite_code=invite_code)
                current_user.referral_code = invite_user
                current_user.save(update_fields=['referral_code'])
                return HttpResponse('referral code entered successfully!')
            except ObjectDoesNotExist:
                return HttpResponseBadRequest("Unknown user.")
            except DatabaseError:
                return HttpResponseServerError("Error of data base.")
        else:
            return HttpResponseBadRequest('this user has already used the invite code!')
    else:
        return HttpResponseBadRequest('Only method "GET" supported.')



# Providethis user has already used the invite codest of invited users.

def getreferrals(request):
    if request.method == 'GET':
        user_code = request.GET.get('usercode', None)
        phone_number = request.GET.get('phonenumber', None)
        if phone_number is None:
            return HttpResponseBadRequest('Phone number required!')
        if user_code is None:
            return HttpResponseBadRequest('Code requried!')
        try:
            current_user = User.objects.get(Q(invite_code=user_code) & Q(phone=phone_number))
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("This user doesn't exist!")
        except DatabaseError:
            return HttpResponseServerError("Error of data base.")
        try:
            referral_users_list = User.objects.filter(referral_code=current_user)
            return JsonResponse({'phonelist': [str(user.phone) for user in referral_users_list]})
        except DatabaseError:
            return HttpResponseServerError ("Error of data base.")
    else:
        return HttpResponseBadRequest('Only method "GET" supported.')
        


