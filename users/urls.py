from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/create/', views.create_profile, name='create_profile'),
    path('profiles/<int:profile_id>/watchlist/', views.watchlist_view, name='watchlist'),
    path('watchlist/add/<int:movie_id>/<int:profile_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:movie_id>/<int:profile_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('settings/', views.account_settings, name='account_settings'),
]
