from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Profile, Watchlist
from movies.models import Movie


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/register.html')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'users/register.html')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'users/register.html')
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, f'Welcome to Cartmation, {username}!')
        return redirect('home')
    return render(request, 'users/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                if user.is_active:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid credentials.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_list(request):
    profiles = Profile.objects.filter(user=request.user)
    return render(request, 'users/profiles.html', {'profiles': profiles})


@login_required
def create_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        is_kids = request.POST.get('is_kids') == 'on'
        Profile.objects.create(user=request.user, name=name, is_kids=is_kids)
        return redirect('profile_list')
    return render(request, 'users/create_profile.html')


@login_required
def watchlist_view(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    watchlist = Watchlist.objects.filter(profile=profile).select_related('movie')
    return render(request, 'users/watchlist.html', {'profile': profile, 'watchlist': watchlist})


@login_required
def add_to_watchlist(request, movie_id, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    movie = get_object_or_404(Movie, id=movie_id)
    Watchlist.objects.get_or_create(profile=profile, movie=movie)
    messages.success(request, f'"{movie.title}" added to your watchlist.')
    return redirect('movie_detail', pk=movie_id)


@login_required
def remove_from_watchlist(request, movie_id, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)
    Watchlist.objects.filter(profile=profile, movie_id=movie_id).delete()
    messages.success(request, 'Removed from watchlist.')
    return redirect('watchlist', profile_id=profile_id)


@login_required
def account_settings(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            username = request.POST.get('username')
            if username:
                request.user.username = username
            if request.FILES.get('avatar'):
                request.user.avatar = request.FILES['avatar']
            request.user.save()
            messages.success(request, 'Profile updated successfully!')
        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if not request.user.check_password(old_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password1 != new_password2:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password1) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
            else:
                request.user.set_password(new_password1)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully!')
        return redirect('account_settings')
    return render(request, 'users/account_settings.html')
