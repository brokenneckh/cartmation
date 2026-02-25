from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('browse/', views.browse, name='browse'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:pk>/watch/', views.watch_movie, name='watch_movie'),
    path('movie/<int:pk>/rate/', views.rate_movie, name='rate_movie'),
    path('movie/<int:pk>/like/', views.like_movie, name='like_movie'),
    path('genre/<int:pk>/', views.genre_view, name='genre'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
]
