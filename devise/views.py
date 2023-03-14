from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)
from allauth.account.views import ConfirmEmailView
from django.contrib.auth.models import User
from django.urls import reverse
# from django.contrib.auth import get_user_model


@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to the Devise DRF API"
    })


# dj-rest-auth logout view fix from CI
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


# https://stackoverflow.com/questions/29725369/improperlyconfigured-at-rest-auth-registration-account-confirm-email
class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            self.object = None
        user = User.objects.get(email=self.object.email_address.email)
        # redirect_url = reverse('account_login', args=(user.id,))
        redirect_url = reverse('account_login')
        return redirect(redirect_url)
