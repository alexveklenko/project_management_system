from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

from projects.views import Project
from tasks.views import Task
from time_entries.views import TimeEntry
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def index(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'users/index.html', context)


def user_view(request, id):
    user = get_object_or_404(User, id=id)
    projects = Project.objects.filter(
        members=user).order_by('-added')[:10]
    tasks = Task.objects.filter(
        assigned_to=user).order_by('-added')[:10]
    time_entries = TimeEntry.objects.filter(
        author=user).order_by('-added')[:10]
    context = {
        'user': user,
        'projects': projects,
        'tasks': tasks,
        'time_entries': time_entries,
    }
    return render(request, 'users/single_user.html', context)


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


def profile(request):
    return render(request, 'users/profile.html', {})


def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/edit_profile.html', context)
