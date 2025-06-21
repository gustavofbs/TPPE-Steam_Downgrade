from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Genre(models.Model):
    """Modelo para gêneros de jogos (ação, aventura, RPG, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Developer(models.Model):
    """Modelo para desenvolvedores de jogos"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    founded_date = models.DateField(null=True, blank=True)
    logo = models.ImageField(upload_to='developers/', blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Publisher(models.Model):
    """Modelo para publicadoras de jogos"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    founded_date = models.DateField(null=True, blank=True)
    logo = models.ImageField(upload_to='publishers/', blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Game(models.Model):
    """Modelo principal para jogos"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    release_date = models.DateField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    cover_image = models.ImageField(upload_to='games/covers/')
    banner_image = models.ImageField(upload_to='games/banners/', blank=True)
    
    # Relações
    genres = models.ManyToManyField(Genre, related_name='games')
    developer = models.ForeignKey(Developer, on_delete=models.PROTECT, related_name='developed_games')
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name='published_games')
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def current_price(self):
        """Calcula o preço atual com desconto"""
        if self.discount_percent > 0:
            discount = (self.discount_percent / 100) * self.base_price
            return self.base_price - discount
        return self.base_price
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-release_date']

class GameVersion(models.Model):
    """Modelo para diferentes versões de um jogo (importante para downgrade)"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50)
    release_date = models.DateField()
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.game.title} - v{self.version_number}"
    
    class Meta:
        ordering = ['-release_date']
        unique_together = ['game', 'version_number']

class GameImage(models.Model):
    """Modelo para screenshots e imagens adicionais de jogos"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='games/screenshots/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Image for {self.game.title}"
    
    class Meta:
        ordering = ['order']

class SystemRequirement(models.Model):
    """Modelo para requisitos de sistema dos jogos"""
    REQUIREMENT_TYPE_CHOICES = (
        ('minimum', 'Mínimos'),
        ('recommended', 'Recomendados'),
    )
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='system_requirements')
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPE_CHOICES)
    os = models.CharField(max_length=100)
    processor = models.CharField(max_length=200)
    memory = models.CharField(max_length=100)
    graphics = models.CharField(max_length=200)
    directx = models.CharField(max_length=100, blank=True)
    storage = models.CharField(max_length=100)
    additional_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.game.title} - {self.get_requirement_type_display()}"
    
    class Meta:
        unique_together = ['game', 'requirement_type']
