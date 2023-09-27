from django.shortcuts import render
from .models import Music
from rest_framework.response import Response
from rest_framework import status
from .serializers import MusicSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from utils import get_token
User = get_user_model()



# Create your views here.

@api_view(['GET', 'POST'])
def music_list(request):
    if request.method == 'GET':
        music = Music.objects.all()
        serializer = MusicSerializer(music, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
@api_view(['PUT', 'DELETE'])
def music_detail(request, pk):
    try:
        music = Music.objects.get(pk=pk)
    except Music.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(music,  serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    if request.method == 'DELETE':
        music.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        # print(request.POST)
        fname =  request.data['first_name']
        lname = request.data['last_name']
        # username = request.data['username']
        email = request.data['email']
        pass1 = request.data['password']
        pass2 = request.data['confirm_password']

    if User.objects.filter(email=email):
        return Response('email is already used', status=status.HTTP_400_BAD_REQUEST)
    
    if pass1 != pass2:
        return Response('Inout a uniform password', status=status.HTTP_400_BAD_REQUEST)
    
    # if len(username) > 8:
    #     return Response('the username is too long', status=status.HTTP_400_BAD_REQUEST)
    
    # if not username.isalnum():
    #    return Response('the username is too long', status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(first_name=fname, last_name=lname,email=email, password=pass1)
    if user:
        token = get_token(user)
        response_data = {
            "user":{
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email": user.email
            },
            "token":token.key
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED )
    # myuser = User.objects.create()
    # if myuser.is_valid():
    #     myuser.save()
    return Response('You have successfully registered')
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
    user = authenticate(email = email, password = password)
    if user:
        response_data = {
            "user":{
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email": user.email
            },
            "token":get_token(user).key

        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED )
    return Response('not logged in', status=status.HTTP_401_UNAUTHORIZED)
    
    

def logout(request):
    if request.method == 'POST':
        user = User.objects.get()
        user.delete()
        logout(user)


        



