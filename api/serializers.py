from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Movie, Rating
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
        #fields = ('__all__')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'no_of_ratings', 'avg_rating')
        # fields = ('__all__', 'no_of_ratings', 'avg_rating') <-----will not work like this!!


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        #fields = ('id','stars','user','movie')
        fields = ('__all__')
