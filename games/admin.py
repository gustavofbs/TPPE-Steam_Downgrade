from django.contrib import admin
from .models import Genre, Developer, Publisher, Game, GameVersion, GameImage, SystemRequirement

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'founded_date')
    search_fields = ('name',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'founded_date')
    search_fields = ('name',)

class GameVersionInline(admin.TabularInline):
    model = GameVersion
    extra = 1

class GameImageInline(admin.TabularInline):
    model = GameImage
    extra = 3

class SystemRequirementInline(admin.TabularInline):
    model = SystemRequirement
    extra = 2
    max_num = 2

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer', 'publisher', 'release_date', 'base_price', 'discount_percent', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'genres', 'developer', 'publisher')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'release_date'
    inlines = [GameVersionInline, GameImageInline, SystemRequirementInline]

@admin.register(GameVersion)
class GameVersionAdmin(admin.ModelAdmin):
    list_display = ('game', 'version_number', 'release_date', 'is_available')
    list_filter = ('is_available', 'release_date')
    search_fields = ('game__title', 'version_number')

@admin.register(GameImage)
class GameImageAdmin(admin.ModelAdmin):
    list_display = ('game', 'caption', 'order')
    list_filter = ('game',)
    search_fields = ('game__title', 'caption')

@admin.register(SystemRequirement)
class SystemRequirementAdmin(admin.ModelAdmin):
    list_display = ('game', 'requirement_type', 'os')
    list_filter = ('requirement_type', 'os')
    search_fields = ('game__title',)
