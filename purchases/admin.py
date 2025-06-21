from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Library, LibraryItem, DownloadHistory, Wishlist, WishlistItem, Coupon

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'updated_at')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'game', 'quantity', 'subtotal', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('game__title', 'cart__user__username')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'game', 'quantity', 'price', 'discount', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('game__title', 'order__user__username')

class LibraryItemInline(admin.TabularInline):
    model = LibraryItem
    extra = 1

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_games', 'created_at')
    search_fields = ('user__username',)
    inlines = [LibraryItemInline]

class DownloadHistoryInline(admin.TabularInline):
    model = DownloadHistory
    extra = 1

@admin.register(LibraryItem)
class LibraryItemAdmin(admin.ModelAdmin):
    list_display = ('library', 'game', 'playtime', 'formatted_playtime', 'last_played', 'is_favorite')
    list_filter = ('is_favorite', 'acquired_at')
    search_fields = ('game__title', 'library__user__username')
    inlines = [DownloadHistoryInline]

@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ('library_item', 'game_version', 'downloaded_at', 'ip_address')
    list_filter = ('downloaded_at',)
    search_fields = ('library_item__game__title', 'library_item__library__user__username')

class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 1

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'created_at')
    search_fields = ('user__username',)
    inlines = [WishlistItemInline]

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'game', 'priority', 'added_at')
    list_filter = ('priority', 'added_at')
    search_fields = ('game__title', 'wishlist__user__username')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 'is_active', 'max_uses', 'current_uses')
    list_filter = ('is_active', 'valid_from', 'valid_to')
    search_fields = ('code', 'description')
    date_hierarchy = 'valid_from'
