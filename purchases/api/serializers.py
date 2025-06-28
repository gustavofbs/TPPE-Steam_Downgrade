from rest_framework import serializers
from purchases.models import (
    Cart, CartItem, Order, OrderItem,
    Library, LibraryItem, DownloadHistory,
    Wishlist, WishlistItem, Coupon
)
from games.api.serializers import GameListSerializer, GameDetailSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer para itens do carrinho"""
    game_detail = GameListSerializer(source='game', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'game', 'game_detail', 'quantity', 'added_at', 'subtotal']
        read_only_fields = ['id', 'added_at', 'subtotal']
    
    def to_representation(self, instance):
        """Adiciona o subtotal calculado à representação"""
        representation = super().to_representation(instance)
        representation['subtotal'] = str(instance.subtotal())
        return representation


class CartSerializer(serializers.ModelSerializer):
    """Serializer para o carrinho de compras"""
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'total_items', 'total_price']
    
    def get_total_price(self, obj):
        """Retorna o preço total do carrinho"""
        return str(obj.total_price())


class CartItemCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar/atualizar itens do carrinho"""
    class Meta:
        model = CartItem
        fields = ['game', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer para itens do pedido"""
    game_detail = GameListSerializer(source='game', read_only=True)
    # Não temos GameVersionSerializer, então vamos usar um serializer básico
    game_version_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'game', 'game_detail', 'game_version', 'game_version_detail', 
                  'quantity', 'price', 'discount', 'subtotal']
        read_only_fields = ['id', 'subtotal']
    
    def get_game_version_detail(self, obj):
        """Retorna informações básicas sobre a versão do jogo"""
        if obj.game_version:
            return {
                'id': obj.game_version.id,
                'version_name': obj.game_version.version_name,
                'release_date': obj.game_version.release_date,
                'is_available': obj.game_version.is_available
            }
        return None
    
    def to_representation(self, instance):
        """Adiciona o subtotal calculado à representação"""
        representation = super().to_representation(instance)
        representation['subtotal'] = str(instance.subtotal())
        return representation


class OrderSerializer(serializers.ModelSerializer):
    """Serializer para pedidos"""
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_amount', 'coupon_code', 'coupon_discount',
                 'created_at', 'updated_at', 'payment_method', 'payment_id', 'notes', 'items']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar pedidos"""
    class Meta:
        model = Order
        fields = ['coupon_code', 'payment_method', 'notes']


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualizar pedidos"""
    class Meta:
        model = Order
        fields = ['status', 'payment_id', 'notes']


class LibraryItemSerializer(serializers.ModelSerializer):
    """Serializer para itens da biblioteca"""
    game_detail = GameListSerializer(source='game', read_only=True)
    
    class Meta:
        model = LibraryItem
        fields = ['id', 'game', 'game_detail', 'acquired_at', 'last_played', 'playtime', 'is_favorite']
        read_only_fields = ['id', 'acquired_at']


class DownloadHistorySerializer(serializers.ModelSerializer):
    """Serializer para histórico de downloads"""
    # Não temos GameVersionSerializer, então vamos usar um serializer básico
    game_version_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = DownloadHistory
        fields = ['id', 'library_item', 'game_version', 'game_version_detail', 'downloaded_at', 'ip_address', 'user_agent']
        read_only_fields = ['id', 'downloaded_at', 'ip_address', 'user_agent']
    
    def get_game_version_detail(self, obj):
        """Retorna informações básicas sobre a versão do jogo"""
        if obj.game_version:
            return {
                'id': obj.game_version.id,
                'version_name': obj.game_version.version_name,
                'release_date': obj.game_version.release_date,
                'is_available': obj.game_version.is_available
            }
        return None


class LibrarySerializer(serializers.ModelSerializer):
    """Serializer para a biblioteca de jogos"""
    items = LibraryItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Library
        fields = ['id', 'user', 'items', 'total_games', 'created_at']
        read_only_fields = ['id', 'user', 'created_at', 'total_games']


class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializer para itens da lista de desejos"""
    game_detail = GameListSerializer(source='game', read_only=True)
    
    class Meta:
        model = WishlistItem
        fields = ['id', 'game', 'game_detail', 'added_at', 'priority']
        read_only_fields = ['id', 'added_at']


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer para a lista de desejos"""
    items = WishlistItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'items', 'total_items', 'created_at']
        read_only_fields = ['id', 'user', 'created_at', 'total_items']


class WishlistItemCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar/atualizar itens da lista de desejos"""
    class Meta:
        model = WishlistItem
        fields = ['game', 'priority']


class CouponSerializer(serializers.ModelSerializer):
    """Serializer para cupons de desconto"""
    is_valid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'description', 'discount_percent', 'valid_from', 
                 'valid_to', 'is_active', 'max_uses', 'current_uses', 'is_valid']
        read_only_fields = ['id', 'current_uses', 'is_valid']
    
    def to_representation(self, instance):
        """Adiciona o status de validade do cupom à representação"""
        representation = super().to_representation(instance)
        representation['is_valid'] = instance.is_valid()
        return representation
