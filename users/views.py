from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer, UserCreateSerializer, PasswordResetSerializer

User = get_user_model()

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Registra um novo usuário no sistema",
        request_body=UserCreateSerializer,
        responses={
            201: openapi.Response(
                description="Usuário criado com sucesso",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Token de atualização JWT'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Token de acesso JWT'),
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='Dados do usuário')
                    }
                )
            ),
            400: "Dados inválidos"
        }
    )
    def post(self, request):
        """
        Cria um novo usuário no sistema.
        
        Retorna tokens JWT de acesso e atualização junto com os dados do usuário.
        """
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    @swagger_auto_schema(
        operation_description="Encerra a sessão do usuário invalidando o token de atualização",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Token de atualização JWT')
            }
        ),
        responses={
            205: "Logout realizado com sucesso",
            400: "Token inválido"
        }
    )
    def post(self, request):
        """
        Encerra a sessão do usuário.
        
        Adiciona o token de atualização à lista negra, invalidando-o.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Envia um email com link para redefinição de senha",
        request_body=PasswordResetSerializer,
        responses={
            200: "Email de redefinição de senha enviado",
            400: "Email inválido"
        }
    )
    def post(self, request):
        """
        Envia um email com link para redefinição de senha.
        
        Gera um token único e envia um link para o email do usuário.
        """
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"
                
                send_mail(
                    'Redefinição de senha - Roteiro Ibiapaba',
                    f'Clique no link para redefinir sua senha: {reset_link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response({'detail': 'Email de redefinição de senha enviado.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # Não informamos ao usuário que o email não existe por segurança
                return Response({'detail': 'Email de redefinição de senha enviado.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    @swagger_auto_schema(
        operation_description="Retorna os dados do perfil do usuário autenticado",
        responses={
            200: UserSerializer
        }
    )
    def get(self, request):
        """
        Retorna os dados do perfil do usuário autenticado.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Atualiza os dados do perfil do usuário autenticado",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Dados inválidos"
        }
    )
    def put(self, request):
        """
        Atualiza os dados do perfil do usuário autenticado.
        
        Permite atualizar nome, email e foto.
        """
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
