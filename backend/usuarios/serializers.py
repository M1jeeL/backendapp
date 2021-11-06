from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
#from django.contrib.auth.hashers import make_password
from .models import Client, Teacher, User, Case

###     VARIABLES GLOBALES     ###
expertise_status = [
    ('L', 'Legal'),
    ('F', 'Financiera')
]

type_status = [
    ('L', 'Legal'),
    ('F', 'Financiera'),
    ('A', 'Ambos')
]

careers_status = [
    ('abogado', 'Derecho'),
    ('ingeniero economico', 'Ingeniero en economia'),
    ('Ingeniero industrial', 'Ingeniero industrial'),
    ('Ingeniero informatico', 'Ingeniero en informatica')
]

status = [
    ('D', 'Disponible'),
    ('A', 'Asignado'),
    ('S', 'Solicitud Cierre'),
    ('C', 'Cerrado')
]

chat_preference = [
    ('0', 'ChatApp'),
    ('1', 'Llamada'),
    ('2', 'Ambas')
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


###     CREATE CASE             ####

class CreateCaseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    files = serializers.FileField(required=False)
    type_status = serializers.ChoiceField(required=True,choices=type_status)
    status = serializers.ChoiceField(required=True,choices=status)
    chat_preference = serializers.ChoiceField(required=True,choices=chat_preference)
    class Meta:
        model = Case
        fields = (
            'name',
            'description',
            'files',
            'type_status',
            'status',
            'chat_preference'
        )
    def get_cleaned_data(self):
            data = super(CreateCaseSerializer, self).get_cleaned_data()
            extra_data = {
                'name' : self.validated_data.get('name', ''),
                'description' : self.validated_data.get('description', ''),
                'files' : self.validated_data.get('files', ''),
                'type_status': self.validated_data.get('type_status', ''),
                'status' : self.validated_data.get('status', ''),
                'chat_preference' : self.validated_data.get('chat_preference', ''),
                
            }
            data.update(extra_data)
            return data

    def save(self, request):
        
        
        
        case = Case(
            
            name = self.validated_data.get('name', ''),
                description = self.validated_data.get('description', ''),
                files = self.validated_data.get('files', ''),
                type_status = self.validated_data.get('type_status', ''),
                status = self.validated_data.get('status', ''),
                chat_preference = self.validated_data.get('chat_preference', ''),
            )
        case.save()
        return case    

###     PERFIL DE CASOS     ###
class CaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Case
        fields = (
            'id',
            'name',
            'description',
            'type_status',
            'status',
            'chat_preference',
            'case_teacher',
            'case_client'
        )