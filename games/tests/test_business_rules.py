from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from decimal import Decimal
import datetime

from games.models import Genre, Developer, Publisher, Game, GameVersion, GameImage, SystemRequirement
image_mock = SimpleUploadedFile(name='cover.jpg', content=b'file_content', content_type='image/jpeg')

class GameBusinessRulesTest(TestCase):
    """Testes para as regras de negócio do modelo Game"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.developer = Developer.objects.create(name="Valve")
        self.publisher = Publisher.objects.create(name="Valve")
        self.genre = Genre.objects.create(name="FPS")
    
    def test_game_price_validation(self):
        """Testa validações de preço do jogo"""
        # Preço negativo não deve ser permitido
        game = Game(
            title="Half-Life",
            base_price=Decimal('-10.00'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        with self.assertRaises(ValidationError):
            game.full_clean()
        
        # Preço zero é permitido (jogo gratuito)
        game = Game(
            title="Team Fortress 2",
            slug="team-fortress-2",
            description="Um jogo gratuito de tiro em equipe.",
            base_price=Decimal('0.00'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date(),
            cover_image=image_mock
        )
        
        try:
            game.full_clean()
            game.save()
        except ValidationError:
            self.fail("Game with zero price should be valid (free game)")
    
    def test_game_discount_validation(self):
        """Testa validações de desconto do jogo"""
        # Desconto negativo não deve ser permitido
        game = Game(
            title="Portal",
            base_price=Decimal('19.99'),
            discount_percent=-10,
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        with self.assertRaises(ValidationError):
            game.full_clean()
        
        # Desconto maior que 100% não deve ser permitido
        game = Game(
            title="Portal",
            base_price=Decimal('19.99'),
            discount_percent=110,
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        with self.assertRaises(ValidationError):
            game.full_clean()
                

        # Desconto de 100% é permitido (jogo gratuito temporariamente)
        game = Game(
            title="Portal",
            slug="portal",
            description="Jogo de quebra-cabeça da Valve",
            base_price=Decimal('19.99'),
            discount_percent=100,
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date(),
            cover_image=image_mock
        )
        
        try:
            game.full_clean()
            game.save()
            self.assertEqual(game.discount_price, Decimal('0.00'))
        except ValidationError:
            self.fail("Game with 100% discount should be valid (temporarily free)")
    
    def test_game_release_date_validation(self):
        """Testa validações de data de lançamento"""
        # Data no futuro deve ser permitida (pré-venda)
        future_date = timezone.now().date() + datetime.timedelta(days=30)
        game = Game(
            title="Half-Life 3",
            slug="half-life-3",
            description="O mais aguardado de todos os tempos.",
            base_price=Decimal('59.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=future_date,
            cover_image=image_mock
        )
        
        try:
            game.full_clean()
            game.save()
            self.assertTrue(game.is_pre_order)
        except ValidationError:
            self.fail("Game with future release date should be valid (pre-order)")
    
    def test_game_discount_calculation(self):
        """Testa cálculos de desconto"""
        game = Game.objects.create(
            title="Left 4 Dead",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        # Sem desconto
        self.assertEqual(game.discount_price, Decimal('29.99'))
        
        # 25% de desconto
        game.discount_percent = 25
        game.save()
        self.assertEqual(game.discount_price, Decimal('22.49'))
        
        # 33% de desconto
        game.discount_percent = 33
        game.save()
        self.assertEqual(game.discount_price, Decimal('20.09'))
        
        # 50% de desconto
        game.discount_percent = 50
        game.save()
        self.assertEqual(game.discount_price, Decimal('15.00'))
        
        # 75% de desconto
        game.discount_percent = 75
        game.save()
        self.assertEqual(game.discount_price, Decimal('7.50'))
        
        # 100% de desconto (gratuito)
        game.discount_percent = 100
        game.save()
        self.assertEqual(game.discount_price, Decimal('0.00'))
    
    def test_game_version_validation(self):
        """Testa validações de versão do jogo"""
        game = Game.objects.create(
            title="Counter-Strike",
            base_price=Decimal('9.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        # Tamanho de arquivo negativo não deve ser permitido
        version = GameVersion(
            game=game,
            version_number="1.6",
            file_size_mb=-100
        )
        
        with self.assertRaises(ValidationError):
            version.full_clean()
        
        # Tamanho de arquivo zero não deve ser permitido
        version = GameVersion(
            game=game,
            version_number="1.6",
            file_size_mb=0
        )
        
        with self.assertRaises(ValidationError):
            version.full_clean()
    
    def test_system_requirement_validation(self):
        """Testa validações de requisitos de sistema"""
        game = Game.objects.create(
            title="Half-Life 2",
            base_price=Decimal('19.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        # Não deve permitir dois requisitos mínimos para o mesmo jogo
        SystemRequirement.objects.create(
            game=game,
            os="Windows XP",
            processor="1.7 GHz",
            memory="512 MB RAM",
            requirement_type='minimum'
        )
        
        duplicate_min_req = SystemRequirement(
            game=game,
            os="Windows Vista",
            processor="1.8 GHz",
            memory="1 GB RAM",
            requirement_type='minimum'
        )
        
        with self.assertRaises(ValidationError):
            duplicate_min_req.full_clean()
        
        # Não deve permitir dois requisitos recomendados para o mesmo jogo
        SystemRequirement.objects.create(
            game=game,
            os="Windows 7",
            processor="2.4 GHz",
            memory="2 GB RAM",
            requirement_type='recommended'
        )
        
        duplicate_rec_req = SystemRequirement(
            game=game,
            os="Windows 10",
            processor="3.0 GHz",
            memory="4 GB RAM",
            requirement_type='recommended'
        )
        
        with self.assertRaises(ValidationError):
            duplicate_rec_req.full_clean()
    
    def test_game_image_cover_validation(self):
        """Testa validações de imagem de capa"""
        game = Game.objects.create(
            title="Portal 2",
            base_price=Decimal('19.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date()
        )
        
        # Cria uma imagem de capa
        GameImage.objects.create(
            game=game,
            image="games/portal2/cover.jpg",
            is_cover=True
        )
        
        # Não deve permitir duas imagens de capa para o mesmo jogo
        duplicate_cover = GameImage(
            game=game,
            image="games/portal2/cover2.jpg",
            is_cover=True
        )
        
        with self.assertRaises(ValidationError):
            duplicate_cover.full_clean()
        
        # Deve permitir imagens que não são de capa
        screenshot = GameImage(
            game=game,
            image="games/portal2/screenshot1.jpg",
            is_cover=False
        )
        
        try:
            screenshot.full_clean()
            screenshot.save()
        except ValidationError:
            self.fail("Non-cover image should be valid")
