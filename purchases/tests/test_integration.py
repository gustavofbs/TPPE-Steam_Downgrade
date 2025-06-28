from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

from purchases.models import (
    Cart, CartItem, Order, OrderItem, 
    Library, LibraryItem, DownloadHistory,
    Wishlist, WishlistItem, Coupon
)
from games.models import Game, GameVersion, Developer, Publisher, Genre

User = get_user_model()

class CartToOrderIntegrationTest(TestCase):
    """Testes de integração entre carrinho e pedido"""
    
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
        
        # Criar dois jogos para testar
        self.game1 = Game.objects.create(
            title="Test Game 1",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        self.game2 = Game.objects.create(
            title="Test Game 2",
            base_price=Decimal('19.99'),
            discount_percent=25,  # 25% de desconto
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        # Criar versões para os jogos
        self.game1_version = GameVersion.objects.create(
            game=self.game1,
            version_number="1.0",
            release_date=timezone.now().date(),
            file_size_mb=1000
        )
        
        self.game2_version = GameVersion.objects.create(
            game=self.game2,
            version_number="1.0",
            release_date=timezone.now().date(),
            file_size_mb=800
        )
        
        # Criar carrinho e adicionar itens
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item1 = CartItem.objects.create(
            cart=self.cart,
            game=self.game1,
            quantity=1
        )
        self.cart_item2 = CartItem.objects.create(
            cart=self.cart,
            game=self.game2,
            quantity=2
        )
    
    def test_cart_to_order_conversion(self):
        """Testa a conversão de um carrinho para um pedido"""
        # Calcular o total esperado
        # game1: 29.99 * 1 = 29.99
        # game2: (19.99 * 0.75) * 2 = 29.99
        expected_total = Decimal('29.99') + (Decimal('19.99') * Decimal('0.75') * 2)
        
        # Criar um pedido a partir do carrinho
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=expected_total,
            payment_method='credit_card',
            payment_id='test_payment_123'
        )
        
        # Adicionar itens do carrinho ao pedido
        for cart_item in self.cart.items.all():
            OrderItem.objects.create(
                order=order,
                game=cart_item.game,
                game_version=cart_item.game.versions.first(),
                quantity=cart_item.quantity,
                price=cart_item.game.discount_price,
                discount=Decimal('0.00')
            )
        
        # Verificar se o pedido foi criado corretamente
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.total_amount, expected_total)
        
        # Verificar se os itens do pedido correspondem aos itens do carrinho
        order_items = order.items.all()
        self.assertEqual(order_items[0].game, self.game1)
        self.assertEqual(order_items[0].quantity, 1)
        self.assertEqual(order_items[0].price, Decimal('29.99'))
        
        self.assertEqual(order_items[1].game, self.game2)
        self.assertEqual(order_items[1].quantity, 2)
        self.assertEqual(order_items[1].price, Decimal('14.99'))  # 19.99 * 0.75

class OrderToLibraryIntegrationTest(TestCase):
    """Testes de integração entre pedido e biblioteca"""
    
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
        
        # Criar dois jogos para testar
        self.game1 = Game.objects.create(
            title="Test Game 1",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        self.game2 = Game.objects.create(
            title="Test Game 2",
            base_price=Decimal('19.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        # Criar versões para os jogos
        self.game1_version = GameVersion.objects.create(
            game=self.game1,
            version_number="1.0",
            release_date=timezone.now().date(),
            file_size_mb=1000
        )
        
        self.game2_version = GameVersion.objects.create(
            game=self.game2,
            version_number="1.0",
            release_date=timezone.now().date(),
            file_size_mb=800
        )
        
        # Criar um pedido com os jogos
        self.order = Order.objects.create(
            user=self.user,
            status='completed',
            total_amount=Decimal('49.98'),
            payment_method='credit_card',
            payment_id='test_payment_123'
        )
        
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            game=self.game1,
            game_version=self.game1_version,
            quantity=1,
            price=Decimal('29.99'),
            discount=Decimal('0.00')
        )
        
        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            game=self.game2,
            game_version=self.game2_version,
            quantity=1,
            price=Decimal('19.99'),
            discount=Decimal('0.00')
        )
        
        # Criar biblioteca para o usuário
        self.library = Library.objects.create(user=self.user)
    
    def test_order_to_library_conversion(self):
        """Testa a adição de jogos à biblioteca após a conclusão de um pedido"""
        # Adicionar jogos do pedido à biblioteca
        for order_item in self.order.items.all():
            LibraryItem.objects.create(
                library=self.library,
                game=order_item.game,
                order=self.order
            )
        
        # Verificar se os jogos foram adicionados à biblioteca
        self.assertEqual(self.library.items.count(), 2)
        
        # Verificar se os jogos na biblioteca correspondem aos jogos do pedido
        library_games = [item.game for item in self.library.items.all()]
        self.assertIn(self.game1, library_games)
        self.assertIn(self.game2, library_games)
        
        # Verificar se a referência ao pedido está correta
        for library_item in self.library.items.all():
            self.assertEqual(library_item.order, self.order)

class LibraryToDownloadIntegrationTest(TestCase):
    """Testes de integração entre biblioteca e histórico de downloads"""
    
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
        
        # Criar jogo e versões
        self.game = Game.objects.create(
            title="Test Game",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        self.game_version1 = GameVersion.objects.create(
            game=self.game,
            version_number="1.0",
            release_date=timezone.now().date() - datetime.timedelta(days=30),
            file_size_mb=1000
        )
        
        self.game_version2 = GameVersion.objects.create(
            game=self.game,
            version_number="2.0",
            release_date=timezone.now().date(),
            file_size_mb=1200
        )
        
        # Criar biblioteca e item
        self.library = Library.objects.create(user=self.user)
        self.library_item = LibraryItem.objects.create(
            library=self.library,
            game=self.game
        )
    
    def test_library_download_tracking(self):
        """Testa o registro de downloads de diferentes versões de um jogo"""
        # Registrar download da versão 1.0
        download1 = DownloadHistory.objects.create(
            library_item=self.library_item,
            game_version=self.game_version1,
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0"
        )
        
        # Registrar download da versão 2.0
        download2 = DownloadHistory.objects.create(
            library_item=self.library_item,
            game_version=self.game_version2,
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0"
        )
        
        # Verificar se os downloads foram registrados corretamente
        downloads = self.library_item.downloads.all()
        self.assertEqual(downloads.count(), 2)
        
        # Verificar se as versões estão corretas
        downloaded_versions = [download.game_version for download in downloads]
        self.assertIn(self.game_version1, downloaded_versions)
        self.assertIn(self.game_version2, downloaded_versions)

class CouponOrderIntegrationTest(TestCase):
    """Testes de integração entre cupons e pedidos"""
    
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
        
        # Criar jogo
        self.game = Game.objects.create(
            title="Test Game",
            base_price=Decimal('100.00'),  # Preço base de 100 para facilitar cálculos
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        # Criar cupom de 20% de desconto
        self.coupon = Coupon.objects.create(
            code="SAVE20",
            description="20% de desconto",
            discount_percent=20,
            valid_to=timezone.now() + datetime.timedelta(days=30),
            max_uses=100
        )
        
        # Criar carrinho e adicionar item
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            game=self.game,
            quantity=1
        )
    
    def test_coupon_application_to_order(self):
        """Testa a aplicação de um cupom a um pedido"""
        # Verificar se o cupom é válido
        self.assertTrue(self.coupon.is_valid())
        
        # Calcular o desconto do cupom (20% de 100.00)
        coupon_discount = self.coupon.calculate_discount(self.game.base_price)
        expected_total = self.game.base_price - coupon_discount
        
        # Criar um pedido com o cupom aplicado
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=expected_total,
            payment_method='credit_card',
            payment_id='test_payment_123',
            coupon_code=self.coupon.code,
            coupon_discount=coupon_discount
        )
        
        # Adicionar item ao pedido
        OrderItem.objects.create(
            order=order,
            game=self.game,
            quantity=1,
            price=self.game.base_price,
            discount=coupon_discount
        )
        
        # Incrementar o uso do cupom
        self.coupon.current_uses += 1
        self.coupon.save()
        
        # Verificar se o pedido foi criado corretamente com o desconto
        self.assertEqual(order.total_amount, Decimal('80.00'))  # 100 - 20% = 80
        self.assertEqual(order.coupon_code, "SAVE20")
        self.assertEqual(order.coupon_discount, Decimal('20.00'))
        
        # Verificar se o uso do cupom foi registrado
        updated_coupon = Coupon.objects.get(code="SAVE20")
        self.assertEqual(updated_coupon.current_uses, 1)
        
        # Verificar se o cupom ainda é válido após o uso
        self.assertTrue(updated_coupon.is_valid())
        
        # Testar limite de usos
        updated_coupon.max_uses = 1
        updated_coupon.save()
        self.assertFalse(updated_coupon.is_valid())  # Não deve ser mais válido
