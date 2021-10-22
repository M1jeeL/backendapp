from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
#from django.contrib.auth.hashers import make_password
from .models import Case, Client, Teacher, User

###     VARIABLES GLOBALES     ###
expertise_status = [
    ('L', 'Legal'),
    ('F', 'Financiera')
]

careers_status = [
    ('abogado', 'Derecho'),
    ('ingeniero economico', 'Ingeniero en economia'),
    ('Ingeniero industrial', 'Ingeniero industrial'),
    ('Ingeniero informatico', 'Ingeniero en informatica'),
]

##########      SERIALIZADORES     ########## 

###     REGISTRAR TEACHER     ###
class TeacherRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    rut = serializers.CharField(required = True)
    teacher = serializers.PrimaryKeyRelatedField(read_only=True,)
    phone = serializers.CharField(required=True)
    high_school = serializers.CharField(required=True)
    expertise = serializers.ChoiceField(required=True,choices=expertise_status)
    careers = serializers.ChoiceField(required=True,choices=careers_status)
    docfile = serializers.FileField(required=False)
    img = serializers.ImageField(required=False)
    
    def get_cleaned_data(self):
            data = super(TeacherRegistrationSerializer, self).get_cleaned_data()
            extra_data = {
                'first_name' : self.validated_data.get('first_name', ''),
                'last_name' : self.validated_data.get('last_name', ''),
                'rut' : self.validated_data.get('rut', ''),
                'phone' : self.validated_data.get('phone', ''),
                'high_school': self.validated_data.get('high_school', ''),
                'docfile' : self.validated_data.get('docfile', ''),
                'img' : self.validated_data.get('img', ''),
                'expertise' : self.validated_data.get('expertise', ''),
                'career' : self.validated_data.get('careers', ''),
            }
            data.update(extra_data)
            return data

    def save(self, request):
        user = super(TeacherRegistrationSerializer, self).save(request)
        user.is_teacher = True
        user.save()
        teacher = Teacher(
            teacher=user,
            phone = self.validated_data.get('phone', ''),
            expertise = self.validated_data.get('expertise', ''),
            high_school= self.validated_data.get('high_school', ''),
            docfile = self.validated_data.get('docfile', ''),
            rut = self.validated_data.get('rut', ''),
            img = self.validated_data.get('img', ''),
            careers = self.validated_data.get('careers', ''),
            )
        teacher.save()
        return user

###     REGISTRAR CLIENT     ###
class ClientRegistrationSerializer(RegisterSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True,)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    rut = serializers.CharField(required = True)
    phone = serializers.CharField(required=True)
    
    def get_cleaned_data(self):
            data = super(ClientRegistrationSerializer, self).get_cleaned_data()
            extra_data = {
                'phone' : self.validated_data.get('phone', ''),
                'first_name' : self.validated_data.get('first_name', ''),
                'last_name' : self.validated_data.get('last_name', ''),
                'rut' : self.validated_data.get('rut', ''),
            }
            data.update(extra_data)
            return data

    def save(self, request):
        user = super(ClientRegistrationSerializer, self).save(request)
        user.is_client = True
        user.save()
        client = Client(
            client=user,
            phone=self.cleaned_data.get('phone'),
            rut = self.validated_data.get('rut', ''),
            )
        client.save()
        return user


###     INICIO DE SESION     ###
class LoginSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )

###     PERFIL DEL USUARIO     ###
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email'
        )



###     OBTENER UPDATE POR ID   ###

class PutcasebyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = (
            'name',
            'type_status'
        )