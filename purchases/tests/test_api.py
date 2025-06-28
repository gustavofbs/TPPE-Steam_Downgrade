from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
import datetime

from games.models import Game, Genre, Developer, Publisher
from purchases.models import Cart, CartItem, Order, OrderItem, Library, LibraryItem, Wishlist, WishlistItem, Coupon


class PurchasesAPITest(TestCase):
    """Testes para a API de compras"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuários para os testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )
        
        # Criar gênero, desenvolvedor e publicadora para os jogos
        self.genre = Genre.objects.create(
            name='Action',
            slug='action',
            description='Action games'
        )
        
        self.developer = Developer.objects.create(
            name='Test Developer',
            description='A test developer'
        )
        
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='A test publisher'
        )
        
        # Criar jogos para os testes
        self.game1 = Game.objects.create(
            title='Test Game 1',
            slug='test-game-1',
            description='A test game 1',
            short_description='Test game 1',
            release_date=datetime.date(2023, 1, 1),
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher
        )
        self.game1.genres.add(self.genre)
        
        self.game2 = Game.objects.create(
            title='Test Game 2',
            slug='test-game-2',
            description='A test game 2',
            short_description='Test game 2',
            release_date=datetime.date(2023, 2, 1),
            base_price=Decimal('39.99'),
            discount_percent=10,
            developer=self.developer,
            publisher=self.publisher
        )
        self.game2.genres.add(self.genre)
        
        # Criar carrinho e itens para o usuário de teste
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            game=self.game1,
            quantity=1
        )
        
        # Criar cupom para os testes
        self.coupon = Coupon.objects.create(
            code='TESTCODE',
            description='Test coupon',
            discount_percent=10,
            valid_from=timezone.now() - datetime.timedelta(days=1),
            valid_to=timezone.now() + datetime.timedelta(days=1),
            is_active=True
        )
        
        # Configurar cliente API
        self.client = APIClient()
        
        # URLs para os testes
        self.cart_url = reverse('cart-list')
        self.my_cart_url = reverse('cart-my-cart')
        self.add_item_url = reverse('cart-add-item')
        self.remove_item_url = reverse('cart-remove-item')
        self.clear_cart_url = reverse('cart-clear')
        
        self.orders_url = reverse('order-list')
        self.order_detail_url = lambda pk: reverse('order-detail', kwargs={'pk': pk})
        
        self.library_url = reverse('library-list')
        self.my_library_url = reverse('library-my-library')
        
        self.wishlist_url = reverse('wishlist-list')
        self.my_wishlist_url = reverse('wishlist-my-wishlist')
        self.add_wishlist_item_url = reverse('wishlist-add-item')
        self.remove_wishlist_item_url = reverse('wishlist-remove-item')
        self.clear_wishlist_url = reverse('wishlist-clear')
        
        self.coupons_url = reverse('coupon-list')
        self.validate_coupon_url = reverse('coupon-validate')
    
    def test_cart_unauthenticated(self):
        """Testa que usuários não autenticados não podem acessar o carrinho"""
        response = self.client.get(self.my_cart_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_cart_authenticated(self):
        """Testa que usuários autenticados podem acessar seu carrinho"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.my_cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['game'], self.game1.id)
    
    def test_add_item_to_cart(self):
        """Testa adicionar um item ao carrinho"""
        self.client.force_authenticate(user=self.user)
        data = {
            'game': self.game2.id,
            'quantity': 2
        }
        response = self.client.post(self.add_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 2)
        
        # Verificar se o item foi adicionado corretamente
        cart_items = CartItem.objects.filter(cart=self.cart)
        self.assertEqual(cart_items.count(), 2)
        self.assertTrue(cart_items.filter(game=self.game2, quantity=2).exists())
    
    def test_update_cart_item_quantity(self):
        """Testa atualizar a quantidade de um item no carrinho"""
        self.client.force_authenticate(user=self.user)
        data = {
            'game': self.game1.id,
            'quantity': 3
        }
        response = self.client.post(self.add_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a quantidade foi atualizada
        cart_item = CartItem.objects.get(cart=self.cart, game=self.game1)
        self.assertEqual(cart_item.quantity, 3)
    
    def test_remove_item_from_cart(self):
        """Testa remover um item do carrinho"""
        self.client.force_authenticate(user=self.user)
        data = {
            'game': self.game1.id
        }
        response = self.client.post(self.remove_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o item foi removido
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 0)
    
    def test_clear_cart(self):
        """Testa limpar o carrinho"""
        # Adicionar mais um item ao carrinho
        CartItem.objects.create(
            cart=self.cart,
            game=self.game2,
            quantity=1
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.clear_cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o carrinho está vazio
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 0)
    
    def test_create_order(self):
        """Testa criar um pedido a partir do carrinho"""
        self.client.force_authenticate(user=self.user)
        data = {
            'payment_method': 'credit_card',
            'notes': 'Test order'
        }
        response = self.client.post(self.orders_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o pedido foi criado corretamente
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.payment_method, 'credit_card')
        self.assertEqual(order.notes, 'Test order')
        
        # Verificar se o item do pedido foi criado
        order_item = OrderItem.objects.filter(order=order).first()
        self.assertIsNotNone(order_item)
        self.assertEqual(order_item.game, self.game1)
        self.assertEqual(order_item.quantity, 1)
        
        # Verificar se o carrinho foi esvaziado
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 0)
    
    def test_create_order_with_coupon(self):
        """Testa criar um pedido com cupom de desconto"""
        self.client.force_authenticate(user=self.user)
        data = {
            'coupon_code': 'TESTCODE',
            'payment_method': 'credit_card'
        }
        response = self.client.post(self.orders_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o cupom foi aplicado corretamente
        order = Order.objects.filter(user=self.user).first()
        self.assertEqual(order.coupon_code, 'TESTCODE')
        self.assertEqual(order.coupon_discount, Decimal('3.00'))  # 10% de 29.99
        
        # Verificar se o uso do cupom foi incrementado
        self.coupon.refresh_from_db()
        self.assertEqual(self.coupon.current_uses, 1)
    
    def test_list_orders(self):
        """Testa listar os pedidos do usuário"""
        # Criar um pedido para o teste
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('29.99')
        )
        OrderItem.objects.create(
            order=order,
            game=self.game1,
            quantity=1,
            price=Decimal('29.99'),
            discount=Decimal('0.00')
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], order.id)
    
    def test_update_order_status(self):
        """Testa atualizar o status de um pedido"""
        # Criar um pedido para o teste
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('29.99')
        )

        OrderItem.objects.create(
            order=order,
            game=self.game1,
            quantity=1,
            price=self.game1.current_price(),
            discount=self.game1.discount_amount()
        )
        
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'status': 'completed'
        }
        response = self.client.put(self.order_detail_url(order.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o status foi atualizado
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')
        
        # Verificar se o jogo foi adicionado à biblioteca
        library = Library.objects.get(user=self.user)
        self.assertTrue(LibraryItem.objects.filter(library=library, game=self.game1).exists())
    
    def test_library_access(self):
        """Testa acesso à biblioteca de jogos"""
        # Criar biblioteca e item para o teste
        library = Library.objects.create(user=self.user)
        library_item = LibraryItem.objects.create(
            library=library,
            game=self.game1
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.my_library_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['game'], self.game1.id)
    
    def test_wishlist_operations(self):
        """Testa operações na lista de desejos"""
        self.client.force_authenticate(user=self.user)
        
        # Adicionar item à lista de desejos
        data = {
            'game': self.game2.id,
            'priority': 3
        }
        response = self.client.post(self.add_wishlist_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o item foi adicionado
        wishlist = Wishlist.objects.get(user=self.user)
        self.assertEqual(WishlistItem.objects.filter(wishlist=wishlist).count(), 1)
        wishlist_item = WishlistItem.objects.get(wishlist=wishlist, game=self.game2)
        self.assertEqual(wishlist_item.priority, 3)
        
        # Atualizar prioridade
        data = {
            'game': self.game2.id,
            'priority': 5
        }
        response = self.client.post(self.add_wishlist_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a prioridade foi atualizada
        wishlist_item.refresh_from_db()
        self.assertEqual(wishlist_item.priority, 5)
        
        # Remover item da lista de desejos
        data = {
            'game': self.game2.id
        }
        response = self.client.post(self.remove_wishlist_item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o item foi removido
        self.assertEqual(WishlistItem.objects.filter(wishlist=wishlist).count(), 0)
    
    def test_coupon_validation(self):
        """Testa validação de cupom"""
        self.client.force_authenticate(user=self.user)
        
        # Testar cupom válido
        data = {
            'code': 'TESTCODE'
        }
        response = self.client.post(self.validate_coupon_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_valid'])
        
        # Testar cupom inválido
        data = {
            'code': 'INVALIDCODE'
        }
        response = self.client.post(self.validate_coupon_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Testar cupom expirado
        expired_coupon = Coupon.objects.create(
            code='EXPIRED',
            description='Expired coupon',
            discount_percent=10,
            valid_from=timezone.now() - datetime.timedelta(days=10),
            valid_to=timezone.now() - datetime.timedelta(days=1),
            is_active=True
        )
        
        data = {
            'code': 'EXPIRED'
        }
        response = self.client.post(self.validate_coupon_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_valid'])
    
    def test_coupon_management_staff_only(self):
        """Testa que apenas staff pode gerenciar cupons"""
        # Tentar listar cupons como usuário normal
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.coupons_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Listar cupons como admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.coupons_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Criar novo cupom como admin
        data = {
            'code': 'NEWCODE',
            'description': 'New coupon',
            'discount_percent': 20,
            'valid_from': timezone.now().isoformat(),
            'valid_to': (timezone.now() + datetime.timedelta(days=30)).isoformat(),
            'is_active': True
        }
        response = self.client.post(self.coupons_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o cupom foi criado
        self.assertTrue(Coupon.objects.filter(code='NEWCODE').exists())
