from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from games.models import Game

class Friendship(models.Model):
    """Modelo para amizades entre usuários"""
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('accepted', 'Aceito'),
        ('rejected', 'Rejeitado'),
        ('blocked', 'Bloqueado'),
    )
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship_requests_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.sender == self.receiver:
            raise ValidationError("Você não pode ser amigo de si mesmo.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Garante que clean() será chamado antes de salvar
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('sender', 'receiver')
        verbose_name_plural = 'Friendships'
    
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.get_status_display()})"

class GameReview(models.Model):
    """Modelo para avaliações de jogos"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    playtime_at_review = models.PositiveIntegerField(default=0, help_text='Tempo de jogo em minutos quando a avaliação foi feita')
    is_recommended = models.BooleanField(default=True)
    is_spoiler = models.BooleanField(default=False)
    helpful_votes = models.PositiveIntegerField(default=0)
    not_helpful_votes = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'game')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Avaliação de {self.user.username} para {self.game.title}"

class ReviewComment(models.Model):
    """Modelo para comentários em avaliações"""
    review = models.ForeignKey(GameReview, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_spoiler = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comentário de {self.user.username} em avaliação de {self.review.user.username}"

class ReviewVote(models.Model):
    """Modelo para votos em avaliações (se foi útil ou não)"""
    VOTE_CHOICES = (
        ('helpful', 'Útil'),
        ('not_helpful', 'Não Útil'),
    )
    
    review = models.ForeignKey(GameReview, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_votes')
    vote_type = models.CharField(max_length=11, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.user == self.review.user:
            raise ValidationError("Você não pode votar na sua própria avaliação.")

    def save(self, *args, **kwargs):
        self.full_clean()  # chama clean() e aplica as validações antes de salvar
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('review', 'user')
    
    def __str__(self):
        return f"{self.user.username} votou '{self.get_vote_type_display()}' na avaliação de {self.review.user.username}"

class UserActivity(models.Model):
    """Modelo para atividades dos usuários na plataforma"""
    ACTIVITY_TYPES = (
        ('purchase', 'Compra'),
        ('review', 'Avaliação'),
        ('achievement', 'Conquista'),
        ('friend', 'Nova Amizade'),
        ('playtime', 'Tempo de Jogo'),
        ('wishlist', 'Lista de Desejos'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_activities')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User activities'
    
    def __str__(self):
        return f"{self.user.username}: {self.description}"

class GameRecommendation(models.Model):
    """Modelo para recomendações de jogos entre amigos"""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations_sent')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations_received')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='recommendations')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def clean(self):
        if self.sender == self.receiver:
            raise ValidationError("Você não pode recomendar um jogo para si mesmo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.sender.username} recomendou {self.game.title} para {self.receiver.username}"

class UserGamePreference(models.Model):
    """Modelo para preferências de jogos dos usuários (para recomendações)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='game_preferences')
    genre = models.ForeignKey('games.Genre', on_delete=models.CASCADE, related_name='user_preferences')
    weight = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'genre')
    
    def __str__(self):
        return f"{self.user.username} - {self.genre.name} (Peso: {self.weight})"
