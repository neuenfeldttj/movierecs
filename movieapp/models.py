from django.db import models

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Movie(models.Model):
    movie_id = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=50)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class User(models.Model):
    user_id = models.IntegerField(unique=True)
    watchlist = models.ManyToManyField(Movie, through='UserMovieRating', related_name='watched_by')

    def add_movie_rating(self, movie, rating):
        UserMovieRating.objects.update_or_create(user=self, movie=movie, defaults={'rating': rating})

    def get_movie_ratings(self):
        return self.usermovierating_set.all()

    def __str__(self):
        return str(self.id)

class UserMovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.DecimalField(decimal_places=1, max_digits=2)

    class Meta:
        unique_together = ('user', 'movie') # no duplicates

    def __str__(self):
        return f"{self.user.id} rated {self.movie.title} with {self.rating}"
    

