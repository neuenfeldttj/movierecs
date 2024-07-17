from rest_framework import serializers
from .models import User, Movie, Genre, UserMovieRating

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['movie_id', 'title', 'genres']

class UserMovieRatingSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)

    def create(self, validated_data):
        # Get the Movie object based on the title
        movie, created = Movie.objects.get_or_create(title=validated_data['title'])
        
        user, _ = User.objects.get_or_create(user_id=-1)
        
        # Create a new UserMovieRating instance
        user_movie_rating = UserMovieRating.objects.create(
            user=user,
            movie=movie,
            rating=validated_data['rating']
        )
        
        return user_movie_rating