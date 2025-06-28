from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from decimal import Decimal

from games.models import Genre, Developer, Publisher, Game, GameVersion, GameImage, SystemRequirement

class GenreModelTest(TestCase):
    """Testes para o modelo Genre"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.genre = Genre.objects.create(
            name="Ação",
            description="Jogos de ação e aventura"
        )
    
    def test_genre_creation(self):
        """Testa se um gênero é criado corretamente"""
        self.assertEqual(self.genre.name, "Ação")
        self.assertEqual(self.genre.description, "Jogos de ação e aventura")
    
    def test_genre_str_representation(self):
        """Testa a representação string do modelo"""
        self.assertEqual(str(self.genre), "Ação")
    
    def test_genre_unique_name(self):
        """Testa se não é possível criar gêneros com o mesmo nome"""
        with self.assertRaises(IntegrityError):
            Genre.objects.create(
                name="Ação",
                description="Outro gênero de ação"
            )

class DeveloperModelTest(TestCase):
    """Testes para o modelo Developer"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.developer = Developer.objects.create(
            name="Valve Corporation",
            website="https://www.valvesoftware.com",
            description="Desenvolvedora do Steam e de jogos como Half-Life e Portal"
        )
    
    def test_developer_creation(self):
        """Testa se uma desenvolvedora é criada corretamente"""
        self.assertEqual(self.developer.name, "Valve Corporation")
        self.assertEqual(self.developer.website, "https://www.valvesoftware.com")
        self.assertEqual(
            self.developer.description, 
            "Desenvolvedora do Steam e de jogos como Half-Life e Portal"
        )
        self.assertTrue(self.developer.is_active)
    
    def test_developer_str_representation(self):
        """Testa a representação string do modelo"""
        self.assertEqual(str(self.developer), "Valve Corporation")
    
    def test_developer_unique_name(self):
        """Testa se não é possível criar desenvolvedoras com o mesmo nome"""
        with self.assertRaises(IntegrityError):
            Developer.objects.create(
                name="Valve Corporation",
                website="https://www.valve.com"
            )

class PublisherModelTest(TestCase):
    """Testes para o modelo Publisher"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.publisher = Publisher.objects.create(
            name="Electronic Arts",
            website="https://www.ea.com",
            description="Publicadora de jogos como FIFA e Battlefield"
        )
    
    def test_publisher_creation(self):
        """Testa se uma publicadora é criada corretamente"""
        self.assertEqual(self.publisher.name, "Electronic Arts")
        self.assertEqual(self.publisher.website, "https://www.ea.com")
        self.assertEqual(
            self.publisher.description, 
            "Publicadora de jogos como FIFA e Battlefield"
        )
        self.assertTrue(self.publisher.is_active)
    
    def test_publisher_str_representation(self):
        """Testa a representação string do modelo"""
        self.assertEqual(str(self.publisher), "Electronic Arts")
    
    def test_publisher_unique_name(self):
        """Testa se não é possível criar publicadoras com o mesmo nome"""
        with self.assertRaises(IntegrityError):
            Publisher.objects.create(
                name="Electronic Arts",
                website="https://www.electronicarts.com"
            )

class GameModelTest(TestCase):
    """Testes para o modelo Game"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Cria objetos necessários para o teste
        self.genre = Genre.objects.create(name="FPS", description="First Person Shooter")
        self.developer = Developer.objects.create(
            name="Valve", 
            website="https://www.valvesoftware.com"
        )
        self.publisher = Publisher.objects.create(
            name="Valve", 
            website="https://www.valvesoftware.com"
        )
        
        # Cria o jogo para teste
        self.game = Game.objects.create(
            title="Half-Life 2",
            description="Um clássico FPS com elementos de física",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.datetime(2004, 11, 16).date()
        )
        
        # Adiciona gênero ao jogo
        self.game.genres.add(self.genre)
    
    def test_game_creation(self):
        """Testa se um jogo é criado corretamente"""
        self.assertEqual(self.game.title, "Half-Life 2")
        self.assertEqual(self.game.base_price, Decimal('29.99'))
        self.assertEqual(self.game.developer.name, "Valve")
        self.assertEqual(self.game.publisher.name, "Valve")
        self.assertEqual(self.game.release_date, timezone.datetime(2004, 11, 16).date())
        self.assertTrue(self.game.is_active)
    
    def test_game_genres(self):
        """Testa se os gêneros são associados corretamente ao jogo"""
        self.assertEqual(self.game.genres.count(), 1)
        self.assertEqual(self.game.genres.first().name, "FPS")
    
    def test_game_str_representation(self):
        """Testa a representação string do modelo"""
        self.assertEqual(str(self.game), "Half-Life 2")
    
    def test_game_discount_price(self):
        """Testa o cálculo do preço com desconto"""
        # Sem desconto
        self.assertEqual(self.game.discount_price, Decimal('29.99'))
        
        # Com desconto de 50%
        self.game.discount_percent = 50
        self.game.save()
        self.assertEqual(self.game.discount_price, Decimal('15.00'))
    
    def test_game_is_on_sale(self):
        """Testa se o jogo está em promoção"""
        # Inicialmente sem desconto
        self.assertFalse(self.game.is_on_sale)
        
        # Com desconto
        self.game.discount_percent = 20
        self.game.save()
        self.assertTrue(self.game.is_on_sale)

class GameVersionModelTest(TestCase):
    """Testes para o modelo GameVersion"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Cria objetos necessários para o teste
        self.developer = Developer.objects.create(name="Valve")
        self.publisher = Publisher.objects.create(name="Valve")
        
        # Cria o jogo para teste
        self.game = Game.objects.create(
            title="Counter-Strike",
            base_price=Decimal('9.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.datetime(2000, 11, 1).date(),
        )
        
        # Cria versão do jogo
        self.version = GameVersion.objects.create(
            game=self.game,
            version_number="1.6",
            release_date=timezone.datetime(2003, 9, 9).date(),
            description="Versão clássica do Counter-Strike",
            download_url="https://example.com/cs16.zip",
            file_size_mb=500
        )
    
    def test_version_creation(self):
        """Testa se uma versão do jogo é criada corretamente"""
        self.assertEqual(self.version.game.title, "Counter-Strike")
        self.assertEqual(self.version.version_number, "1.6")
        self.assertEqual(self.version.release_date, timezone.datetime(2003, 9, 9).date())
        self.assertEqual(self.version.file_size_mb, 500)
    
    def test_version_str_representation(self):
        """Testa a representação string do modelo"""
        self.assertEqual(str(self.version), "Counter-Strike - 1.6")
    
    def test_version_formatted_file_size(self):
        """Testa a formatação do tamanho do arquivo"""
        self.assertEqual(self.version.formatted_file_size, "500 MB")
        
        # Teste para GB
        self.version.file_size_mb = 1500
        self.version.save()
        self.assertEqual(self.version.formatted_file_size, "1.46 GB")

class SystemRequirementModelTest(TestCase):
    """Testes para o modelo SystemRequirement"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Cria objetos necessários para o teste
        self.developer = Developer.objects.create(name="Valve")
        self.publisher = Publisher.objects.create(name="Valve")
        
        # Cria o jogo para teste
        self.game = Game.objects.create(
            title="Half-Life 2",
            base_price=Decimal('19.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.datetime(2004, 11, 16).date(),
        )
        
        # Cria requisitos de sistema
        self.requirements = SystemRequirement.objects.create(
            game=self.game,
            requirement_type="minimum", 
            os="Windows XP/Vista/7",
            processor="1.7 GHz",
            memory="512 MB RAM",
            graphics="DirectX 8.1 level Graphics Card",
            directx="Version 8.1",
            storage="6.5 GB",
            additional_notes="Keyboard and mouse required"
        )
    
    def test_requirements_creation(self):
        """Testa se os requisitos de sistema são criados corretamente"""
        self.assertEqual(self.requirements.game.title, "Half-Life 2")
        self.assertEqual(self.requirements.os, "Windows XP/Vista/7")
        self.assertEqual(self.requirements.memory, "512 MB RAM")
        self.assertEqual(self.requirements.storage, "6.5 GB")
        self.assertTrue(self.requirements.requirement_type, "minimum")
    
    def test_requirements_str_representation(self):
        """Testa a representação string do modelo"""
        self.assertEqual(str(self.requirements), "Requisitos Mínimos - Half-Life 2")
        
        # Muda para requisitos recomendados
        self.requirements.requirement_type = "recommended"
        self.requirements.save()
        self.assertEqual(str(self.requirements), "Requisitos Recomendados - Half-Life 2")
