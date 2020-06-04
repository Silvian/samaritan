"""Webhook decorators."""
from django.http import HttpResponse

from samaritan import settings


def api_key_required(func):
    def wrapper(request):
        api_key = request.META.get("HTTP_API_KEY")
        if api_key != settings.WEBHOOK_API_KEY:
            return HttpResponse(status=403)
        return func(request)
    return wrapper
