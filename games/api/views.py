from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from games.models import Game, Genre, Developer, Publisher, GameVersion, GameImage, SystemRequirement
from .serializers import (
    GameListSerializer,
    GameDetailSerializer,
    GameCreateUpdateSerializer,
    GenreSerializer,
    DeveloperSerializer,
    PublisherSerializer,
    GameVersionSerializer,
    GameImageSerializer,
    SystemRequirementSerializer
)
from .filters import GameFilter


class GenreViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    API endpoint para gêneros de jogos.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class DeveloperViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    API endpoint para desenvolvedores de jogos.
    """
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class PublisherViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """
    API endpoint para publicadoras de jogos.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class GameViewSet(mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    """
    API endpoint para jogos.
    
    list:
    Retorna uma lista de todos os jogos.
    
    retrieve:
    Retorna os detalhes de um jogo específico.
    
    create:
    Cria um novo jogo.
    
    update:
    Atualiza um jogo existente.
    
    destroy:
    Remove um jogo existente.
    """
    queryset = Game.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = GameFilter
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['title', 'release_date', 'base_price', 'created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        """Retorna o serializer apropriado com base na ação"""
        if self.action == 'list':
            return GameListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return GameCreateUpdateSerializer
        return GameDetailSerializer
    
    @action(detail=True, methods=['get'])
    def versions(self, request, slug=None):
        """
        Retorna todas as versões de um jogo específico.
        """
        game = self.get_object()
        versions = GameVersion.objects.filter(game=game)
        serializer = GameVersionSerializer(versions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def images(self, request, slug=None):
        """
        Retorna todas as imagens de um jogo específico.
        """
        game = self.get_object()
        images = GameImage.objects.filter(game=game)
        serializer = GameImageSerializer(images, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def requirements(self, request, slug=None):
        """
        Retorna todos os requisitos de sistema de um jogo específico.
        """
        game = self.get_object()
        requirements = SystemRequirement.objects.filter(game=game)
        serializer = SystemRequirementSerializer(requirements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Retorna jogos em destaque.
        """
        featured_games = Game.objects.filter(is_featured=True, is_active=True)
        page = self.paginate_queryset(featured_games)
        if page is not None:
            serializer = GameListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = GameListSerializer(featured_games, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        """
        Retorna jogos em promoção.
        """
        sale_games = Game.objects.filter(discount_percent__gt=0, is_active=True)
        page = self.paginate_queryset(sale_games)
        if page is not None:
            serializer = GameListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = GameListSerializer(sale_games, many=True)
        return Response(serializer.data)


class GameVersionViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    API endpoint para versões de jogos.
    """
    queryset = GameVersion.objects.all()
    serializer_class = GameVersionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game', 'is_available']
    
    def perform_create(self, serializer):
        game_id = self.request.data.get('game')
        game = get_object_or_404(Game, id=game_id)
        serializer.save(game=game)


class GameImageViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    API endpoint para imagens de jogos.
    """
    queryset = GameImage.objects.all()
    serializer_class = GameImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game', 'is_cover']
    
    def perform_create(self, serializer):
        game_id = self.request.data.get('game')
        game = get_object_or_404(Game, id=game_id)
        serializer.save(game=game)


class SystemRequirementViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    API endpoint para requisitos de sistema de jogos.
    """
    queryset = SystemRequirement.objects.all()
    serializer_class = SystemRequirementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['game', 'requirement_type']
    
    def perform_create(self, serializer):
        game_id = self.request.data.get('game')
        game = get_object_or_404(Game, id=game_id)
        serializer.save(game=game)
