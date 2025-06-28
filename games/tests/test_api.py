from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
import datetime

from games.models import Game, Genre, Developer, Publisher, GameVersion, GameImage, SystemRequirement
image_mock = SimpleUploadedFile(name='cover.jpg', content=b'file_content', content_type='image/jpeg')

class GamesAPITest(TestCase):
    """Testes para a API de jogos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar um cliente da API
        self.client = APIClient()
        
        # Criar usuários para os testes
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )
        
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Criar gêneros para os testes
        self.genre1 = Genre.objects.create(name='Action', description='Action games')
        self.genre2 = Genre.objects.create(name='Adventure', description='Adventure games')
        
        # Criar desenvolvedores para os testes
        self.developer = Developer.objects.create(
            name='Test Developer',
            description='A test developer',
            website='https://testdeveloper.com',
            founded_date='2000-01-01'
        )
        
        # Criar publicadoras para os testes
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='A test publisher',
            website='https://testpublisher.com',
            founded_date='2000-01-01'
        )
        
        # Criar um jogo para os testes
        self.game = Game.objects.create(
            title='Test Game',
            slug='test-game',
            description='A test game description',
            short_description='A short description',
            release_date='2023-01-01',
            base_price=Decimal('59.99'),
            discount_percent=10,
            cover_image='games/covers/test.jpg',
            developer=self.developer,
            publisher=self.publisher
        )
        
        # Adicionar gêneros ao jogo
        self.game.genres.add(self.genre1, self.genre2)
        
        # Criar uma versão do jogo para os testes
        self.game_version = GameVersion.objects.create(
            game=self.game,
            version_number='1.0',
            release_date='2023-01-01',
            description='Initial version',
            is_available=True,
            file_size_mb=1000
        )
        
        # Criar requisitos de sistema para os testes
        self.system_requirement = SystemRequirement.objects.create(
            game=self.game,
            requirement_type='minimum',
            os='Windows 10',
            processor='Intel Core i5',
            memory='8 GB RAM',
            graphics='NVIDIA GTX 1060',
            directx='DirectX 12',
            storage='50 GB'
        )
        
        # URLs para os testes
        self.games_list_url = reverse('game-list')
        self.game_detail_url = lambda slug: reverse('game-detail', kwargs={'slug': slug})
        self.game_versions_url = lambda slug: reverse('game-versions', kwargs={'slug': slug})
        self.game_images_url = lambda slug: reverse('game-images', kwargs={'slug': slug})
        self.game_requirements_url = lambda slug: reverse('game-requirements', kwargs={'slug': slug})
        self.game_featured_url = reverse('game-featured')
        self.game_on_sale_url = reverse('game-on-sale')
        
        self.genres_list_url = reverse('genre-list')
        self.genre_detail_url = lambda slug: reverse('genre-detail', kwargs={'slug': slug})
        
        self.developers_list_url = reverse('developer-list')
        self.developer_detail_url = lambda pk: reverse('developer-detail', kwargs={'pk': pk})
        
        self.publishers_list_url = reverse('publisher-list')
        self.publisher_detail_url = lambda pk: reverse('publisher-detail', kwargs={'pk': pk})
    
    def _get_valid_image_file(self):
        """Cria um arquivo de imagem válido para testes"""
        image = Image.new('RGB', (100, 100), color='blue')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        return SimpleUploadedFile('test_image.jpg', buffer.read(), content_type='image/jpeg')
    
    def test_list_games_unauthenticated(self):
        """Testa a listagem de jogos por um usuário não autenticado"""
        response = self.client.get(self.games_list_url)
        
        # Verificar a resposta (deve ser permitida para leitura)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_game_unauthenticated(self):
        """Testa a obtenção dos detalhes de um jogo por um usuário não autenticado"""
        response = self.client.get(self.game_detail_url(self.game.slug))
        
        # Verificar a resposta (deve ser permitida para leitura)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Game')
        self.assertEqual(response.data['slug'], 'test-game')
        self.assertEqual(response.data['description'], 'A test game description')
        self.assertEqual(response.data['developer']['name'], 'Test Developer')
        self.assertEqual(response.data['publisher']['name'], 'Test Publisher')
        self.assertEqual(len(response.data['genres']), 2)
    
    def test_create_game_unauthenticated(self):
        """Testa a criação de um jogo por um usuário não autenticado"""
        # Dados para o novo jogo
        data = {
            'title': 'New Game',
            'description': 'A new game description',
            'short_description': 'A short description',
            'release_date': '2023-02-01',
            'base_price': '49.99',
            'discount_percent': 0,
            'developer': self.developer.id,
            'publisher': self.publisher.id,
            'genres': [self.genre1.id]
        }
        
        # Fazer a requisição sem autenticação
        response = self.client.post(self.games_list_url, data)
        
        # Verificar a resposta (deve ser negada)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_game_authenticated(self):
        """Testa a criação de um jogo por um usuário autenticado"""
        # Autenticar como usuário admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Criar imagem para o jogo
        cover_image = self._get_valid_image_file()
        
        # Dados para o novo jogo
        data = {
            'title': 'New Game',
            'description': 'A new game description',
            'short_description': 'A short description',
            'release_date': '2023-02-01',
            'base_price': '49.99',
            'discount_percent': 0,
            'cover_image': cover_image,
            'developer': self.developer.id,
            'publisher': self.publisher.id,
            'genres': [self.genre1.id]
        }
        
        # Fazer a requisição
        response = self.client.post(
            self.games_list_url,
            data,
            format='multipart'
        )
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o jogo foi criado
        self.assertTrue(Game.objects.filter(title='New Game').exists())
        
        # Verificar os detalhes do jogo criado
        new_game = Game.objects.get(title='New Game')
        self.assertEqual(new_game.description, 'A new game description')
        self.assertEqual(new_game.base_price, Decimal('49.99'))
        self.assertEqual(new_game.developer, self.developer)
        self.assertEqual(new_game.publisher, self.publisher)
        self.assertEqual(list(new_game.genres.all()), [self.genre1])
    
    def test_delete_game_authenticated(self):
        """Testa a exclusão de um jogo por um usuário autenticado"""
        # Autenticar como usuário admin
        self.client.force_authenticate(user=self.admin_user)
        
        # Fazer a requisição
        response = self.client.delete(self.game_detail_url(self.game.slug))
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se o jogo foi excluído
        self.assertFalse(Game.objects.filter(id=self.game.id).exists())
    
    def test_game_versions_endpoint(self):
        """Testa o endpoint de versões de um jogo"""
        response = self.client.get(self.game_versions_url(self.game.slug))
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['version_number'], '1.0')
    
    def test_game_requirements_endpoint(self):
        """Testa o endpoint de requisitos de sistema de um jogo"""
        response = self.client.get(self.game_requirements_url(self.game.slug))
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['requirement_type'], 'minimum')
        self.assertEqual(response.data[0]['os'], 'Windows 10')
    
    def test_game_featured_endpoint(self):
        """Testa o endpoint de jogos em destaque"""
        # Marcar o jogo como destaque
        self.game.is_featured = True
        self.game.save()
        
        response = self.client.get(self.game_featured_url)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Game')
    
    def test_game_on_sale_endpoint(self):
        """Testa o endpoint de jogos em promoção"""
        response = self.client.get(self.game_on_sale_url)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Game')
        self.assertEqual(response.data['results'][0]['discount_percent'], 10)
    
    def test_list_genres(self):
        """Testa a listagem de gêneros"""
        response = self.client.get(self.genres_list_url)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_genre(self):
        """Testa a obtenção dos detalhes de um gênero"""
        response = self.client.get(self.genre_detail_url(self.genre1.slug))
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Action')
        self.assertEqual(response.data['description'], 'Action games')
    
    def test_list_developers(self):
        """Testa a listagem de desenvolvedores"""
        response = self.client.get(self.developers_list_url)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_developer(self):
        """Testa a obtenção dos detalhes de um desenvolvedor"""
        response = self.client.get(self.developer_detail_url(self.developer.id))
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Developer')
        self.assertEqual(response.data['description'], 'A test developer')
    
    def test_list_publishers(self):
        """Testa a listagem de publicadoras"""
        response = self.client.get(self.publishers_list_url)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_retrieve_publisher(self):
        """Testa a obtenção dos detalhes de uma publicadora"""
        response = self.client.get(self.publisher_detail_url(self.publisher.id))
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Publisher')
        self.assertEqual(response.data['description'], 'A test publisher')
