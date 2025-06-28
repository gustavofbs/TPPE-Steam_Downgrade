from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from users.models import Profile
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ProfileSerializer,
    PasswordChangeSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint para usuários.
    
    list:
    Retorna uma lista de todos os usuários.
    
    retrieve:
    Retorna os detalhes de um usuário específico.
    
    create:
    Cria um novo usuário.
    
    update:
    Atualiza um usuário existente.
    
    destroy:
    Remove um usuário existente.
    """
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado com base na ação"""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        """
        Permissões personalizadas:
        - Qualquer um pode criar um usuário (registro)
        - Apenas usuários autenticados podem ver a lista de usuários
        - Apenas o próprio usuário ou um administrador pode ver, atualizar ou excluir um usuário específico
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Criar um novo usuário"""
        serializer.save()
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """
        Retorna o perfil de um usuário específico.
        """
        user = self.get_object()
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], serializer_class=ProfileSerializer)
    def update_profile(self, request, pk=None):
        """
        Atualiza o perfil de um usuário específico.
        """
        user = self.get_object()
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], serializer_class=PasswordChangeSerializer)
    def change_password(self, request, pk=None):
        """
        Altera a senha de um usuário específico.
        """
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            # Verificar se a senha antiga está correta
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Senha incorreta.']}, status=status.HTTP_400_BAD_REQUEST)
            
            # Definir a nova senha
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'Senha alterada com sucesso.'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Retorna os detalhes do usuário autenticado.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
