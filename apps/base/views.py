from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'apps/base/index.html')


@login_required
def logout_after_change_password(request: HttpRequest):
    logout(request)
    messages.success(request, _('password has been changed successfully'))
    return redirect(reverse('login'))