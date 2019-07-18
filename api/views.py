from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    # Custom API call method for user to create/update ratings
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            # user = User.objects.get(id=1) <--Hardcoded user..
            # print('user:', user)

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(
                    user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created',
                            'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            response = {'message': 'is working'}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    # Restrict user to use default ModelViewSet api call method (eg. create/update..)
    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
