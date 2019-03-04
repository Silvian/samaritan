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


@login_required
def get_user_profile(request):
    if request.is_ajax:
        user = get_user(request)
        response = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "mobile_number": user.profile.mobile_number,
            "profile_image": user.profile.profile_pic.url
        }
        return JsonResponse(response)


@login_required
def update_user_profile(request):
    if request.method == 'POST':
        user = get_user(request)
        form = UserForm(request.POST or None, instance=user)
        profile_image = request.FILES['profile_image']
        if form.is_valid() and profile_image:
            user.profile.mobile_number = request.POST['mobile_number']
            user.profile.profile_pic = profile_image
            form.save()
            return JsonResponse(success_response)

        return JsonResponse(failure_response)
