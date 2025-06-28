from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from social.models import (
    Friendship, GameReview, ReviewVote, 
    UserActivity, GameRecommendation, UserGamePreference
)
from games.models import Game, Developer, Publisher, Genre

User = get_user_model()

# Mock para imagens em testes
image_mock = SimpleUploadedFile(name='test_image.jpg', content=b'file_content', content_type='image/jpeg')

class FriendshipModelTest(TestCase):
    """Testes para o modelo Friendship"""
    
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
        
        self.friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='pending'
        )
    
    def test_friendship_creation(self):
        """Testa se uma amizade é criada corretamente"""
        self.assertEqual(self.friendship.sender, self.user1)
        self.assertEqual(self.friendship.receiver, self.user2)
        self.assertEqual(self.friendship.status, 'pending')
        self.assertIsNotNone(self.friendship.created_at)
        self.assertIsNotNone(self.friendship.updated_at)
    
    def test_friendship_string_representation(self):
        """Testa a representação em string de uma amizade"""
        expected_string = f"{self.user1.username} -> {self.user2.username} (Pendente)"
        self.assertEqual(str(self.friendship), expected_string)
    
    def test_friendship_status_update(self):
        """Testa a atualização do status de uma amizade"""
        self.friendship.status = 'accepted'
        self.friendship.save()
        
        updated_friendship = Friendship.objects.get(id=self.friendship.id)
        self.assertEqual(updated_friendship.status, 'accepted')
    
    def test_friendship_unique_constraint(self):
        """Testa a restrição de unicidade entre remetente e destinatário"""
        # Tentar criar uma amizade duplicada deve falhar
        with self.assertRaises(Exception):
            duplicate_friendship = Friendship.objects.create(
                sender=self.user1,
                receiver=self.user2,
                status='pending'
            )

class GameReviewModelTest(TestCase):
    """Testes para o modelo GameReview"""
    
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
        
        self.review = GameReview.objects.create(
            user=self.user,
            game=self.game,
            rating=4,
            title="Great game!",
            content="This is a fantastic game with amazing graphics.",
            playtime_at_review=120,
            is_recommended=True,
            is_spoiler=False
        )
    
    def test_review_creation(self):
        """Testa se uma avaliação é criada corretamente"""
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.game, self.game)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.title, "Great game!")
        self.assertEqual(self.review.content, "This is a fantastic game with amazing graphics.")
        self.assertEqual(self.review.playtime_at_review, 120)
        self.assertTrue(self.review.is_recommended)
        self.assertFalse(self.review.is_spoiler)
        self.assertEqual(self.review.helpful_votes, 0)
        self.assertEqual(self.review.not_helpful_votes, 0)
    
    def test_review_string_representation(self):
        """Testa a representação em string de uma avaliação"""
        expected_string = f"Avaliação de {self.user.username} para {self.game.title}"
        self.assertEqual(str(self.review), expected_string)
    
    def test_review_rating_validation(self):
        """Testa a validação da classificação (rating) de uma avaliação"""
        # Rating menor que 1 não deve ser permitido
        self.review.rating = 0
        with self.assertRaises(ValidationError):
            self.review.full_clean()
        
        # Rating maior que 5 não deve ser permitido
        self.review.rating = 6
        with self.assertRaises(ValidationError):
            self.review.full_clean()
        
        # Ratings válidos devem ser aceitos
        for rating in range(1, 6):
            self.review.rating = rating
            try:
                self.review.full_clean()
            except ValidationError:
                self.fail(f"Rating {rating} should be valid")
    
    def test_review_unique_constraint(self):
        """Testa a restrição de unicidade entre usuário e jogo"""
        # Tentar criar uma avaliação duplicada deve falhar
        with self.assertRaises(Exception):
            duplicate_review = GameReview.objects.create(
                user=self.user,
                game=self.game,
                rating=5,
                title="Another review",
                content="This should fail"
            )

class ReviewVoteModelTest(TestCase):
    """Testes para o modelo ReviewVote"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        self.voter = User.objects.create_user(
            username='voter',
            email='voter@example.com',
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
            content="This is a fantastic game with amazing graphics."
        )
        
        self.vote = ReviewVote.objects.create(
            review=self.review,
            user=self.voter,
            vote_type='helpful'
        )
    
    def test_vote_creation(self):
        """Testa se um voto é criado corretamente"""
        self.assertEqual(self.vote.review, self.review)
        self.assertEqual(self.vote.user, self.voter)
        self.assertEqual(self.vote.vote_type, 'helpful')
        self.assertIsNotNone(self.vote.created_at)
    
    def test_vote_string_representation(self):
        """Testa a representação em string de um voto"""
        expected_string = f"{self.voter.username} votou '{self.vote.get_vote_type_display()}' na avaliação de {self.user.username}"
        self.assertEqual(str(self.vote), expected_string)
    
    def test_vote_type_validation(self):
        """Testa a validação do tipo de voto"""
        # Tipo de voto inválido não deve ser permitido
        self.vote.vote_type = 'invalid_type'
        with self.assertRaises(ValidationError):
            self.vote.full_clean()
        
        # Tipos de voto válidos devem ser aceitos
        valid_vote_types = ['helpful', 'not_helpful']
        for vote_type in valid_vote_types:
            self.vote.vote_type = vote_type
            try:
                self.vote.full_clean()
            except ValidationError:
                self.fail(f"Vote type {vote_type} should be valid")

class UserActivityModelTest(TestCase):
    """Testes para o modelo UserActivity"""
    
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
        
        self.activity = UserActivity.objects.create(
            user=self.user,
            activity_type='purchase',
            game=self.game,
            description="Comprou Test Game",
            is_public=True
        )
    
    def test_activity_creation(self):
        """Testa se uma atividade é criada corretamente"""
        self.assertEqual(self.activity.user, self.user)
        self.assertEqual(self.activity.activity_type, 'purchase')
        self.assertEqual(self.activity.game, self.game)
        self.assertEqual(self.activity.description, "Comprou Test Game")
        self.assertTrue(self.activity.is_public)
        self.assertIsNotNone(self.activity.created_at)
    
    def test_activity_string_representation(self):
        """Testa a representação em string de uma atividade"""
        expected_string = f"{self.user.username}: {self.activity.description}"
        self.assertEqual(str(self.activity), expected_string)
    
    def test_activity_type_validation(self):
        """Testa a validação do tipo de atividade"""
        # Tipo de atividade inválido não deve ser permitido
        self.activity.activity_type = 'invalid_type'
        with self.assertRaises(ValidationError):
            self.activity.full_clean()
        
        # Tipos de atividade válidos devem ser aceitos
        valid_activity_types = ['purchase', 'review', 'achievement', 'friend', 'playtime', 'wishlist']
        for activity_type in valid_activity_types:
            self.activity.activity_type = activity_type
            try:
                self.activity.full_clean()
            except ValidationError:
                self.fail(f"Activity type {activity_type} should be valid")
    
    def test_activity_without_game(self):
        """Testa a criação de uma atividade sem jogo associado"""
        activity_without_game = UserActivity.objects.create(
            user=self.user,
            activity_type='friend',
            description="Fez amizade com outro usuário",
            is_public=True
        )
        
        self.assertIsNone(activity_without_game.game)
        self.assertEqual(activity_without_game.activity_type, 'friend')
        self.assertEqual(activity_without_game.description, "Fez amizade com outro usuário")

class GameRecommendationModelTest(TestCase):
    """Testes para o modelo GameRecommendation"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.sender = User.objects.create_user(
            username='sender',
            email='sender@example.com',
            password='password123'
        )
        
        self.receiver = User.objects.create_user(
            username='receiver',
            email='receiver@example.com',
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
        
        self.recommendation = GameRecommendation.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            game=self.game,
            message="Você vai adorar este jogo!",
            is_read=False
        )
    
    def test_recommendation_creation(self):
        """Testa se uma recomendação é criada corretamente"""
        self.assertEqual(self.recommendation.sender, self.sender)
        self.assertEqual(self.recommendation.receiver, self.receiver)
        self.assertEqual(self.recommendation.game, self.game)
        self.assertEqual(self.recommendation.message, "Você vai adorar este jogo!")
        self.assertFalse(self.recommendation.is_read)
        self.assertIsNotNone(self.recommendation.created_at)
    
    def test_recommendation_string_representation(self):
        """Testa a representação em string de uma recomendação"""
        expected_string = f"{self.sender.username} recomendou {self.game.title} para {self.receiver.username}"
        self.assertEqual(str(self.recommendation), expected_string)
    
    def test_recommendation_mark_as_read(self):
        """Testa a marcação de uma recomendação como lida"""
        self.assertFalse(self.recommendation.is_read)
        
        self.recommendation.is_read = True
        self.recommendation.save()
        
        updated_recommendation = GameRecommendation.objects.get(id=self.recommendation.id)
        self.assertTrue(updated_recommendation.is_read)

class UserGamePreferenceModelTest(TestCase):
    """Testes para o modelo UserGamePreference"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        self.genre = Genre.objects.create(
            name="RPG",
            description="Role-playing games"
        )
        
        self.preference = UserGamePreference.objects.create(
            user=self.user,
            genre=self.genre,
            weight=8
        )
    
    def test_preference_creation(self):
        """Testa se uma preferência é criada corretamente"""
        self.assertEqual(self.preference.user, self.user)
        self.assertEqual(self.preference.genre, self.genre)
        self.assertEqual(self.preference.weight, 8)
        self.assertIsNotNone(self.preference.created_at)
        self.assertIsNotNone(self.preference.updated_at)
    
    def test_preference_string_representation(self):
        """Testa a representação em string de uma preferência"""
        expected_string = f"{self.user.username} - {self.genre.name} (Peso: {self.preference.weight})"
        self.assertEqual(str(self.preference), expected_string)
    
    def test_preference_weight_validation(self):
        """Testa a validação do peso de uma preferência"""
        # Peso menor que 1 não deve ser permitido
        self.preference.weight = 0
        with self.assertRaises(ValidationError):
            self.preference.full_clean()
        
        # Peso maior que 10 não deve ser permitido
        self.preference.weight = 11
        with self.assertRaises(ValidationError):
            self.preference.full_clean()
        
        # Pesos válidos devem ser aceitos
        for weight in range(1, 11):
            self.preference.weight = weight
            try:
                self.preference.full_clean()
            except ValidationError:
                self.fail(f"Weight {weight} should be valid")
