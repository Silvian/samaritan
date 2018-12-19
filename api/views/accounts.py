"""
This is the main user accounts file for Samaritan CMA app

@author: Silvian Dragan
@Date: 27/11/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Please note: All methods and classes in here must be secure (i.e. use @login_required decorators)
"""
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from django_common.auth_backends import User

from api.views import failure_response, success_response
from authentication.forms import UserDetailsForm


@login_required
@staff_member_required
def get_all_users(request):
    if request.is_ajax:
        users = User.objects.filter(is_superuser=False)
        if users:
            for user in users:
                user.password = None
        data = serializers.serialize("json", users)
        return HttpResponse(data, content_type='application/json')


@login_required
@staff_member_required
def get_user_details(request):
    if request.is_ajax:
        user = get_object_or_404(User, id=request.GET['id'], is_superuser=False)
        response = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "mobile_number": user.profile.mobile_number,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
        }
        return JsonResponse(response)


@login_required
@staff_member_required
def create_new_user(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.profile.mobile_number = request.POST['mobile_number']
            new_user.is_active = True
            new_user.save()

            # Send the user's welcome pack email
            new_user.profile.send_welcome_email(get_current_site(request).name)
            return JsonResponse({'user': new_user.pk})
        return JsonResponse(failure_response)


@login_required
@staff_member_required
def update_user(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.POST['id'], is_superuser=False)
        form = UserDetailsForm(request.POST or None, instance=user)

        if form.is_valid():
            user.profile.mobile_number = request.POST['mobile_number']
            if user.id == request.user.id:
                user.is_staff = True
            form.save()
            return JsonResponse(success_response)
        return JsonResponse(failure_response)


@login_required
@staff_member_required
def activate_user(request):
    if request.method == 'POST':
        if request.POST['is_active']:
            user = get_object_or_404(User, id=request.POST['id'], is_superuser=False)
            if user.id is not request.user.id:
                user.is_active = request.POST['is_active']
                user.save()
                return JsonResponse(success_response)
        return JsonResponse(failure_response)


@login_required
@staff_member_required
def resend_welcome_email(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.POST['id'], is_superuser=False)
        user.profile.send_welcome_email(get_current_site(request).name)
        return JsonResponse(success_response)


@login_required
@staff_member_required
def delete_user(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.POST['id'], is_superuser=False)
        if user.id is not request.user.id:
            user.delete()
            return JsonResponse(success_response)
        return JsonResponse(failure_response)
