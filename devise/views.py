from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)
from allauth.account.views import ConfirmEmailView
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect
from . import settings
from allauth.account.adapter import get_adapter


# Code from CI 'Moments' walkthrough project
@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to the Devise DRF API"
    })


# Code from CI 'Moments' walkthrough project
@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response


class CustomConfirmEmailView(ConfirmEmailView):
    """
    Customising the ConfirmEmailView provided with django-allauth
    to verify email on GET and redirect to home instead of allauth templates
    """
    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            if settings.ACCOUNT_CONFIRM_EMAIL_ON_GET:
                return self.post(*args, **kwargs)
        except Http404:
            self.object = None
        return Http404
        # self.object = self.get_object()
        # if settings.ACCOUNT_CONFIRM_EMAIL_ON_GET:
        #     return self.post(*args, **kwargs)

    def get_redirect_url(self):
        return redirect('/')
