import pytest
from django.utils import timezone
from decimal import Decimal

@pytest.fixture
def genre():
    """Fixture para criar um gênero de jogo"""
    from games.models import Genre
    return Genre.objects.create(name="Test Genre", description="Test Description")

@pytest.fixture
def developer():
    """Fixture para criar uma desenvolvedora"""
    from games.models import Developer
    return Developer.objects.create(
        name="Test Developer", 
        website="https://testdev.com",
        description="Test Developer Description"
    )

@pytest.fixture
def publisher():
    """Fixture para criar uma publicadora"""
    from games.models import Publisher
    return Publisher.objects.create(
        name="Test Publisher", 
        website="https://testpub.com",
        description="Test Publisher Description"
    )

@pytest.fixture
def game(developer, publisher, genre):
    """Fixture para criar um jogo com relacionamentos"""
    from games.models import Game
    game = Game.objects.create(
        title="Test Game",
        description="Test Game Description",
        base_price=Decimal('29.99'),
        developer=developer,
        publisher=publisher,
        release_date=timezone.now().date()
    )
    game.genres.add(genre)
    return game

@pytest.fixture
def game_version(game):
    """Fixture para criar uma versão de jogo"""
    from games.models import GameVersion
    return GameVersion.objects.create(
        game=game,
        version_number="1.0",
        release_date=timezone.now().date(),
        description="Test Version",
        file_size_mb=1000
    )

@pytest.fixture
def system_requirement(game):
    """Fixture para criar requisitos de sistema"""
    from games.models import SystemRequirement
    return SystemRequirement.objects.create(
        game=game,
        os="Windows 10",
        processor="Intel i5",
        memory="8 GB RAM",
        graphics="NVIDIA GTX 1060",
        storage="50 GB",
        is_minimum=True
    )

@pytest.fixture
def game_image(game):
    """Fixture para criar uma imagem de jogo"""
    from games.models import GameImage
    return GameImage.objects.create(
        game=game,
        image="games/test/cover.jpg",
        is_cover=True
    )
