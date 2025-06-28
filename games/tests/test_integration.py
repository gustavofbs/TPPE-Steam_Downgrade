from django.test import TestCase
from django.utils import timezone
from decimal import Decimal

from games.models import Genre, Developer, Publisher, Game, GameVersion, GameImage, SystemRequirement

class GameIntegrationTest(TestCase):
    """Testes de integração para o modelo Game e seus relacionamentos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Cria gêneros
        self.genre1 = Genre.objects.create(name="FPS", description="First Person Shooter", slug="fps")
        self.genre2 = Genre.objects.create(name="Ação", description="Jogos de ação", slug="acao")
        
        # Cria desenvolvedora e publicadora
        self.developer = Developer.objects.create(
            name="Valve", 
            website="https://www.valvesoftware.com"
        )
        self.publisher = Publisher.objects.create(
            name="Valve", 
            website="https://www.valvesoftware.com"
        )
        
        # Cria o jogo
        self.game = Game.objects.create(
            title="Half-Life 2",
            description="Um clássico FPS com elementos de física",
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.datetime(2004, 11, 16).date()
        )
        
        # Adiciona gêneros ao jogo
        self.game.genres.add(self.genre1, self.genre2)
        
        # Cria versões do jogo
        self.version1 = GameVersion.objects.create(
            game=self.game,
            version_number="1.0",
            release_date=timezone.datetime(2004, 11, 16).date(),
            description="Versão inicial",
            file_size_mb=4500
        )
        
        self.version2 = GameVersion.objects.create(
            game=self.game,
            version_number="1.1",
            release_date=timezone.datetime(2005, 2, 15).date(),
            description="Primeira atualização",
            file_size_mb=4600
        )
        
        # Cria imagens do jogo
        self.image1 = GameImage.objects.create(
            game=self.game,
            image="games/half-life2/cover.jpg",
            is_cover=True
        )
        
        self.image2 = GameImage.objects.create(
            game=self.game,
            image="games/half-life2/screenshot1.jpg",
            is_cover=False
        )
        
        # Cria requisitos de sistema
        self.min_req = SystemRequirement.objects.create(
            game=self.game,
            os="Windows XP/Vista/7",
            processor="1.7 GHz",
            memory="512 MB RAM",
            graphics="DirectX 8.1 level Graphics Card",
            storage="6.5 GB",
            requirement_type='minimum'
        )
        
        self.rec_req = SystemRequirement.objects.create(
            game=self.game,
            os="Windows 7/8/10",
            processor="2.4 GHz",
            memory="1 GB RAM",
            graphics="DirectX 9 level Graphics Card",
            storage="6.5 GB",
            requirement_type='recommended'
        )
    
    def test_game_genres_relationship(self):
        """Testa a relação entre jogos e gêneros"""
        self.assertEqual(self.game.genres.count(), 2)
        self.assertIn(self.genre1, self.game.genres.all())
        self.assertIn(self.genre2, self.game.genres.all())
        
        # Testa a relação inversa
        self.assertIn(self.game, self.genre1.games.all())
        self.assertIn(self.game, self.genre2.games.all())
    
    def test_game_versions_relationship(self):
        """Testa a relação entre jogos e suas versões"""
        versions = GameVersion.objects.filter(game=self.game)
        self.assertEqual(versions.count(), 2)
        self.assertIn(self.version1, versions)
        self.assertIn(self.version2, versions)
        
        # Verifica se as versões estão ordenadas por data de lançamento (mais recente primeiro)
        versions_ordered = list(versions.order_by('-release_date'))
        self.assertEqual(versions_ordered[0], self.version2)
        self.assertEqual(versions_ordered[1], self.version1)
    
    def test_game_images_relationship(self):
        """Testa a relação entre jogos e suas imagens"""
        images = GameImage.objects.filter(game=self.game)
        self.assertEqual(images.count(), 2)
        
        # Verifica se há exatamente uma imagem de capa
        cover_images = images.filter(is_cover=True)
        self.assertEqual(cover_images.count(), 1)
        self.assertEqual(cover_images.first(), self.image1)
        
        # Verifica método para obter a capa
        self.assertEqual(self.game.get_cover_image(), self.image1.image)
    
    def test_game_system_requirements(self):
        """Testa a relação entre jogos e seus requisitos de sistema"""
        requirements = SystemRequirement.objects.filter(game=self.game)
        self.assertEqual(requirements.count(), 2)
        
        # Verifica requisitos mínimos e recomendados
        min_reqs = requirements.filter(requirement_type='minimum')
        rec_reqs = requirements.filter(requirement_type='recommended')
        
        self.assertEqual(min_reqs.count(), 1)
        self.assertEqual(rec_reqs.count(), 1)
        self.assertEqual(min_reqs.first(), self.min_req)
        self.assertEqual(rec_reqs.first(), self.rec_req)
    
    def test_developer_games(self):
        """Testa a relação entre desenvolvedora e seus jogos"""
        developer_games = Game.objects.filter(developer=self.developer)
        self.assertEqual(developer_games.count(), 1)
        self.assertIn(self.game, developer_games)
    
    def test_publisher_games(self):
        """Testa a relação entre publicadora e seus jogos"""
        publisher_games = Game.objects.filter(publisher=self.publisher)
        self.assertEqual(publisher_games.count(), 1)
        self.assertIn(self.game, publisher_games)
    
    def test_cascading_delete(self):
        """Testa se a exclusão de um jogo exclui suas entidades relacionadas"""
        game_id = self.game.id
        self.game.delete()
        
        # Verifica se as versões foram excluídas
        self.assertEqual(GameVersion.objects.filter(game_id=game_id).count(), 0)
        
        # Verifica se as imagens foram excluídas
        self.assertEqual(GameImage.objects.filter(game_id=game_id).count(), 0)
        
        # Verifica se os requisitos de sistema foram excluídos
        self.assertEqual(SystemRequirement.objects.filter(game_id=game_id).count(), 0)
        
        # Verifica se os gêneros NÃO foram excluídos (many-to-many)
        self.assertEqual(Genre.objects.count(), 2)
        
        # Verifica se a desenvolvedora e publicadora NÃO foram excluídas
        self.assertEqual(Developer.objects.count(), 1)
        self.assertEqual(Publisher.objects.count(), 1)
