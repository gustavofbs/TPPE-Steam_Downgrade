from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils import timezone
import datetime

from purchases.models import (
    Cart, CartItem, Order, OrderItem, 
    Library, LibraryItem, DownloadHistory,
    Wishlist, WishlistItem, Coupon
)
from games.models import Game, GameVersion, Developer, Publisher, Genre

User = get_user_model()

class CartModelTest(TestCase):
    """Testes para o modelo Cart"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.developer = Developer.objects.create(
            name="Test Developer",
            website="https://testdev.com"
        )
        
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            website="https://testpub.com"
        )
        
        self.game = Game.objects.create(
            title="Test Game",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        self.cart = Cart.objects.create(user=self.user)
        
    def test_cart_creation(self):
        """Testa se um carrinho é criado corretamente"""
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(str(self.cart), f"Carrinho de {self.user.username}")
        self.assertEqual(self.cart.total_items(), 0)
        self.assertEqual(self.cart.total_price(), 0)
    
    def test_cart_item_addition(self):
        """Testa a adição de itens ao carrinho"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            game=self.game,
            quantity=2
        )
        
        self.assertEqual(self.cart.total_items(), 1)
        self.assertEqual(self.cart.total_price(), Decimal('59.98'))  # 29.99 * 2
        self.assertEqual(cart_item.subtotal(), Decimal('59.98'))
    
    def test_cart_item_unique_constraint(self):
        """Testa se não é possível adicionar o mesmo jogo duas vezes ao carrinho"""
        CartItem.objects.create(
            cart=self.cart,
            game=self.game,
            quantity=1
        )
        
        with self.assertRaises(IntegrityError):
            CartItem.objects.create(
                cart=self.cart,
                game=self.game,
                quantity=1
            )

class OrderModelTest(TestCase):
    """Testes para o modelo Order"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.developer = Developer.objects.create(
            name="Test Developer",
            website="https://testdev.com"
        )
        
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            website="https://testpub.com"
        )
        
        self.game = Game.objects.create(
            title="Test Game",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        self.game_version = GameVersion.objects.create(
            game=self.game,
            version_number="1.0",
            release_date=timezone.now().date(),
            file_size_mb=1000
        )
        
        self.order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('29.99'),
            payment_method='credit_card',
            payment_id='test_payment_123'
        )
    
    def test_order_creation(self):
        """Testa se um pedido é criado corretamente"""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(self.order.total_amount, Decimal('29.99'))
        self.assertEqual(str(self.order), f"Pedido #{self.order.id} - {self.user.username}")
    
    def test_order_item_creation(self):
        """Testa a criação de itens de pedido"""
        order_item = OrderItem.objects.create(
            order=self.order,
            game=self.game,
            game_version=self.game_version,
            quantity=1,
            price=Decimal('29.99'),
            discount=Decimal('0.00')
        )
        
        self.assertEqual(order_item.subtotal(), Decimal('29.99'))
        self.assertEqual(str(order_item), f"{self.game.title} - Pedido #{self.order.id}")
    
    def test_order_status_transition(self):
        """Testa a transição de status de um pedido"""
        self.order.status = 'processing'
        self.order.save()
        self.assertEqual(self.order.status, 'processing')
        
        self.order.status = 'completed'
        self.order.save()
        self.assertEqual(self.order.status, 'completed')

class LibraryModelTest(TestCase):
    """Testes para o modelo Library"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.developer = Developer.objects.create(
            name="Test Developer",
            website="https://testdev.com"
        )
        
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            website="https://testpub.com"
        )
        
        self.game = Game.objects.create(
            title="Test Game",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        self.game_version = GameVersion.objects.create(
            game=self.game,
            version_number="1.0",
            release_date=timezone.now().date(),
            file_size_mb=1000
        )
        
        self.order = Order.objects.create(
            user=self.user,
            status='completed',
            total_amount=Decimal('29.99'),
            payment_method='credit_card',
            payment_id='test_payment_123'
        )
        
        self.library = Library.objects.create(user=self.user)
    
    def test_library_creation(self):
        """Testa se uma biblioteca é criada corretamente"""
        self.assertEqual(self.library.user, self.user)
        self.assertEqual(str(self.library), f"Biblioteca de {self.user.username}")
        self.assertEqual(self.library.total_games(), 0)
    
    def test_library_item_creation(self):
        """Testa a adição de itens à biblioteca"""
        library_item = LibraryItem.objects.create(
            library=self.library,
            game=self.game,
            order=self.order
        )
        
        self.assertEqual(self.library.total_games(), 1)
        self.assertEqual(library_item.playtime, 0)
        self.assertIsNone(library_item.last_played)
        self.assertFalse(library_item.is_favorite)
    
    def test_library_item_playtime(self):
        """Testa o registro de tempo de jogo"""
        library_item = LibraryItem.objects.create(
            library=self.library,
            game=self.game,
            order=self.order,
            playtime=120  # 2 horas em minutos
        )
        
        self.assertEqual(library_item.playtime, 120)
        self.assertEqual(library_item.formatted_playtime(), "2 horas")
        
        library_item.playtime = 90  # 1 hora e 30 minutos
        library_item.save()
        self.assertEqual(library_item.formatted_playtime(), "1 hora e 30 minutos")

class DownloadHistoryModelTest(TestCase):
    """Testes para o modelo DownloadHistory"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.developer = Developer.objects.create(
            name="Test Developer",
            website="https://testdev.com"
        )
        
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            website="https://testpub.com"
        )
        
        self.game = Game.objects.create(
            title="Test Game",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        self.game_version = GameVersion.objects.create(
            game=self.game,
            version_number="1.0",
            release_date=timezone.now().date(),
            file_size_mb=1000
        )
        
        self.library = Library.objects.create(user=self.user)
        self.library_item = LibraryItem.objects.create(
            library=self.library,
            game=self.game
        )
    
    def test_download_history_creation(self):
        """Testa se um registro de download é criado corretamente"""
        download = DownloadHistory.objects.create(
            library_item=self.library_item,
            game_version=self.game_version,
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0"
        )
        
        self.assertEqual(download.library_item, self.library_item)
        self.assertEqual(download.game_version, self.game_version)
        self.assertEqual(download.ip_address, "127.0.0.1")
        self.assertEqual(download.user_agent, "Mozilla/5.0")
        self.assertIsNotNone(download.downloaded_at)

class WishlistModelTest(TestCase):
    """Testes para o modelo Wishlist"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.developer = Developer.objects.create(
            name="Test Developer",
            website="https://testdev.com"
        )
        
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            website="https://testpub.com"
        )
        
        self.game = Game.objects.create(
            title="Test Game",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        self.wishlist = Wishlist.objects.create(user=self.user)
    
    def test_wishlist_creation(self):
        """Testa se uma lista de desejos é criada corretamente"""
        self.assertEqual(self.wishlist.user, self.user)
        self.assertEqual(str(self.wishlist), f"Lista de desejos de {self.user.username}")
        self.assertEqual(self.wishlist.total_items(), 0)
    
    def test_wishlist_item_creation(self):
        """Testa a adição de itens à lista de desejos"""
        wishlist_item = WishlistItem.objects.create(
            wishlist=self.wishlist,
            game=self.game,
            priority=3
        )
        
        self.assertEqual(self.wishlist.total_items(), 1)
        self.assertEqual(wishlist_item.priority, 3)
        self.assertEqual(str(wishlist_item), f"{self.game.title} - Lista de desejos de {self.user.username}")

class CouponModelTest(TestCase):
    """Testes para o modelo Coupon"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Cupom válido por 30 dias
        valid_to = timezone.now() + datetime.timedelta(days=30)
        
        self.coupon = Coupon.objects.create(
            code="TESTCODE",
            description="Cupom de teste",
            discount_percent=20,
            valid_to=valid_to,
            max_uses=100
        )
    
    def test_coupon_creation(self):
        """Testa se um cupom é criado corretamente"""
        self.assertEqual(self.coupon.code, "TESTCODE")
        self.assertEqual(self.coupon.description, "Cupom de teste")
        self.assertEqual(self.coupon.discount_percent, 20)
        self.assertEqual(self.coupon.current_uses, 0)
        self.assertTrue(self.coupon.is_active)
        self.assertTrue(self.coupon.is_valid())
    
    def test_coupon_validity(self):
        """Testa a validade de um cupom"""
        # Cupom expirado
        expired_coupon = Coupon.objects.create(
            code="EXPIRED",
            discount_percent=10,
            valid_to=timezone.now() - datetime.timedelta(days=1)
        )
        self.assertFalse(expired_coupon.is_valid())
        
        # Cupom inativo
        inactive_coupon = Coupon.objects.create(
            code="INACTIVE",
            discount_percent=10,
            valid_to=timezone.now() + datetime.timedelta(days=30),
            is_active=False
        )
        self.assertFalse(inactive_coupon.is_valid())
        
        # Cupom com limite de usos atingido
        max_uses_coupon = Coupon.objects.create(
            code="MAXUSES",
            discount_percent=10,
            valid_to=timezone.now() + datetime.timedelta(days=30),
            max_uses=5,
            current_uses=5
        )
        self.assertFalse(max_uses_coupon.is_valid())
