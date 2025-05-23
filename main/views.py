from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required(redirect_field_name='login')
def main(request):
    return redirect('view_dash')


def logout_view(request):
    logout(request)
    return redirect('main')
