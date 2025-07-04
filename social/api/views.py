from rest_framework import viewsets, permissions, filters, mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from social.models import (
    Friendship, GameReview, ReviewComment, ReviewVote,
    UserActivity, GameRecommendation, UserGamePreference
)
from .serializers import (
    FriendshipSerializer, FriendshipCreateSerializer, FriendshipUpdateSerializer,
    GameReviewSerializer, GameReviewCreateUpdateSerializer,
    ReviewCommentSerializer, ReviewCommentCreateSerializer,
    ReviewVoteSerializer, ReviewVoteCreateSerializer,
    UserActivitySerializer, GameRecommendationSerializer,
    GameRecommendationCreateSerializer, UserGamePreferenceSerializer
)
from games.models import Game, Genre


class FriendshipViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        GenericViewSet):
    """
    API endpoint para gerenciar amizades.
    
    list:
    Retorna uma lista de todas as amizades do usuário autenticado.
    
    retrieve:
    Retorna os detalhes de uma amizade específica.
    
    create:
    Cria uma nova solicitação de amizade.
    
    update:
    Atualiza o status de uma amizade existente.
    
    destroy:
    Remove uma amizade existente.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Retorna apenas as amizades do usuário autenticado"""
        user = self.request.user
        return Friendship.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        )
    
    def get_serializer_class(self):
        """Seleciona o serializer apropriado com base na ação"""
        if self.action == 'create':
            return FriendshipCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return FriendshipUpdateSerializer
        return FriendshipSerializer
    
    def perform_create(self, serializer):
        """Define o usuário autenticado como remetente da solicitação"""
        serializer.save(sender=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_friends(self, request):
        """Retorna apenas as amizades aceitas do usuário"""
        user = request.user
        queryset = Friendship.objects.filter(
            (models.Q(sender=user) | models.Q(receiver=user)) &
            models.Q(status='accepted')
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_requests(self, request):
        """Retorna solicitações de amizade pendentes recebidas pelo usuário"""
        queryset = Friendship.objects.filter(receiver=request.user, status='pending')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Aceita uma solicitação de amizade"""
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response(
                {"detail": "Você só pode aceitar solicitações enviadas para você."},
                status=status.HTTP_403_FORBIDDEN
            )
        friendship.status = 'accepted'
        friendship.save()
        serializer = self.get_serializer(friendship)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Rejeita uma solicitação de amizade"""
        friendship = self.get_object()
        if friendship.receiver != request.user:
            return Response(
                {"detail": "Você só pode rejeitar solicitações enviadas para você."},
                status=status.HTTP_403_FORBIDDEN
            )
        friendship.status = 'rejected'
        friendship.save()
        serializer = self.get_serializer(friendship)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        """Bloqueia um usuário"""
        friendship = self.get_object()
        if friendship.receiver != request.user and friendship.sender != request.user:
            return Response(
                {"detail": "Você só pode bloquear usuários relacionados a você."},
                status=status.HTTP_403_FORBIDDEN
            )
        friendship.status = 'blocked'
        friendship.save()
        serializer = self.get_serializer(friendship)
        return Response(serializer.data)


class GameReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint para avaliações de jogos.
    
    list:
    Retorna uma lista de todas as avaliações.
    
    retrieve:
    Retorna os detalhes de uma avaliação específica.
    
    create:
    Cria uma nova avaliação.
    
    update:
    Atualiza uma avaliação existente.
    
    destroy:
    Remove uma avaliação existente.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['game', 'user', 'is_recommended']
    ordering_fields = ['created_at', 'rating', 'helpful_votes']
    ordering = ['-created_at']
    search_fields = ['title', 'content']
    
    def get_queryset(self):
        """Retorna todas as avaliações, mas permite filtrar por jogo"""
        queryset = GameReview.objects.all()
        game_id = self.request.query_params.get('game', None)
        if game_id:
            queryset = queryset.filter(game_id=game_id)
        return queryset
    
    def get_serializer_class(self):
        """Seleciona o serializer apropriado com base na ação"""
        if self.action in ['create', 'update', 'partial_update']:
            return GameReviewCreateUpdateSerializer
        return GameReviewSerializer
    
    def perform_create(self, serializer):
        """Define o usuário autenticado como autor da avaliação"""
        # Obtém o tempo de jogo do usuário para este jogo, se disponível
        from purchases.models import LibraryItem
        game = serializer.validated_data['game']
        try:
            library_item = LibraryItem.objects.get(
                library__user=self.request.user,
                game=game
            )
            playtime = library_item.playtime
        except LibraryItem.DoesNotExist:
            playtime = 0
            
        serializer.save(
            user=self.request.user,
            playtime_at_review=playtime
        )
        
        # Cria uma atividade de usuário para esta avaliação
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='review',
            game=game,
            description=f"Avaliou {game.title} com {serializer.validated_data['rating']} estrelas"
        )
    
    def perform_update(self, serializer):
        """Atualiza a avaliação e registra a data de atualização"""
        serializer.save(updated_at=timezone.now())
    
    def perform_destroy(self, instance):
        """Verifica se o usuário é o autor da avaliação antes de excluir"""
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Você não tem permissão para excluir esta avaliação.")
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        """Marca uma avaliação como útil"""
        review = self.get_object()
        if review.user == request.user:
            return Response(
                {"detail": "Você não pode votar na sua própria avaliação."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        vote, created = ReviewVote.objects.get_or_create(
            review=review,
            user=request.user,
            defaults={'vote_type': 'helpful'}
        )
        
        if not created:
            vote.vote_type = 'helpful'
            vote.save()
            
        # Atualiza o contador de votos úteis
        helpful_count = ReviewVote.objects.filter(review=review, vote_type='helpful').count()
        not_helpful_count = ReviewVote.objects.filter(review=review, vote_type='not_helpful').count()
        
        review.helpful_votes = helpful_count
        review.not_helpful_votes = not_helpful_count
        review.save()
        
        return Response({'status': 'success', 'helpful_votes': helpful_count})
    
    @action(detail=True, methods=['post'])
    def mark_not_helpful(self, request, pk=None):
        """Marca uma avaliação como não útil"""
        review = self.get_object()
        if review.user == request.user:
            return Response(
                {"detail": "Você não pode votar na sua própria avaliação."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        vote, created = ReviewVote.objects.get_or_create(
            review=review,
            user=request.user,
            defaults={'vote_type': 'not_helpful'}
        )
        
        if not created:
            vote.vote_type = 'not_helpful'
            vote.save()
            
        # Atualiza o contador de votos não úteis
        helpful_count = ReviewVote.objects.filter(review=review, vote_type='helpful').count()
        not_helpful_count = ReviewVote.objects.filter(review=review, vote_type='not_helpful').count()
        
        review.helpful_votes = helpful_count
        review.not_helpful_votes = not_helpful_count
        review.save()
        
        return Response({'status': 'success', 'not_helpful_votes': not_helpful_count})


class ReviewCommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint para comentários em avaliações.
    
    list:
    Retorna uma lista de todos os comentários.
    
    retrieve:
    Retorna os detalhes de um comentário específico.
    
    create:
    Cria um novo comentário.
    
    update:
    Atualiza um comentário existente.
    
    destroy:
    Remove um comentário existente.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['review', 'user']
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    def get_queryset(self):
        """Retorna todos os comentários, mas permite filtrar por avaliação"""
        queryset = ReviewComment.objects.all()
        review_id = self.request.query_params.get('review', None)
        if review_id:
            queryset = queryset.filter(review_id=review_id)
        return queryset
    
    def get_serializer_class(self):
        """Seleciona o serializer apropriado com base na ação"""
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewCommentCreateSerializer
        return ReviewCommentSerializer
    
    def perform_create(self, serializer):
        """Define o usuário autenticado como autor do comentário"""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Atualiza o comentário e registra a data de atualização"""
        serializer.save(updated_at=timezone.now())
    
    def perform_destroy(self, instance):
        """Verifica se o usuário é o autor do comentário antes de excluir"""
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Você não tem permissão para excluir este comentário.")
        instance.delete()


class UserActivityViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    API endpoint para atividades de usuários.
    
    list:
    Retorna uma lista de todas as atividades públicas.
    
    retrieve:
    Retorna os detalhes de uma atividade específica.
    """
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'activity_type', 'game']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Retorna atividades públicas de todos os usuários e
        atividades privadas apenas do usuário autenticado
        """
        user = self.request.user
        return UserActivity.objects.filter(
            models.Q(is_public=True) | models.Q(user=user)
        )
    
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Retorna apenas as atividades do usuário autenticado"""
        queryset = UserActivity.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def friends_activities(self, request):
        """Retorna atividades públicas dos amigos do usuário"""
        # Obtém IDs dos amigos
        friends_ids = Friendship.objects.filter(
            (models.Q(sender=request.user) | models.Q(receiver=request.user)) &
            models.Q(status='accepted')
        ).values_list(
            'sender', 'receiver'
        ).distinct()
        
        # Filtra IDs para excluir o próprio usuário
        friend_ids = []
        for sender_id, receiver_id in friends_ids:
            if sender_id != request.user.id:
                friend_ids.append(sender_id)
            if receiver_id != request.user.id:
                friend_ids.append(receiver_id)
        
        # Obtém atividades públicas dos amigos
        queryset = UserActivity.objects.filter(
            user_id__in=friend_ids,
            is_public=True
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GameRecommendationViewSet(viewsets.ModelViewSet):
    """
    API endpoint para recomendações de jogos.
    
    list:
    Retorna uma lista de todas as recomendações do usuário autenticado.
    
    retrieve:
    Retorna os detalhes de uma recomendação específica.
    
    create:
    Cria uma nova recomendação.
    
    update:
    Atualiza uma recomendação existente.
    
    destroy:
    Remove uma recomendação existente.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['sender', 'receiver', 'game', 'is_read']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Retorna apenas as recomendações enviadas ou recebidas pelo usuário autenticado"""
        user = self.request.user
        return GameRecommendation.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user)
        )
    
    def get_serializer_class(self):
        """Seleciona o serializer apropriado com base na ação"""
        if self.action in ['create', 'update', 'partial_update']:
            return GameRecommendationCreateSerializer
        return GameRecommendationSerializer
    
    def perform_create(self, serializer):
        """Define o usuário autenticado como remetente da recomendação"""
        serializer.save(sender=self.request.user)
    
    @action(detail=False, methods=['get'])
    def received(self, request):
        """Retorna apenas as recomendações recebidas pelo usuário"""
        queryset = GameRecommendation.objects.filter(receiver=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Retorna apenas as recomendações enviadas pelo usuário"""
        queryset = GameRecommendation.objects.filter(sender=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Marca uma recomendação como lida"""
        recommendation = self.get_object()
        if recommendation.receiver != request.user:
            return Response(
                {"detail": "Você só pode marcar como lida recomendações enviadas para você."},
                status=status.HTTP_403_FORBIDDEN
            )
        recommendation.is_read = True
        recommendation.save()
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data)


class UserGamePreferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint para preferências de jogos dos usuários.
    
    list:
    Retorna uma lista de todas as preferências do usuário autenticado.
    
    retrieve:
    Retorna os detalhes de uma preferência específica.
    
    create:
    Cria uma nova preferência.
    
    update:
    Atualiza uma preferência existente.
    
    destroy:
    Remove uma preferência existente.
    """
    serializer_class = UserGamePreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas as preferências do usuário autenticado"""
        return UserGamePreference.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Define o usuário autenticado como dono da preferência"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recommended_games(self, request):
        """Retorna jogos recomendados com base nas preferências do usuário"""
        # Obtém os gêneros preferidos do usuário com seus pesos
        user_preferences = UserGamePreference.objects.filter(
            user=request.user
        ).select_related('genre')
        
        if not user_preferences.exists():
            return Response(
                {"detail": "Você precisa definir suas preferências de gêneros primeiro."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cria um dicionário de pesos por gênero
        genre_weights = {pref.genre_id: pref.weight for pref in user_preferences}
        genre_ids = list(genre_weights.keys())
        
        # Obtém jogos que correspondem aos gêneros preferidos
        from django.db.models import Count, F, ExpressionWrapper, FloatField, Case, When, Value
        
        # Cria uma expressão para calcular a pontuação de cada jogo
        # baseada nos pesos dos gêneros e no desconto atual
        games = Game.objects.filter(
            genres__id__in=genre_ids,
            is_active=True
        ).annotate(
            matching_genres=Count('genres', filter=models.Q(genres__id__in=genre_ids)),
            # Calcula um bônus para jogos em promoção
            discount_bonus=ExpressionWrapper(
                F('discount_percent') / 10.0,
                output_field=FloatField()
            )
        ).distinct()
        
        # Adiciona uma pontuação personalizada para cada jogo
        scored_games = []
        for game in games:
            # Calcula a pontuação baseada nos gêneros do jogo e seus pesos
            score = 0
            for genre in game.genres.all():
                if genre.id in genre_weights:
                    score += genre_weights[genre.id]
            
            # Adiciona bônus para jogos em promoção
            if game.discount_percent > 0:
                score += game.discount_percent / 10.0
                
            scored_games.append((game, score))
        
        # Ordena os jogos por pontuação
        scored_games.sort(key=lambda x: x[1], reverse=True)
        
        # Limita a 10 jogos
        top_games = [game for game, score in scored_games[:10]]
        
        # Serializa os jogos
        from games.api.serializers import GameListSerializer
        serializer = GameListSerializer(top_games, many=True)
        return Response(serializer.data)
