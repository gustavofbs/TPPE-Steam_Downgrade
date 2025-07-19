from rest_framework import serializers
from games.models import Game, Genre, Developer, Publisher, GameVersion, GameImage, SystemRequirement


class GenreSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Genre"""
    
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'slug']
        read_only_fields = ['slug']


class DeveloperSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Developer"""
    
    class Meta:
        model = Developer
        fields = ['id', 'name', 'description', 'website', 'founded_date', 'logo', 'is_active']


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Publisher"""
    
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'description', 'website', 'founded_date', 'logo', 'is_active']


class SystemRequirementSerializer(serializers.ModelSerializer):
    """Serializer para o modelo SystemRequirement"""
    
    class Meta:
        model = SystemRequirement
        fields = [
            'id', 'requirement_type', 'os', 'processor', 'memory', 
            'graphics', 'directx', 'storage', 'additional_notes'
        ]
        read_only_fields = ['game']


class GameImageSerializer(serializers.ModelSerializer):
    """Serializer para o modelo GameImage"""
    image = serializers.SerializerMethodField()
    
    def get_image(self, obj):
        """Retorna a URL completa da imagem"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    class Meta:
        model = GameImage
        fields = ['id', 'image', 'caption', 'order', 'is_cover']
        read_only_fields = ['game']


class GameVersionSerializer(serializers.ModelSerializer):
    """Serializer para o modelo GameVersion"""
    formatted_file_size = serializers.ReadOnlyField()
    
    class Meta:
        model = GameVersion
        fields = [
            'id', 'version_number', 'release_date', 'description', 
            'is_available', 'file_size_mb', 'download_url', 'formatted_file_size'
        ]
        read_only_fields = ['game']


class GameListSerializer(serializers.ModelSerializer):
    """Serializer para listar jogos (versão resumida)"""
    developer_name = serializers.ReadOnlyField(source='developer.name')
    publisher_name = serializers.ReadOnlyField(source='publisher.name')
    genres = serializers.StringRelatedField(many=True, read_only=True)
    discount_price = serializers.ReadOnlyField()
    is_on_sale = serializers.ReadOnlyField()
    cover_image = serializers.SerializerMethodField()
    
    def get_cover_image(self, obj):
        """Retorna a URL completa da imagem de capa"""
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None
    
    class Meta:
        model = Game
        fields = [
            'id', 'title', 'slug', 'short_description', 'release_date', 
            'base_price', 'discount_percent', 'discount_price', 'is_on_sale',
            'cover_image', 'developer_name', 'publisher_name', 'genres',
            'is_featured', 'is_active'
        ]


class GameDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalhes de um jogo"""
    developer = DeveloperSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    versions = GameVersionSerializer(many=True, read_only=True)
    images = GameImageSerializer(many=True, read_only=True)
    system_requirements = SystemRequirementSerializer(many=True, read_only=True)
    discount_price = serializers.ReadOnlyField()
    is_on_sale = serializers.ReadOnlyField()
    cover_image = serializers.SerializerMethodField()
    banner_image = serializers.SerializerMethodField()
    
    def get_cover_image(self, obj):
        """Retorna a URL completa da imagem de capa"""
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None
    
    def get_banner_image(self, obj):
        """Retorna a URL completa da imagem de banner"""
        if obj.banner_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.banner_image.url)
            return obj.banner_image.url
        return None
    
    class Meta:
        model = Game
        fields = [
            'id', 'title', 'slug', 'description', 'short_description', 
            'release_date', 'base_price', 'discount_percent', 'discount_price',
            'is_on_sale', 'cover_image', 'banner_image', 'developer', 'publisher',
            'genres', 'versions', 'images', 'system_requirements',
            'created_at', 'updated_at', 'is_featured', 'is_active'
        ]


class GameCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para criar e atualizar jogos"""
    
    class Meta:
        model = Game
        fields = [
            'title', 'description', 'short_description', 'release_date',
            'base_price', 'discount_percent', 'cover_image', 'banner_image',
            'genres', 'developer', 'publisher', 'is_featured', 'is_active'
        ]
    
    def create(self, validated_data):
        """Criar um novo jogo"""
        genres_data = validated_data.pop('genres', [])
        game = Game.objects.create(**validated_data)
        
        # Adicionar gêneros
        if genres_data:
            game.genres.set(genres_data)
        
        return game
    
    def update(self, instance, validated_data):
        """Atualizar um jogo existente"""
        genres_data = validated_data.pop('genres', None)
        
        # Atualizar campos do jogo
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Atualizar gêneros se fornecidos
        if genres_data is not None:
            instance.genres.set(genres_data)
        
        instance.save()
        return instance
