from rest_framework import serializers
from social.models import (
    Friendship, GameReview, ReviewComment, ReviewVote,
    UserActivity, GameRecommendation, UserGamePreference
)
from django.contrib.auth import get_user_model
from games.api.serializers import GameListSerializer

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    """Serializer básico para informações de usuário"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'first_name', 'last_name']


class FriendshipSerializer(serializers.ModelSerializer):
    """Serializer para amizades"""
    sender_detail = UserBasicSerializer(source='sender', read_only=True)
    receiver_detail = UserBasicSerializer(source='receiver', read_only=True)
    
    class Meta:
        model = Friendship
        fields = ['id', 'sender', 'receiver', 'sender_detail', 'receiver_detail', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FriendshipCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar solicitações de amizade"""
    class Meta:
        model = Friendship
        fields = ['receiver']


class FriendshipUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualizar status de amizade"""
    class Meta:
        model = Friendship
        fields = ['status']
        read_only_fields = ['sender', 'receiver']


class ReviewVoteSerializer(serializers.ModelSerializer):
    """Serializer para votos em avaliações"""
    user_detail = UserBasicSerializer(source='user', read_only=True)
    
    class Meta:
        model = ReviewVote
        fields = ['id', 'review', 'user', 'user_detail', 'vote_type', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ReviewCommentSerializer(serializers.ModelSerializer):
    """Serializer para comentários em avaliações"""
    user_detail = UserBasicSerializer(source='user', read_only=True)
    
    class Meta:
        model = ReviewComment
        fields = ['id', 'review', 'user', 'user_detail', 'content', 'created_at', 'updated_at', 'is_spoiler']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class GameReviewSerializer(serializers.ModelSerializer):
    """Serializer para avaliações de jogos"""
    user_detail = UserBasicSerializer(source='user', read_only=True)
    game_detail = GameListSerializer(source='game', read_only=True)
    comments = ReviewCommentSerializer(many=True, read_only=True)
    votes = ReviewVoteSerializer(many=True, read_only=True)
    
    class Meta:
        model = GameReview
        fields = [
            'id', 'user', 'user_detail', 'game', 'game_detail', 'rating', 'title', 'content',
            'created_at', 'updated_at', 'playtime_at_review', 'is_recommended', 'is_spoiler',
            'helpful_votes', 'not_helpful_votes', 'comments', 'votes'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'helpful_votes', 'not_helpful_votes']


class GameReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para criar/atualizar avaliações de jogos"""
    class Meta:
        model = GameReview
        fields = ['game', 'rating', 'title', 'content', 'is_recommended', 'is_spoiler']


class ReviewCommentCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar comentários em avaliações"""
    class Meta:
        model = ReviewComment
        fields = ['review', 'content', 'is_spoiler']


class ReviewVoteCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar votos em avaliações"""
    class Meta:
        model = ReviewVote
        fields = ['review', 'vote_type']


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer para atividades de usuários"""
    user_detail = UserBasicSerializer(source='user', read_only=True)
    game_detail = GameListSerializer(source='game', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'user_detail', 'activity_type', 'game', 'game_detail', 'description', 'created_at', 'is_public']
        read_only_fields = ['id', 'user', 'created_at']


class GameRecommendationSerializer(serializers.ModelSerializer):
    """Serializer para recomendações de jogos"""
    sender_detail = UserBasicSerializer(source='sender', read_only=True)
    receiver_detail = UserBasicSerializer(source='receiver', read_only=True)
    game_detail = GameListSerializer(source='game', read_only=True)
    
    class Meta:
        model = GameRecommendation
        fields = ['id', 'sender', 'sender_detail', 'receiver', 'receiver_detail', 'game', 'game_detail', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'sender', 'created_at']


class GameRecommendationCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar recomendações de jogos"""
    class Meta:
        model = GameRecommendation
        fields = ['receiver', 'game', 'message']


class UserGamePreferenceSerializer(serializers.ModelSerializer):
    """Serializer para preferências de jogos dos usuários"""
    genre_name = serializers.ReadOnlyField(source='genre.name')
    
    class Meta:
        model = UserGamePreference
        fields = ['id', 'user', 'genre', 'genre_name', 'weight', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
