"""
This is the main user profile file for Samaritan CMA app

@author: Silvian Dragan
@Date: 06/12/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Please note: All methods and classes in here must be secure (i.e. use @login_required decorators)
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.http import JsonResponse

from api.views import success_response, failure_response
from authentication.forms import UserForm
from authentication.models import MFAConfiguration, MFACode, MFACookie
from messageservice.tasks import send_sms_task


@login_required
def get_user_profile(request):
    if request.is_ajax:
        user = get_user(request)
        response = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "mfa_enabled": user.profile.mfa_enabled,
            "mobile_number": user.profile.mobile_number,
            "profile_image": user.profile.profile_pic.url,
        }
        return JsonResponse(response)


@login_required
def update_user_profile(request):
    if request.method == 'POST':
        user = get_user(request)
        form = UserForm(request.POST or None, instance=user)
        if form.is_valid():
            user.profile.mobile_number = request.POST['mobile_number']
            profile_image = request.FILES.get(['profile_image'][0], default=None)
            if profile_image:
                user.profile.profile_pic = profile_image
            form.save()
            return JsonResponse(success_response)

        return JsonResponse(failure_response)


@login_required
def send_mfa_code(request):
    if request.is_ajax:
        user = get_user(request)
        mfa_config = MFAConfiguration.load()
        if mfa_config and mfa_config.active:
            if user.profile.mobile_number:
                # generate the mfa code and send sms to the user
                mfa_code = MFACode.objects.create(user=user)
                message = "One time code: {}".format(mfa_code.calculate_six_digit_code())
                send_sms_task.delay(
                    message=message,
                    phone=user.profile.mobile_number,
                )
                return JsonResponse(success_response)

        return JsonResponse(failure_response)


def verify_mfa_code(request):
    if request.method == 'POST':
        user = get_user(request)
        mfa_code = MFACode.objects.filter(user=user).last()
        if mfa_code:
            if not mfa_code.expired:
                if request.POST['code'] == mfa_code.calculate_six_digit_code():
                    user.profile.mfa_enabled = True
                    user.save()
                    return JsonResponse(success_response)

        return JsonResponse(failure_response)


def disable_mfa(request):
    if request.method == 'POST':
        user = get_user(request)
        MFACookie.objects.filter(user=user).delete()
        user.profile.mfa_enabled = False
        user.save()
        return JsonResponse(success_response)
