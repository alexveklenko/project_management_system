from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User


from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}. You can login now')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            messages.warning(request, 'You already logged in')
            return redirect('/')
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})
