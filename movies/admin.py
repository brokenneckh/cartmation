from django.contrib import admin
from .models import Movie, Genre, Season, Episode, UserRating, WatchHistory, Comment, MovieLike

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'release_year', 'rating', 'is_featured', 'is_trending']
    list_filter = ['content_type', 'is_featured', 'is_trending', 'genre']
    search_fields = ['title']
    filter_horizontal = ['genre']

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['movie', 'season_number', 'title']

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['season', 'episode_number', 'title', 'duration']

@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'score', 'created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'text', 'created_at']
    search_fields = ['user__username', 'movie__title']

@admin.register(MovieLike)
class MovieLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'is_like', 'created_at']

@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'watched_at']
