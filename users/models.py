from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    subscription = models.CharField(max_length=20, choices=[
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ], default='free')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='profile_avatars/', null=True, blank=True)
    is_kids = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.name}"


class Watchlist(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'movie')

    def __str__(self):
        return f"{self.profile.name} - {self.movie.title}"
