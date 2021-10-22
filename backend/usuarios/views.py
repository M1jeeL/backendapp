from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from .serializers import (
    TeacherRegistrationSerializer, ClientRegistrationSerializer,
    LoginSerializer, ProfileSerializer)
from django.contrib.auth import authenticate, login, logout
from django.db.models import query
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from rest_framework.decorators import api_view
from rest_framework import generics, serializers
from rest_framework import status
from rest_framework.response import Response

from .models import Client, User

####        CLIENTE        ####

###     VIEW REGISTRO TEACHER     ###
class TeacherRegistrationView(RegisterView):
    serializer_class = TeacherRegistrationSerializer

###     VIEW REGISTRO CLIENT     ###
class ClientRegistrationView(RegisterView):
    serializer_class = ClientRegistrationSerializer


###     VIEW PERFIL CLIENT     ###
class ProfilesViewClient(generics.ListAPIView):
    queryset = User.objects.filter(is_client=True)
    serializer_class = ProfileSerializer

###     VIEW PERFIL TEACHER     ###
class ProfilesViewTeacher(generics.ListAPIView):
    queryset = User.objects.filter(is_teacher=True)
    serializer_class = ProfileSerializer

###     VIEW USUARIOS     ###
class ProfilesViewUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer


###     PROFILE CLIENT BY ID     ###
@api_view(['GET'])
def profile_client(request, id):
    client = User.objects.get(id=id, is_client=True)
    serializer = ProfileSerializer(client, many=False)
    return Response(serializer.data)

###     PROFILE TEACHER BY ID     ###
@api_view(['GET'])
def profile_teacher(request, id):
    client = User.objects.get(id=id, is_teacher=True)
    serializer = ProfileSerializer(client, many=False)
    return Response(serializer.data)


###     LOGIN USER     ###
@api_view(['POST'])
def login_user(request):
    #Capturar email y password
    email = request.data.get('email', None)
    password = request.data.get('password', None)
    client = authenticate(email=email, password=password)

    if client:
        login(request, client)
        return Response(LoginSerializer(client).data, status=status.HTTP_200_OK)
    return Response({'Failed': "[!]ERROR: email or password incorrect!"}, 
                    status=status.HTTP_404_NOT_FOUND)

###     LOGOUT USER     ###
@api_view(['POST'])
def logout_client(request):
    logout(request)
    return Response({'Logout': "[-] Logout successfuly!"}, status=status.HTTP_200_OK)


###     CAMBIAR CONTRASEÑA     ###
@receiver(reset_password_token_created)
def reset_password(sender, instance, reset_password_token, *args, **kwargs):
    print(
        f"\n[+]Recupera la contraseña del correo '{reset_password_token.user.email}' \n[-]Usando el token '{reset_password_token.key}' desde la API http://localhost:8000/user/reset_password/confirm/.")
































































###     LISTA CASOS     ###
@api_view(['GET'])
def case_get_all(request):
    cases = Case.objects.get()
    serializer = CaseSerializer(cases, many=True)
    return Response(serializer.data, stauts=status.HTTP_200_OK)
