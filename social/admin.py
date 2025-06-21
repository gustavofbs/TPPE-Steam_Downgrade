from django.contrib import admin
from .models import Friendship, GameReview, ReviewComment, ReviewVote, UserActivity, GameRecommendation, UserGamePreference

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sender__username', 'receiver__username')
    date_hierarchy = 'created_at'

class ReviewCommentInline(admin.TabularInline):
    model = ReviewComment
    extra = 1

class ReviewVoteInline(admin.TabularInline):
    model = ReviewVote
    extra = 1

@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'rating', 'title', 'is_recommended', 'created_at', 'helpful_votes', 'not_helpful_votes')
    list_filter = ('rating', 'is_recommended', 'is_spoiler', 'created_at')
    search_fields = ('user__username', 'game__title', 'title', 'content')
    date_hierarchy = 'created_at'
    inlines = [ReviewCommentInline, ReviewVoteInline]

@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'created_at', 'is_spoiler')
    list_filter = ('is_spoiler', 'created_at')
    search_fields = ('user__username', 'review__title', 'content')
    date_hierarchy = 'created_at'

@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at')
    search_fields = ('user__username', 'review__title')
    date_hierarchy = 'created_at'

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'game', 'description', 'created_at', 'is_public')
    list_filter = ('activity_type', 'is_public', 'created_at')
    search_fields = ('user__username', 'description', 'game__title')
    date_hierarchy = 'created_at'

@admin.register(GameRecommendation)
class GameRecommendationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'game', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'game__title', 'message')
    date_hierarchy = 'created_at'

@admin.register(UserGamePreference)
class UserGamePreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'genre', 'weight', 'updated_at')
    list_filter = ('weight', 'genre')
    search_fields = ('user__username', 'genre__name')
    date_hierarchy = 'updated_at'
