import pandas as pd
from django.core.management.base import BaseCommand
from movieapp.models import User, Movie, Genre

class Command(BaseCommand):
    def handle(self, *args, **options):
        movies_df = pd.read_csv("./movies.csv")
        print("Adding movies to database")
        for i, row in movies_df.iterrows():
            movie, _ = Movie.objects.get_or_create(movie_id=row["movieId"], title=row["title"])
            print(movie)
            genres = row["genres"].split("|")
            for genre in genres:
                g, created = Genre.objects.get_or_create(name=genre)
                print(g)
                movie.genres.add(g)
            movie.save()

        print("Movies added!")

        ratings_df = pd.read_csv("./ratings.csv")
        print("Adding users to database")
        for i, row in ratings_df.iterrows():
            user, _ = User.objects.get_or_create(user_id=row["userId"])
            print(user)
            movie = Movie.objects.get(movie_id=row["movieId"])
            user.add_movie_rating(movie=movie, rating=row["rating"])

        print("Users added!")