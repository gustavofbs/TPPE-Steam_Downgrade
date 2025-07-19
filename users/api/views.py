from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
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
    
    @action(detail=True, methods=['put'])
    def update_profile(self, request, pk=None):
        """
        Atualiza o perfil e dados básicos de um usuário específico.
        """
        user = self.get_object()
        profile = get_object_or_404(Profile, user=user)
        
        # Atualizar dados básicos do usuário
        user_data = {}
        if 'first_name' in request.data:
            user_data['first_name'] = request.data['first_name']
        if 'last_name' in request.data:
            user_data['last_name'] = request.data['last_name']
        if 'email' in request.data:
            user_data['email'] = request.data['email']
        
        if user_data:
            user_serializer = UserUpdateSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Atualizar dados do perfil
        profile_data = {}
        if 'bio' in request.data:
            profile_data['bio'] = request.data['bio']
        if 'birth_date' in request.data:
            profile_data['birth_date'] = request.data['birth_date']
        if 'avatar' in request.data:
            profile_data['avatar'] = request.data['avatar']
        
        if profile_data:
            profile_serializer = ProfileSerializer(profile, data=profile_data, partial=True, context={'request': request})
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Retornar dados completos do usuário atualizado
        user_serializer = UserSerializer(user, context={'request': request})
        return Response(user_serializer.data)
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_avatar(self, request, pk=None):
        """
        Endpoint específico para upload de avatar como arquivo.
        """
        user = self.get_object()
        profile = get_object_or_404(Profile, user=user)
        
        if 'avatar' not in request.FILES:
            return Response({'error': 'Nenhum arquivo de avatar fornecido'}, status=status.HTTP_400_BAD_REQUEST)
        
        avatar_file = request.FILES['avatar']
        
        # Validar tipo de arquivo
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if avatar_file.content_type not in allowed_types:
            return Response({'error': 'Tipo de arquivo não permitido. Use JPEG, PNG, GIF ou WebP.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar tamanho do arquivo (máximo 5MB)
        if avatar_file.size > 5 * 1024 * 1024:
            return Response({'error': 'Arquivo muito grande. Máximo 5MB.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Atualizar o avatar
        profile.avatar = avatar_file
        profile.save()
        
        # Retornar dados atualizados do usuário
        user_serializer = UserSerializer(user, context={'request': request})
        return Response(user_serializer.data)
    
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
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Busca usuários por nome de usuário.
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({'results': []})
        
        # Buscar usuários que contenham a query no username
        users = User.objects.select_related('profile').filter(
            username__icontains=query
        ).exclude(
            id=request.user.id  # Excluir o usuário atual
        )[:10]  # Limitar a 10 resultados
        
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response({'results': serializer.data})
