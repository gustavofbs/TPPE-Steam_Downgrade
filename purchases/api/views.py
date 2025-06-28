from rest_framework import viewsets, permissions, filters, mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import transaction

from purchases.models import (
    Cart, CartItem, Order, OrderItem,
    Library, LibraryItem, DownloadHistory,
    Wishlist, WishlistItem, Coupon
)
from .serializers import (
    CartSerializer, CartItemSerializer, CartItemCreateSerializer,
    OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer,
    OrderItemSerializer, LibrarySerializer, LibraryItemSerializer,
    DownloadHistorySerializer, WishlistSerializer, WishlistItemSerializer,
    WishlistItemCreateSerializer, CouponSerializer
)
from games.models import Game, GameVersion


class CartViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    """
    API endpoint para carrinhos de compras.
    
    Permite visualizar o carrinho do usuário autenticado.
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas o carrinho do usuário autenticado"""
        return Cart.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Retorna o carrinho do usuário autenticado"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Adiciona um item ao carrinho"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            game_id = serializer.validated_data['game'].id
            quantity = serializer.validated_data['quantity']
            
            # Verifica se o jogo já está no carrinho
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                game_id=game_id,
                defaults={'quantity': quantity}
            )
            
            # Se o item já existia, atualiza a quantidade
            if not created:
                cart_item.quantity = quantity
                cart_item.save()
            
            # Retorna o carrinho atualizado
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove um item do carrinho"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        game_id = request.data.get('game')
        
        if not game_id:
            return Response(
                {'error': 'É necessário fornecer o ID do jogo'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart_item = CartItem.objects.get(cart=cart, game_id=game_id)
            cart_item.delete()
            
            # Retorna o carrinho atualizado
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item não encontrado no carrinho'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Remove todos os itens do carrinho"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        
        # Retorna o carrinho vazio
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data)


class OrderViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    """
    API endpoint para pedidos.
    
    list:
    Retorna uma lista de todos os pedidos do usuário autenticado.
    
    retrieve:
    Retorna os detalhes de um pedido específico.
    
    create:
    Cria um novo pedido a partir do carrinho atual.
    
    update:
    Atualiza um pedido existente (apenas status, payment_id e notes).
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Retorna apenas os pedidos do usuário autenticado"""
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Seleciona o serializer apropriado com base na ação"""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return OrderUpdateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """Cria um pedido a partir do carrinho atual"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Obtém o carrinho do usuário
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Carrinho não encontrado ou vazio'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o carrinho tem itens
        if cart.items.count() == 0:
            return Response(
                {'error': 'Carrinho vazio'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Processa o cupom, se fornecido
        coupon_code = serializer.validated_data.get('coupon_code', '')
        coupon_discount = 0
        
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid():
                    # Calcula o desconto do cupom
                    total_before_discount = cart.total_price()
                    coupon_discount = coupon.calculate_discount(total_before_discount)
                    
                    # Incrementa o uso do cupom
                    coupon.current_uses += 1
                    coupon.save()
                else:
                    return Response(
                        {'error': 'Cupom inválido ou expirado'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Coupon.DoesNotExist:
                return Response(
                    {'error': 'Cupom não encontrado'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Cria o pedido e os itens do pedido em uma transação
        with transaction.atomic():
            # Cria o pedido
            order = Order.objects.create(
                user=request.user,
                status='pending',
                total_amount=cart.total_price() - coupon_discount,
                coupon_code=coupon_code,
                coupon_discount=coupon_discount,
                payment_method=serializer.validated_data.get('payment_method', ''),
                notes=serializer.validated_data.get('notes', '')
            )
            
            # Cria os itens do pedido
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    game=cart_item.game,
                    quantity=cart_item.quantity,
                    price=cart_item.game.current_price(),
                    discount=cart_item.game.discount_amount()
                )
            
            # Limpa o carrinho
            cart.items.all().delete()
            
            # Adiciona os jogos à biblioteca do usuário se o pedido for concluído
            if order.status == 'completed':
                self._add_games_to_library(order)
        
        # Retorna o pedido criado
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Atualiza um pedido existente"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Apenas staff pode atualizar pedidos de outros usuários
        if instance.user != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Se o status foi alterado para 'completed', adiciona os jogos à biblioteca
        if 'status' in serializer.validated_data and serializer.validated_data['status'] == 'completed':
            self._add_games_to_library(instance)
        
        return Response(OrderSerializer(instance).data)
    
    def _add_games_to_library(self, order):
        """Adiciona os jogos do pedido à biblioteca do usuário"""
        # Obtém ou cria a biblioteca do usuário
        library, created = Library.objects.get_or_create(user=order.user)
        
        # Adiciona cada jogo à biblioteca
        for item in order.items.all():
            # Verifica se o jogo já está na biblioteca
            if not LibraryItem.objects.filter(library=library, game=item.game).exists():
                LibraryItem.objects.create(
                    library=library,
                    game=item.game
                )


class LibraryViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    API endpoint para bibliotecas de jogos.
    
    Permite visualizar a biblioteca do usuário autenticado.
    """
    serializer_class = LibrarySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas a biblioteca do usuário autenticado"""
        return Library.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_library(self, request):
        """Retorna a biblioteca do usuário autenticado"""
        library, created = Library.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(library)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def record_playtime(self, request, pk=None):
        """Registra tempo de jogo para um item da biblioteca"""
        library = self.get_object()
        
        # Verifica se o usuário é dono da biblioteca
        if library.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        game_id = request.data.get('game')
        minutes = request.data.get('minutes')
        
        if not game_id or not minutes:
            return Response(
                {'error': 'É necessário fornecer o ID do jogo e os minutos jogados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            minutes = int(minutes)
            if minutes <= 0:
                raise ValueError()
        except ValueError:
            return Response(
                {'error': 'Os minutos devem ser um número inteiro positivo'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            library_item = LibraryItem.objects.get(library=library, game_id=game_id)
            library_item.playtime_minutes += minutes
            library_item.last_played = timezone.now()
            library_item.save()
            
            serializer = LibraryItemSerializer(library_item)
            return Response(serializer.data)
        except LibraryItem.DoesNotExist:
            return Response(
                {'error': 'Jogo não encontrado na biblioteca'},
                status=status.HTTP_404_NOT_FOUND
            )


class DownloadHistoryViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    """
    API endpoint para histórico de downloads.
    
    Permite registrar downloads de jogos e listar o histórico.
    """
    serializer_class = DownloadHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['library_item', 'game_version']
    ordering_fields = ['downloaded_at']
    ordering = ['-downloaded_at']
    
    def get_queryset(self):
        """Retorna apenas o histórico de downloads do usuário autenticado"""
        library = Library.objects.get(user=self.request.user)
        return DownloadHistory.objects.filter(library_item__library=library)
    
    def create(self, request, *args, **kwargs):
        """Registra um novo download"""
        library_item_id = request.data.get('library_item')
        game_version_id = request.data.get('game_version')
        
        if not library_item_id or not game_version_id:
            return Response(
                {'error': 'É necessário fornecer o ID do item da biblioteca e da versão do jogo'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verifica se o item da biblioteca pertence ao usuário
        try:
            library_item = LibraryItem.objects.get(id=library_item_id)
            if library_item.library.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except LibraryItem.DoesNotExist:
            return Response(
                {'error': 'Item da biblioteca não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verifica se a versão do jogo existe e pertence ao jogo do item da biblioteca
        try:
            game_version = GameVersion.objects.get(id=game_version_id)
            if game_version.game != library_item.game:
                return Response(
                    {'error': 'A versão do jogo não corresponde ao jogo do item da biblioteca'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except GameVersion.DoesNotExist:
            return Response(
                {'error': 'Versão do jogo não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Registra o download
        download = DownloadHistory.objects.create(
            library_item=library_item,
            game_version=game_version,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        serializer = self.get_serializer(download)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WishlistViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    """
    API endpoint para listas de desejos.
    
    Permite visualizar a lista de desejos do usuário autenticado.
    """
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas a lista de desejos do usuário autenticado"""
        return Wishlist.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_wishlist(self, request):
        """Retorna a lista de desejos do usuário autenticado"""
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(wishlist)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Adiciona um item à lista de desejos"""
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistItemCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            game_id = serializer.validated_data['game'].id
            priority = serializer.validated_data.get('priority', 0)
            
            # Verifica se o jogo já está na lista de desejos
            wishlist_item, created = WishlistItem.objects.get_or_create(
                wishlist=wishlist,
                game_id=game_id,
                defaults={'priority': priority}
            )
            
            # Se o item já existia, atualiza a prioridade
            if not created:
                wishlist_item.priority = priority
                wishlist_item.save()
            
            # Retorna a lista de desejos atualizada
            wishlist_serializer = WishlistSerializer(wishlist)
            return Response(wishlist_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove um item da lista de desejos"""
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        game_id = request.data.get('game')
        
        if not game_id:
            return Response(
                {'error': 'É necessário fornecer o ID do jogo'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            wishlist_item = WishlistItem.objects.get(wishlist=wishlist, game_id=game_id)
            wishlist_item.delete()
            
            # Retorna a lista de desejos atualizada
            wishlist_serializer = WishlistSerializer(wishlist)
            return Response(wishlist_serializer.data)
        except WishlistItem.DoesNotExist:
            return Response(
                {'error': 'Item não encontrado na lista de desejos'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Remove todos os itens da lista de desejos"""
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.items.all().delete()
        
        # Retorna a lista de desejos vazia
        wishlist_serializer = WishlistSerializer(wishlist)
        return Response(wishlist_serializer.data)


class CouponViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    API endpoint para cupons de desconto.
    
    list:
    Retorna uma lista de todos os cupons (apenas para staff).
    
    retrieve:
    Retorna os detalhes de um cupom específico (apenas para staff).
    
    create:
    Cria um novo cupom (apenas para staff).
    
    update:
    Atualiza um cupom existente (apenas para staff).
    
    destroy:
    Remove um cupom existente (apenas para staff).
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['code', 'description']
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def validate(self, request):
        """Valida um cupom (disponível para usuários autenticados)"""
        code = request.data.get('code')
        
        if not code:
            return Response(
                {'error': 'É necessário fornecer o código do cupom'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            coupon = Coupon.objects.get(code=code)
            is_valid = coupon.is_valid()
            
            return Response({
                'code': coupon.code,
                'discount_percent': coupon.discount_percent,
                'is_valid': is_valid,
                'message': 'Cupom válido' if is_valid else 'Cupom inválido ou expirado'
            })
        except Coupon.DoesNotExist:
            return Response(
                {'error': 'Cupom não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
