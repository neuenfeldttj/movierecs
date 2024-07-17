from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, User, UserMovieRating
from .serializers import MovieSerializer, UserMovieRatingSerializer
# Create your views here.

class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all().order_by("title")
    serializer_class = MovieSerializer

class RatedMovieView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserMovieRatingSerializer(data=request.data, many=True)

        if serializer.is_valid():
            data = self.update_recommender()

            return Response({'status': 'success', 
                             'message': 'Movies received',
                             'data': data
                             }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_recommender(self):
        def _sim(a_ratings, b_ratings):
            a_avg, b_avg = 0,0
            for a in a_ratings:
                a_avg += a.rating
            a_avg /= len(a_ratings)
            for b in b_ratings:
                b_avg += b.rating
            b_avg /= len(b_ratings)

        # Go through all the movies I haven't seen
        user_a = User.objects.get(user_id=-1)
        seen_movies_ids = user_a.watchlist.values_list('movie_id', flat=True)
        unseen_movies = Movie.objects.exclude(movie_id__in=seen_movies_ids)

        movie_ratings = []
        for movie in unseen_movies:
            # Go through all users who have rated that movie and compute similarity
            users = User.objects.filter(watchlist=movie)
            scores = []
            for user_b in users:
                movies_in_common = user_a.watchlist.all().intersection(user_b.watchlist.all())
                movies_in_common_ids = movies_in_common.values_list('movie_id', flat=True)
                user_a_ratings = UserMovieRating.objects.filter(user=user_a, movie=movies_in_common_ids)
                user_b_ratings = UserMovieRating.objects.filter(user=user_b, movie=movies_in_common_ids)
                score = _sim(user_a_ratings, user_b_ratings)
                
            movie_ratings.append((movie.movie_id, score))

            # Find the closest users (20-50 users) and then predict a score

        # Sort the movies by score and return top 10