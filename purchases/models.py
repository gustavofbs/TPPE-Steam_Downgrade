from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from games.models import Game, GameVersion

class Cart(models.Model):
    """Modelo para o carrinho de compras do usuário"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Carrinho de {self.user.username}"
    
    def total_items(self):
        return self.items.count()
    
    def total_price(self):
        return sum(item.game.current_price() * item.quantity for item in self.items.all())

class CartItem(models.Model):
    """Modelo para itens no carrinho de compras"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'game')
    
    def __str__(self):
        return f"{self.game.title} ({self.quantity}) - {self.cart}"
    
    def subtotal(self):
        return self.game.current_price() * self.quantity

class Order(models.Model):
    """Modelo para pedidos/compras"""
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=100, blank=True)
    payment_id = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    """Modelo para itens em um pedido"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    game_version = models.ForeignKey(GameVersion, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f"{self.game.title} - Pedido #{self.order.id}"
    
    def subtotal(self):
        return (self.price - self.discount) * self.quantity

class Library(models.Model):
    """Modelo para a biblioteca de jogos do usuário"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='library')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Biblioteca de {self.user.username}"
    
    def total_games(self):
        return self.items.count()

class LibraryItem(models.Model):
    """Modelo para itens na biblioteca de jogos do usuário"""
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    acquired_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='library_items')
    playtime = models.PositiveIntegerField(default=0, help_text='Tempo de jogo em minutos')
    last_played = models.DateTimeField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('library', 'game')
    
    def __str__(self):
        return f"{self.game.title} - {self.library}"
    
    def formatted_playtime(self):
        """Retorna o tempo de jogo formatado em horas e minutos"""
        hours = self.playtime // 60
        minutes = self.playtime % 60
        return f"{hours}h {minutes}min"

class DownloadHistory(models.Model):
    """Modelo para histórico de downloads de jogos e versões"""
    library_item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE, related_name='downloads')
    game_version = models.ForeignKey(GameVersion, on_delete=models.PROTECT)
    downloaded_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.game_version} - {self.downloaded_at}"
    
    class Meta:
        ordering = ['-downloaded_at']
        verbose_name_plural = 'Download histories'

class Wishlist(models.Model):
    """Modelo para lista de desejos do usuário"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Lista de desejos de {self.user.username}"
    
    def total_items(self):
        return self.items.count()

class WishlistItem(models.Model):
    """Modelo para itens na lista de desejos"""
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    priority = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    
    class Meta:
        unique_together = ('wishlist', 'game')
        ordering = ['-priority', 'added_at']
    
    def __str__(self):
        return f"{self.game.title} - {self.wishlist}"

class Coupon(models.Model):
    """Modelo para cupons de desconto"""
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_uses = models.PositiveIntegerField(default=0, help_text='0 para usos ilimitados')
    current_uses = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.code} ({self.discount_percent}% off)"
    
    def is_valid(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        if self.max_uses > 0 and self.current_uses >= self.max_uses:
            return False
        return True
