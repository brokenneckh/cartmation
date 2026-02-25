from django.contrib import admin
from .models import CustomUser, Profile, Watchlist

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'subscription', 'is_staff']
    search_fields = ['email', 'username']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_kids']

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['profile', 'movie', 'added_at']
