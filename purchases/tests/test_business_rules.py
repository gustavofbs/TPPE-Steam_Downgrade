from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

from purchases.models import (
    Cart, CartItem, Order, OrderItem, 
    Library, LibraryItem, DownloadHistory,
    Wishlist, WishlistItem, Coupon
)
from games.models import Game, GameVersion, Developer, Publisher, Genre
image_mock = SimpleUploadedFile(name='cover.jpg', content=b'file_content', content_type='image/jpeg')

User = get_user_model()

class CartBusinessRulesTest(TestCase):
    """Testes para regras de negócio do carrinho"""
    
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
    
    def test_cart_quantity_validation(self):
        """Testa validações de quantidade no carrinho"""
        # Quantidade zero não deve ser permitida
        cart_item = CartItem(
            cart=self.cart,
            game=self.game,
            quantity=0
        )
        
        with self.assertRaises(ValidationError):
            cart_item.full_clean()
        
        # Quantidade negativa não deve ser permitida
        cart_item.quantity = -1
        
        with self.assertRaises(ValidationError):
            cart_item.full_clean()
        
        # Quantidade válida deve ser aceita
        cart_item.quantity = 1
        try:
            cart_item.full_clean()
            cart_item.save()
        except ValidationError:
            self.fail("CartItem with valid quantity should be valid")
    
    def test_cart_total_calculation(self):
        """Testa cálculos de total do carrinho com diferentes cenários"""
        # Adicionar um jogo sem desconto
        CartItem.objects.create(
            cart=self.cart,
            game=self.game,
            quantity=2
        )
        
        # Verificar total (29.99 * 2)
        self.assertEqual(self.cart.total_price(), Decimal('59.98'))
        
        # Criar um jogo com desconto
        game_with_discount = Game.objects.create(
            title="Discounted Game",
            slug=f"discounted-game-{self.game.id + 1}",  # ou com uuid
            base_price=Decimal('49.99'),
            discount_percent=50,
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date(),
            cover_image=image_mock,
        )

        
        # Adicionar o jogo com desconto ao carrinho
        CartItem.objects.create(
            cart=self.cart,
            game=game_with_discount,
            quantity=1
        )
        
        # Verificar total (29.99 * 2) + (49.99 * 0.5)
        expected_total = Decimal('59.98') + Decimal('25.00')
        self.assertEqual(self.cart.total_price(), expected_total)

class OrderBusinessRulesTest(TestCase):
    """Testes para regras de negócio de pedidos"""
    
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
    
    def test_order_amount_validation(self):
        """Testa validações de valor do pedido"""
        # Valor negativo não deve ser permitido
        order = Order(
            user=self.user,
            status='pending',
            total_amount=Decimal('-10.00'),
            payment_method='credit_card',
            payment_id='test_payment_123'
        )
        
        with self.assertRaises(ValidationError):
            order.full_clean()
        
        # Valor zero deve ser permitido (pedidos gratuitos)
        order.total_amount = Decimal('0.00')
        try:
            order.full_clean()
            order.save()
        except ValidationError:
            self.fail("Order with zero amount should be valid (free order)")
    
    def test_order_status_validation(self):
        """Testa validações de status do pedido"""
        # Status inválido não deve ser permitido
        order = Order(
            user=self.user,
            status='invalid_status',
            total_amount=Decimal('29.99'),
            payment_method='credit_card',
            payment_id='test_payment_123'
        )
        
        with self.assertRaises(ValidationError):
            order.full_clean()
        
        # Status válido deve ser aceito
        valid_statuses = ['pending', 'processing', 'completed', 'cancelled', 'refunded']
        
        for status in valid_statuses:
            order.status = status
            try:
                order.full_clean()
            except ValidationError:
                self.fail(f"Order with status '{status}' should be valid")
    
    def test_order_item_price_validation(self):
        """Testa validações de preço de item de pedido"""
        # Criar um pedido
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('29.99'),
            payment_method='credit_card',
            payment_id='test_payment_123'
        )
        
        # Preço negativo não deve ser permitido
        order_item = OrderItem(
            order=order,
            game=self.game,
            quantity=1,
            price=Decimal('-10.00'),
            discount=Decimal('0.00')
        )
        
        with self.assertRaises(ValidationError):
            order_item.full_clean()
        
        # Preço zero deve ser permitido (itens gratuitos)
        order_item.price = Decimal('0.00')
        try:
            order_item.full_clean()
            order_item.save()
        except ValidationError:
            self.fail("OrderItem with zero price should be valid (free item)")
        
        # Desconto maior que o preço não deve ser permitido
        order_item = OrderItem(
            order=order,
            game=self.game,
            quantity=1,
            price=Decimal('10.00'),
            discount=Decimal('15.00')
        )
        
        with self.assertRaises(ValidationError):
            order_item.full_clean()

class CouponBusinessRulesTest(TestCase):
    """Testes para regras de negócio de cupons"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.valid_to = timezone.now() + datetime.timedelta(days=30)
    
    def test_coupon_discount_validation(self):
        """Testa validações de desconto do cupom"""
        # Desconto zero não deve ser permitido
        coupon = Coupon(
            code="ZERO",
            discount_percent=0,
            valid_to=self.valid_to
        )
        
        with self.assertRaises(ValidationError):
            coupon.full_clean()
        
        # Desconto negativo não deve ser permitido
        coupon.discount_percent = -10
        
        with self.assertRaises(ValidationError):
            coupon.full_clean()
        
        # Desconto maior que 100% não deve ser permitido
        coupon.discount_percent = 101
        
        with self.assertRaises(ValidationError):
            coupon.full_clean()
        
        # Desconto válido deve ser aceito
        coupon.discount_percent = 50
        try:
            coupon.full_clean()
            coupon.save()
        except ValidationError:
            self.fail("Coupon with valid discount should be valid")
    
    def test_coupon_date_validation(self):
        """Testa validações de data do cupom"""
        # Data de validade no passado não deve ser permitida
        past_date = timezone.now() - datetime.timedelta(days=1)
        
        coupon = Coupon(
            code="PAST",
            discount_percent=20,
            valid_to=past_date
        )
        
        # O cupom pode ser criado, mas não será válido
        coupon.save()
        self.assertFalse(coupon.is_valid())
        
        # Data de validade no futuro deve ser aceita
        future_date = timezone.now() + datetime.timedelta(days=30)
        
        coupon.valid_to = future_date
        coupon.save()
        self.assertTrue(coupon.is_valid())
    
    def test_coupon_usage_limit(self):
        """Testa limites de uso do cupom"""
        # Cupom com limite de usos
        coupon = Coupon.objects.create(
            code="LIMITED",
            discount_percent=20,
            valid_to=self.valid_to,
            max_uses=5,
            current_uses=0
        )
        
        # Cupom deve ser válido inicialmente
        self.assertTrue(coupon.is_valid())
        
        # Simular usos do cupom
        for i in range(5):
            coupon.current_uses += 1
            coupon.save()
            if i < 4:
                self.assertTrue(coupon.is_valid())
            else:
                self.assertFalse(coupon.is_valid())
        
        # Cupom sem limite de usos (max_uses=0)
        unlimited_coupon = Coupon.objects.create(
            code="UNLIMITED",
            discount_percent=20,
            valid_to=self.valid_to,
            max_uses=0,
            current_uses=100
        )
        
        # Cupom deve ser válido independentemente do número de usos
        self.assertTrue(unlimited_coupon.is_valid())

class LibraryBusinessRulesTest(TestCase):
    """Testes para regras de negócio da biblioteca"""
    
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
        
        self.library = Library.objects.create(user=self.user)
    
    def test_library_item_playtime_formatting(self):
        """Testa formatação do tempo de jogo"""
        # Criar item na biblioteca
        library_item = LibraryItem.objects.create(
            library=self.library,
            game=self.game
        )
        
        # Testar diferentes tempos de jogo
        test_cases = [
            (0, "0 minutos"),
            (1, "1 minuto"),
            (30, "30 minutos"),
            (59, "59 minutos"),
            (60, "1 hora"),
            (61, "1 hora e 1 minuto"),
            (90, "1 hora e 30 minutos"),
            (120, "2 horas"),
            (121, "2 horas e 1 minuto"),
            (150, "2 horas e 30 minutos"),
            (3600, "60 horas")
        ]
        
        for minutes, expected_format in test_cases:
            library_item.playtime = minutes
            library_item.save()
            self.assertEqual(library_item.formatted_playtime(), expected_format)
    
    def test_library_item_last_played_update(self):
        """Testa atualização da data de último jogo"""
        # Criar item na biblioteca sem data de último jogo
        library_item = LibraryItem.objects.create(
            library=self.library,
            game=self.game
        )
        
        self.assertIsNone(library_item.last_played)
        
        # Simular jogo sendo jogado
        now = timezone.now()
        library_item.last_played = now
        library_item.save()
        
        self.assertEqual(library_item.last_played, now)

class WishlistBusinessRulesTest(TestCase):
    """Testes para regras de negócio da lista de desejos"""
    
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
    
    def test_wishlist_item_priority_validation(self):
        """Testa validações de prioridade de item na lista de desejos"""
        # Prioridade negativa não deve ser permitida
        wishlist_item = WishlistItem(
            wishlist=self.wishlist,
            game=self.game,
            priority=-1
        )
        
        with self.assertRaises(ValidationError):
            wishlist_item.full_clean()
        
        # Prioridade maior que 5 não deve ser permitida
        wishlist_item.priority = 6
        
        with self.assertRaises(ValidationError):
            wishlist_item.full_clean()
        
        # Prioridades válidas devem ser aceitas
        for priority in range(6):  # 0 a 5
            wishlist_item.priority = priority
            try:
                wishlist_item.full_clean()
            except ValidationError:
                self.fail(f"WishlistItem with priority {priority} should be valid")
