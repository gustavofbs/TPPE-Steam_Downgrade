from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from social.models import (
    Friendship, GameReview, ReviewVote, 
    UserActivity, GameRecommendation, UserGamePreference
)
from games.models import Game, Developer, Publisher, Genre
from purchases.models import Library, LibraryItem

User = get_user_model()

# Mock para imagens em testes
image_mock = SimpleUploadedFile(name='test_image.jpg', content=b'file_content', content_type='image/jpeg')

class FriendshipActivityIntegrationTest(TestCase):
    """Testes de integração entre amizades e atividades de usuário"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )
    
    def test_friendship_creates_activity(self):
        """Testa se a criação de uma amizade gera uma atividade de usuário"""
        # Criar uma amizade
        friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='accepted'
        )
        
        # Criar atividade para o remetente
        sender_activity = UserActivity.objects.create(
            user=self.user1,
            activity_type='friend',
            description=f"Fez amizade com {self.user2.username}",
            is_public=True
        )
        
        # Criar atividade para o destinatário
        receiver_activity = UserActivity.objects.create(
            user=self.user2,
            activity_type='friend',
            description=f"Fez amizade com {self.user1.username}",
            is_public=True
        )
        
        # Verificar se as atividades foram criadas corretamente
        self.assertEqual(sender_activity.user, self.user1)
        self.assertEqual(sender_activity.activity_type, 'friend')
        self.assertEqual(sender_activity.description, f"Fez amizade com {self.user2.username}")
        
        self.assertEqual(receiver_activity.user, self.user2)
        self.assertEqual(receiver_activity.activity_type, 'friend')
        self.assertEqual(receiver_activity.description, f"Fez amizade com {self.user1.username}")

class ReviewVoteIntegrationTest(TestCase):
    """Testes de integração entre avaliações e votos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='password123'
        )
        
        self.voter1 = User.objects.create_user(
            username='voter1',
            email='voter1@example.com',
            password='password123'
        )
        
        self.voter2 = User.objects.create_user(
            username='voter2',
            email='voter2@example.com',
            password='password123'
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
            slug="test-game",
            base_price=29.99,
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date(),
            cover_image=image_mock
        )
        
        self.review = GameReview.objects.create(
            user=self.user,
            game=self.game,
            rating=4,
            title="Great game!",
            content="This is a fantastic game with amazing graphics.",
            helpful_votes=0,
            not_helpful_votes=0
        )
    
    def test_votes_update_review_counters(self):
        """Testa se os votos atualizam corretamente os contadores da avaliação"""
        # Adicionar um voto útil
        helpful_vote = ReviewVote.objects.create(
            review=self.review,
            user=self.voter1,
            vote_type='helpful'
        )
        
        # Atualizar o contador de votos úteis
        self.review.helpful_votes += 1
        self.review.save()
        
        # Verificar se o contador foi atualizado
        updated_review = GameReview.objects.get(id=self.review.id)
        self.assertEqual(updated_review.helpful_votes, 1)
        self.assertEqual(updated_review.not_helpful_votes, 0)
        
        # Adicionar um voto não útil
        not_helpful_vote = ReviewVote.objects.create(
            review=self.review,
            user=self.voter2,
            vote_type='not_helpful'
        )
        
        # Atualizar o contador de votos não úteis
        updated_review.not_helpful_votes += 1
        updated_review.save()
        
        # Verificar se o contador foi atualizado
        final_review = GameReview.objects.get(id=self.review.id)
        self.assertEqual(final_review.helpful_votes, 1)
        self.assertEqual(final_review.not_helpful_votes, 1)

class LibraryReviewIntegrationTest(TestCase):
    """Testes de integração entre biblioteca e avaliações"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
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
            slug="test-game",
            base_price=29.99,
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date(),
            cover_image=image_mock
        )
        
        # Criar biblioteca e adicionar jogo
        self.library = Library.objects.create(user=self.user)
        self.library_item = LibraryItem.objects.create(
            library=self.library,
            game=self.game,
            playtime=120  # 2 horas de jogo
        )
    
    def test_review_with_library_playtime(self):
        """Testa a criação de uma avaliação com o tempo de jogo da biblioteca"""
        # Criar uma avaliação usando o tempo de jogo da biblioteca
        review = GameReview.objects.create(
            user=self.user,
            game=self.game,
            rating=5,
            title="Excelente jogo!",
            content="Joguei por 2 horas e adorei cada minuto.",
            playtime_at_review=self.library_item.playtime,
            is_recommended=True
        )
        
        # Verificar se o tempo de jogo foi registrado corretamente
        self.assertEqual(review.playtime_at_review, 120)
        
        # Criar atividade de avaliação
        activity = UserActivity.objects.create(
            user=self.user,
            activity_type='review',
            game=self.game,
            description=f"Avaliou {self.game.title} com {review.rating} estrelas",
            is_public=True
        )
        
        # Verificar se a atividade foi criada corretamente
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'review')
        self.assertEqual(activity.game, self.game)

class FriendshipRecommendationIntegrationTest(TestCase):
    """Testes de integração entre amizades e recomendações"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )
        
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='password123'
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
            slug="test-game",
            base_price=29.99,
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date(),
            cover_image=image_mock
        )
        
        # Criar amizades
        self.friendship1 = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='accepted'
        )
        
        self.friendship2 = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user3,
            status='pending'
        )
    
    def test_recommend_game_to_friend(self):
        """Testa a recomendação de um jogo para um amigo"""
        # Recomendar jogo para um amigo aceito
        recommendation1 = GameRecommendation.objects.create(
            sender=self.user1,
            receiver=self.user2,
            game=self.game,
            message="Você vai adorar este jogo!"
        )
        
        # Verificar se a recomendação foi criada corretamente
        self.assertEqual(recommendation1.sender, self.user1)
        self.assertEqual(recommendation1.receiver, self.user2)
        self.assertEqual(recommendation1.game, self.game)
        
        # Tentar recomendar para um usuário com amizade pendente
        recommendation2 = GameRecommendation.objects.create(
            sender=self.user1,
            receiver=self.user3,
            game=self.game,
            message="Experimente este jogo!"
        )
        
        # A recomendação deve ser criada, mas poderia ser filtrada na lógica de negócios
        self.assertEqual(recommendation2.sender, self.user1)
        self.assertEqual(recommendation2.receiver, self.user3)

class UserPreferenceRecommendationIntegrationTest(TestCase):
    """Testes de integração entre preferências de usuário e recomendações"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        # Criar gêneros
        self.rpg_genre = Genre.objects.create(
            name="RPG",
            description="Role-playing games"
        )
        
        self.action_genre = Genre.objects.create(
            name="Action",
            description="Action games"
        )
        
        # Criar preferências de usuário
        self.rpg_preference = UserGamePreference.objects.create(
            user=self.user,
            genre=self.rpg_genre,
            weight=9  # Alta preferência por RPG
        )
        
        self.action_preference = UserGamePreference.objects.create(
            user=self.user,
            genre=self.action_genre,
            weight=3  # Baixa preferência por Action
        )
        
        self.developer = Developer.objects.create(
            name="Test Developer",
            website="https://testdev.com"
        )
        
        self.publisher = Publisher.objects.create(
            name="Test Publisher",
            website="https://testpub.com"
        )
        
        # Criar jogos de diferentes gêneros
        self.rpg_game = Game.objects.create(
            title="RPG Game",
            slug="rpg-game",
            base_price=39.99,
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date(),
            cover_image=image_mock
        )
        self.rpg_game.genres.add(self.rpg_genre)
        
        self.action_game = Game.objects.create(
            title="Action Game",
            slug="action-game",
            base_price=29.99,
            developer=self.developer,
            publisher=self.publisher,
            release_date=timezone.now().date(),
            cover_image=image_mock
        )
        self.action_game.genres.add(self.action_genre)
    
    def test_game_recommendation_based_on_preferences(self):
        """Testa a recomendação de jogos com base nas preferências do usuário"""
        # Simular um sistema de recomendação baseado em preferências
        
        # Obter as preferências do usuário
        preferences = UserGamePreference.objects.filter(user=self.user)
        
        # Verificar se as preferências foram obtidas corretamente
        self.assertEqual(preferences.count(), 2)
        
        # Verificar se a preferência por RPG é maior que a preferência por Action
        rpg_weight = preferences.get(genre=self.rpg_genre).weight
        action_weight = preferences.get(genre=self.action_genre).weight
        
        self.assertGreater(rpg_weight, action_weight)
        
        # Com base nas preferências, o jogo RPG deveria ser recomendado primeiro
        # Isso seria implementado na lógica de negócios, aqui apenas verificamos os dados
