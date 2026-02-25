from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('series', 'TV Series'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='movies')
    release_year = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True, help_text='YouTube embed URL')
    duration = models.CharField(max_length=20, null=True, blank=True)
    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='movie')
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def avg_rating(self):
        ratings = self.user_ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return self.rating

    def likes_count(self):
        return self.likes.filter(is_like=True).count()

    def dislikes_count(self):
        return self.likes.filter(is_like=False).count()


class Season(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seasons')
    season_number = models.IntegerField()
    title = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.movie.title} - Season {self.season_number}"


class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    episode_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=20, null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='episode_thumbnails/', null=True, blank=True)

    def __str__(self):
        return f"{self.season} - Episode {self.episode_number}: {self.title}"


class UserRating(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_ratings')
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.email} rated {self.movie.title}: {self.score}/5"


class WatchHistory(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='watch_history')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watched_by')
    watched_at = models.DateTimeField(auto_now=True)
    progress = models.IntegerField(default=0, help_text='Progress in seconds')

    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-watched_at']

    def __str__(self):
        return f"{self.user.email} watched {self.movie.title}"


class Comment(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='comments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.movie.title}"


class MovieLike(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='movie_likes')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        action = 'liked' if self.is_like else 'disliked'
        return f"{self.user.username} {action} {self.movie.title}"
