import decimal
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, User, UserMovieRating
from .serializers import MovieSerializer, UserMovieRatingSerializer, PredictMovieSerializer
import numpy as np

# Create your views here.

class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all().order_by("title")
    serializer_class = MovieSerializer

class RatedMovieView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserMovieRatingSerializer(data=request.data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 
                             'message': 'Movies received',
                             }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PredictMovieView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PredictMovieSerializer(data=request.data)
        if serializer.is_valid():
            rating = self.update_recommender(serializer.validated_data.get("title"))

            return Response({'status': 'success', 
                             'message': 'Movie received',
                             'predicted_rating': rating,
                             }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_recommender(self, new_movie):
        def _sim(a_ratings, b_ratings): #Sample Pearson's correlation coefficient
            a_ratings = [x.rating for x in a_ratings]
            a_avg = np.mean(a_ratings)
            b_ratings = [x.rating for x in b_ratings]
            b_avg = np.mean(b_ratings)
            numerator, a_sum2, b_sum2 = 0,0,0
            for i in range(len(a_ratings)):
                numerator += (a_ratings[i]-a_avg)*(b_ratings[i]-b_avg)
                a_sum2 += (a_ratings[i]-a_avg)**2
                b_sum2 += (b_ratings[i]-b_avg)**2
            if a_sum2 == 0 or b_sum2 == 0:
                return 0
            return decimal.Decimal(numerator / np.sqrt(a_sum2*b_sum2))

        # Go through all the movies I haven't seen
        user_a, _ = User.objects.get_or_create(user_id=-1)
        # seen_movies_ids = user_a.watchlist.values_list('movie_id', flat=True)
        # unseen_movies = Movie.objects.exclude(movie_id__in=seen_movies_ids)
        movie = Movie.objects.get(title=new_movie)
        
        # Average rating for user_a for all movies
        user_a_ratings_all = UserMovieRating.objects.filter(user=user_a)
        ratings_a = [x.rating for x in user_a_ratings_all]
        a_avg = decimal.Decimal(np.mean(ratings_a))
        print("Starting analysis...")
        # Go through all users who have rated that movie and compute similarity
        users = User.objects.filter(watchlist=movie)
        scores = []
        for user_b in users:
            movies_in_common = user_a.watchlist.all() & user_b.watchlist.all()
            # movies_in_common_ids = movies_in_common.values_list('movie_id', flat=True)
            user_a_ratings = UserMovieRating.objects.filter(user=user_a, movie__in=movies_in_common)
            user_b_ratings = UserMovieRating.objects.filter(user=user_b, movie__in=movies_in_common)
            score = abs(_sim(user_a_ratings, user_b_ratings)) #absolute value so we know exact opposite people's interest
            if score != 0:
                scores.append((score, user_b))
        
        # Find the closest users (20-50 users) and then predict a score
        num_people = 30
        if len(users) < 30:
            num_people = len(users)
        scores = sorted(scores, key=lambda x: float(x[0]), reverse=True)[:num_people]
        users = [x[1] for x in scores] #grabs most similar users

        normalizer_sum = 0
        deviation_sum = 0
        for user_b in users:
            user_b_movies = user_b.watchlist.all()
            movies_in_common = user_a.watchlist.all() & (user_b_movies)
            # movies_in_common_ids = movies_in_common.values_list('movie_id', flat=True)
            user_a_ratings = UserMovieRating.objects.filter(user=user_a, movie__in=movies_in_common)
            user_b_ratings = UserMovieRating.objects.filter(user=user_b, movie__in=movies_in_common)
            sim = _sim(user_a_ratings, user_b_ratings)
            normalizer_sum += abs(sim)
            user_b_ratings_all = UserMovieRating.objects.filter(user=user_b)
            ratings_b = [x.rating for x in user_b_ratings_all]
            b_avg = np.mean(ratings_b)
            b_rating = UserMovieRating.objects.get(user=user_b, movie=movie).rating
            deviation_sum += sim*(b_rating-b_avg)

        if normalizer_sum == 0:
            prediction_a = a_avg
        else :
            prediction_a = a_avg + deviation_sum/normalizer_sum
        
        print("\n\nFinished calculating all movies!\n\n")
        print(prediction_a)
        print(deviation_sum, normalizer_sum)

        # # Sort the movies by score and return top 10
        # top_10_ids = sorted(movie_ratings, key=lambda x: x[1], reverse=True)[:10]
        # top_10_ids = [x[0] for x in top_10_ids]
        # top_10_movies = Movie.objects.filter(movie_id__in=top_10_ids)

        return prediction_a