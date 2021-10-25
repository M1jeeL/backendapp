from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_framework.fields import empty
from .serializers import (
    TeacherRegistrationSerializer, ClientRegistrationSerializer,
    LoginSerializer, ProfileSerializer, CreateCaseSerializer, CaseSerializer, PutcasebyIdSerializer)
from django.contrib.auth import SESSION_KEY, authenticate, login, logout
from django.db.models import query
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from rest_framework.decorators import api_view
from rest_framework import generics, serializers
from rest_framework import status
from rest_framework.response import Response

from .models import Client, User, Case

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

### CREAR CASO ###
class CreateCaseView(RegisterView):
    serializer_class = CreateCaseSerializer

###     LISTA CASOS     ###
class CasesViews(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

@api_view(['GET'])
def list_cases(request):
    stat = request.query_params.get('status')
    type = request.query_params.get('type')
    querySet = query_all_avaible()

    if (stat  and type ):
        querySet = query_by_type_status(type,stat)
    elif (type and (stat is None or stat is "")):
        querySet = query_by_type(type)
    elif ((type is None or type is "")  and stat ):
        querySet = query_by_status(stat)
    serializer = CaseSerializer(querySet,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

    
def query_all_avaible():
    querySet = Case.objects.filter(status= 'D')
    return querySet

def query_by_status(status):
    querySet = Case.objects.filter(status=status)
    return querySet

def query_by_type(type):
    querySet = Case.objects.filter(type_status=type).filter(status='D')
    return querySet

def query_by_type_status(type,status):
    querySet = Case.objects.filter(type_status=type).filter(status=status)
    return querySet

# ###     FILTRADO POR ESTADO    ###
# @api_view(['GET'])
# def list_case_status(request, id):
#     case = Case.objects.get(id=id)
#     serializer = CaseSerializer(case, many=False)
#     return Response(serializer.data, status=status.HTTP_200_OK)

### ACTUALIZAR ESTADO CASO####

@api_view(['PUT'])
def edit_case(request, id):
    case = Case.objects.get(id=id)
    serializer = PutcasebyIdSerializer(case, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)