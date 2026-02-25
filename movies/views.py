from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Movie, Genre, UserRating, WatchHistory, Comment, MovieLike


def home(request):
    # Featured list for slideshow
    featured_list = list(Movie.objects.filter(is_featured=True)[:5])
    if len(featured_list) < 5:
        trending_extra = Movie.objects.filter(is_trending=True).exclude(
            id__in=[m.id for m in featured_list])[:5 - len(featured_list)]
        featured_list += list(trending_extra)

    trending = Movie.objects.filter(is_trending=True)[:12]
    movies = Movie.objects.filter(content_type='movie')[:12]
    series = Movie.objects.filter(content_type='series')[:12]
    genres = Genre.objects.all()
    top10 = Movie.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-rating')[:10]
    # Dhanush collection
    dhanush_titles = ['Raayan','Vaathi','Thiruchitrambalam','Karnan','Jagame Thandhiram','Asuran','3','Vada Chennai','Maari','Pattas']
    dhanush_movies = Movie.objects.filter(title__in=dhanush_titles)
    continue_watching = []
    if request.user.is_authenticated:
        continue_watching = WatchHistory.objects.filter(user=request.user).select_related('movie')[:6]
    return render(request, 'movies/home.html', {
        'featured_list': featured_list,
        'trending': trending,
        'movies': movies,
        'series': series,
        'genres': genres,
        'top10': top10,
        'continue_watching': continue_watching,
        'dhanush_movies': dhanush_movies,
    })


@login_required
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    related = Movie.objects.filter(genre__in=movie.genre.all()).exclude(pk=pk).distinct()[:8]
    comments = movie.comments.select_related('user')[:20]
    user_rating = None
    user_like = None
    if request.user.is_authenticated:
        try:
            user_rating = UserRating.objects.get(user=request.user, movie=movie)
        except UserRating.DoesNotExist:
            pass
        try:
            user_like = MovieLike.objects.get(user=request.user, movie=movie)
        except MovieLike.DoesNotExist:
            pass
        WatchHistory.objects.get_or_create(user=request.user, movie=movie)
    if request.method == 'POST':
        text = request.POST.get('comment', '').strip()
        if text:
            Comment.objects.create(user=request.user, movie=movie, text=text)
            return redirect('movie_detail', pk=pk)
    return render(request, 'movies/detail.html', {
        'movie': movie,
        'related': related,
        'comments': comments,
        'user_rating': user_rating,
        'user_like': user_like,
    })


def browse(request):
    genre_id = request.GET.get('genre')
    content_type = request.GET.get('type')
    query = request.GET.get('q')
    movies = Movie.objects.all()
    if genre_id:
        movies = movies.filter(genre__id=genre_id)
    if content_type:
        movies = movies.filter(content_type=content_type)
    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(description__icontains=query))
    genres = Genre.objects.all()
    return render(request, 'movies/browse.html', {
        'movies': movies,
        'genres': genres,
        'selected_genre': genre_id,
        'selected_type': content_type,
        'query': query,
    })


def genre_view(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    movies = Movie.objects.filter(genre=genre)
    return render(request, 'movies/genre.html', {'genre': genre, 'movies': movies})


def search_suggestions(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        movies = Movie.objects.filter(title__icontains=query)[:6]
        results = [{'id': m.pk, 'title': m.title, 'year': m.release_year, 'type': m.content_type} for m in movies]
    return JsonResponse({'results': results})


@login_required
def rate_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        if 1 <= score <= 5:
            UserRating.objects.update_or_create(
                user=request.user, movie=movie,
                defaults={'score': score}
            )
            return JsonResponse({'success': True, 'score': score, 'avg': float(movie.avg_rating())})
    return JsonResponse({'success': False})


@login_required
def like_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        is_like = request.POST.get('action') == 'like'
        like_obj, created = MovieLike.objects.get_or_create(
            user=request.user, movie=movie, defaults={'is_like': is_like})
        if not created:
            if like_obj.is_like == is_like:
                like_obj.delete()
                action = 'removed'
            else:
                like_obj.is_like = is_like
                like_obj.save()
                action = 'like' if is_like else 'dislike'
        else:
            action = 'like' if is_like else 'dislike'
        return JsonResponse({
            'success': True, 'action': action,
            'likes': movie.likes_count(),
            'dislikes': movie.dislikes_count(),
        })
    return JsonResponse({'success': False})


@login_required
def watch_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    WatchHistory.objects.get_or_create(user=request.user, movie=movie)
    return render(request, 'movies/watch.html', {'movie': movie})

