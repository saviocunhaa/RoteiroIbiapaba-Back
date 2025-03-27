from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para visualização e atualização de dados do usuário.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'nome', 'foto', 'data_criacao')
        read_only_fields = ('id', 'data_criacao')
        extra_kwargs = {
            'email': {'help_text': 'Endereço de email do usuário'},
            'nome': {'help_text': 'Nome completo do usuário'},
            'foto': {'help_text': 'Foto de perfil do usuário'},
        }

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de novos usuários.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text='Endereço de email único do usuário'
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        help_text='Senha do usuário (deve atender aos requisitos de segurança)'
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        help_text='Confirmação da senha (deve ser igual ao campo password)'
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'nome', 'foto')
        extra_kwargs = {
            'nome': {'help_text': 'Nome completo do usuário'},
            'foto': {'help_text': 'Foto de perfil do usuário (opcional)'},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não conferem"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer para solicitação de redefinição de senha.
    """
    email = serializers.EmailField(
        required=True,
        help_text='Endereço de email do usuário para envio do link de redefinição'
    )