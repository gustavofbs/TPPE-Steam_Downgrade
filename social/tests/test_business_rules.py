from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime

from social.models import (
    Friendship, GameReview, ReviewVote, 
    UserActivity, GameRecommendation, UserGamePreference
)
from games.models import Game, Developer, Publisher, Genre

User = get_user_model()

# Mock para imagens em testes
image_mock = SimpleUploadedFile(name='test_image.jpg', content=b'file_content', content_type='image/jpeg')

class FriendshipBusinessRulesTest(TestCase):
    """Testes para regras de negócio de amizades"""
    
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
    
    def test_friendship_status_transitions(self):
        """Testa as transições de status de amizade"""
        # Criar uma solicitação de amizade pendente
        friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='pending'
        )
        
        # Verificar status inicial
        self.assertEqual(friendship.status, 'pending')
        
        # Aceitar a solicitação
        friendship.status = 'accepted'
        friendship.save()
        
        updated_friendship = Friendship.objects.get(id=friendship.id)
        self.assertEqual(updated_friendship.status, 'accepted')
        
        # Bloquear a amizade
        friendship.status = 'blocked'
        friendship.save()
        
        updated_friendship = Friendship.objects.get(id=friendship.id)
        self.assertEqual(updated_friendship.status, 'blocked')
    
    def test_bidirectional_friendship_check(self):
        """Testa a verificação bidirecional de amizade"""
        # Criar uma amizade aceita
        friendship = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='accepted'
        )
        
        # Verificar se a amizade existe do user1 para user2
        friendship_1_to_2 = Friendship.objects.filter(
            sender=self.user1,
            receiver=self.user2,
            status='accepted'
        ).exists()
        
        self.assertTrue(friendship_1_to_2)
        
        # Verificar se não existe amizade do user2 para user1 (não é bidirecional por padrão)
        friendship_2_to_1 = Friendship.objects.filter(
            sender=self.user2,
            receiver=self.user1,
            status='accepted'
        ).exists()
        
        self.assertFalse(friendship_2_to_1)
        
        # Em um sistema real, a lógica de negócios trataria a amizade como bidirecional
        # mesmo que o registro no banco seja unidirecional
    
    def test_self_friendship_prevention(self):
        """Testa a prevenção de amizade consigo mesmo"""
        # Tentar criar uma amizade consigo mesmo
        with self.assertRaises(ValidationError):
            friendship = Friendship(
                sender=self.user1,
                receiver=self.user1,
                status='pending'
            )
            friendship.full_clean()

class GameReviewBusinessRulesTest(TestCase):
    """Testes para regras de negócio de avaliações de jogos"""
    
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
    
    def test_review_helpfulness_calculation(self):
        """Testa o cálculo de utilidade da avaliação"""
        # Criar uma avaliação
        review = GameReview.objects.create(
            user=self.user,
            game=self.game,
            rating=4,
            title="Great game!",
            content="This is a fantastic game with amazing graphics.",
            helpful_votes=10,
            not_helpful_votes=5
        )
        
        # Calcular a porcentagem de utilidade
        total_votes = review.helpful_votes + review.not_helpful_votes
        helpfulness_percentage = (review.helpful_votes / total_votes) * 100 if total_votes > 0 else 0
        
        # Verificar se o cálculo está correto
        self.assertEqual(helpfulness_percentage, 66.66666666666666)  # 10/15 * 100 = 66.67%
    
    def test_review_content_validation(self):
        """Testa a validação do conteúdo da avaliação"""
        # Criar uma avaliação sem título
        review = GameReview(
            user=self.user,
            game=self.game,
            rating=4,
            title="",
            content="This is a fantastic game with amazing graphics."
        )
        
        with self.assertRaises(ValidationError):
            review.full_clean()
        
        # Criar uma avaliação sem conteúdo
        review = GameReview(
            user=self.user,
            game=self.game,
            rating=4,
            title="Great game!",
            content=""
        )
        
        with self.assertRaises(ValidationError):
            review.full_clean()
        
        # Criar uma avaliação válida
        review = GameReview(
            user=self.user,
            game=self.game,
            rating=4,
            title="Great game!",
            content="This is a fantastic game with amazing graphics."
        )
        
        try:
            review.full_clean()
            review.save()
        except ValidationError:
            self.fail("Review with valid content should be valid")
    
    def test_review_update_validation(self):
        """Testa a validação de atualização de avaliação"""
        # Criar uma avaliação
        review = GameReview.objects.create(
            user=self.user,
            game=self.game,
            rating=3,
            title="Initial review",
            content="Initial content"
        )
        
        # Atualizar a avaliação
        review.rating = 5
        review.title = "Updated review"
        review.content = "Updated content"
        review.save()
        
        # Verificar se a atualização foi bem-sucedida
        updated_review = GameReview.objects.get(id=review.id)
        self.assertEqual(updated_review.rating, 5)
        self.assertEqual(updated_review.title, "Updated review")
        self.assertEqual(updated_review.content, "Updated content")
        
        # Verificar se o campo updated_at foi atualizado
        self.assertGreater(updated_review.updated_at, updated_review.created_at)

class ReviewVoteBusinessRulesTest(TestCase):
    """Testes para regras de negócio de votos em avaliações"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.reviewer = User.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
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
            user=self.reviewer,
            game=self.game,
            rating=4,
            title="Great game!",
            content="This is a fantastic game with amazing graphics."
        )
    
    def test_vote_uniqueness_per_user_review(self):
        """Testa a unicidade de votos por usuário e avaliação"""
        # Criar um voto
        vote = ReviewVote.objects.create(
            review=self.review,
            user=self.voter,
            vote_type='helpful'
        )
        
        # Tentar criar outro voto do mesmo usuário para a mesma avaliação
        with self.assertRaises(Exception):
            duplicate_vote = ReviewVote.objects.create(
                review=self.review,
                user=self.voter,
                vote_type='not_helpful'
            )
    
    def test_vote_change(self):
        """Testa a mudança de voto"""
        # Criar um voto
        vote = ReviewVote.objects.create(
            review=self.review,
            user=self.voter,
            vote_type='helpful'
        )
        
        # Atualizar o contador de votos úteis
        self.review.helpful_votes += 1
        self.review.save()
        
        # Mudar o tipo de voto
        vote.vote_type = 'not_helpful'
        vote.save()
        
        # Atualizar os contadores
        self.review.helpful_votes -= 1
        self.review.not_helpful_votes += 1
        self.review.save()
        
        # Verificar se os contadores foram atualizados corretamente
        updated_review = GameReview.objects.get(id=self.review.id)
        self.assertEqual(updated_review.helpful_votes, 0)
        self.assertEqual(updated_review.not_helpful_votes, 1)
    
    def test_self_vote_prevention(self):
        """Testa a prevenção de voto em própria avaliação"""
        # Tentar criar um voto do autor na própria avaliação
        with self.assertRaises(ValidationError):
            vote = ReviewVote(
                review=self.review,
                user=self.reviewer,  # Mesmo usuário que criou a avaliação
                vote_type='helpful'
            )
            vote.full_clean()

class UserActivityBusinessRulesTest(TestCase):
    """Testes para regras de negócio de atividades de usuário"""
    
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
    
    def test_activity_privacy_filter(self):
        """Testa o filtro de privacidade de atividades"""
        # Criar atividades públicas e privadas
        public_activity = UserActivity.objects.create(
            user=self.user,
            activity_type='purchase',
            game=self.game,
            description="Comprou Test Game",
            is_public=True
        )
        
        private_activity = UserActivity.objects.create(
            user=self.user,
            activity_type='playtime',
            game=self.game,
            description="Jogou Test Game por 10 horas",
            is_public=False
        )
        
        # Filtrar atividades públicas
        public_activities = UserActivity.objects.filter(is_public=True)
        
        # Verificar se apenas a atividade pública está no resultado
        self.assertEqual(public_activities.count(), 1)
        self.assertIn(public_activity, public_activities)
        self.assertNotIn(private_activity, public_activities)
    
    def test_activity_type_validation(self):
        """Testa a validação do tipo de atividade"""
        # Tentar criar uma atividade com tipo inválido
        with self.assertRaises(ValidationError):
            activity = UserActivity(
                user=self.user,
                activity_type='invalid_type',
                description="Atividade inválida"
            )
            activity.full_clean()
        
        # Criar atividades com tipos válidos
        valid_types = ['purchase', 'review', 'achievement', 'friend', 'playtime', 'wishlist']
        
        for activity_type in valid_types:
            activity = UserActivity(
                user=self.user,
                activity_type=activity_type,
                description=f"Atividade de {activity_type}"
            )
            try:
                activity.full_clean()
                activity.save()
            except ValidationError:
                self.fail(f"Activity with type {activity_type} should be valid")

class GameRecommendationBusinessRulesTest(TestCase):
    """Testes para regras de negócio de recomendações de jogos"""
    
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
    
    def test_recommendation_read_status(self):
        """Testa o status de leitura de uma recomendação"""
        # Criar uma recomendação não lida
        recommendation = GameRecommendation.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            game=self.game,
            message="Você vai adorar este jogo!",
            is_read=False
        )
        
        # Verificar status inicial
        self.assertFalse(recommendation.is_read)
        
        # Marcar como lida
        recommendation.is_read = True
        recommendation.save()
        
        # Verificar se foi marcada como lida
        updated_recommendation = GameRecommendation.objects.get(id=recommendation.id)
        self.assertTrue(updated_recommendation.is_read)
    
    def test_self_recommendation_prevention(self):
        """Testa a prevenção de recomendação para si mesmo"""
        # Tentar criar uma recomendação para si mesmo
        with self.assertRaises(ValidationError):
            recommendation = GameRecommendation(
                sender=self.sender,
                receiver=self.sender,  # Mesmo usuário
                game=self.game,
                message="Recomendação para mim mesmo"
            )
            recommendation.full_clean()

class UserGamePreferenceBusinessRulesTest(TestCase):
    """Testes para regras de negócio de preferências de jogos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        self.rpg_genre = Genre.objects.create(
            name="RPG",
            description="Role-playing games"
        )
        
        self.action_genre = Genre.objects.create(
            name="Action",
            description="Action games"
        )
    
    def test_preference_weight_validation(self):
        """Testa a validação do peso da preferência"""
        # Peso menor que 1 não deve ser permitido
        preference = UserGamePreference(
            user=self.user,
            genre=self.rpg_genre,
            weight=0
        )
        
        with self.assertRaises(ValidationError):
            preference.full_clean()
        
        # Peso maior que 10 não deve ser permitido
        preference.weight = 11
        
        with self.assertRaises(ValidationError):
            preference.full_clean()
        
        # Pesos válidos devem ser aceitos
        for weight in range(1, 11):
            preference.weight = weight
            try:
                preference.full_clean()
            except ValidationError:
                self.fail(f"Weight {weight} should be valid")
    
    def test_preference_uniqueness(self):
        """Testa a unicidade de preferência por usuário e gênero"""
        # Criar uma preferência
        preference = UserGamePreference.objects.create(
            user=self.user,
            genre=self.rpg_genre,
            weight=8
        )
        
        # Tentar criar outra preferência para o mesmo usuário e gênero
        with self.assertRaises(Exception):
            duplicate_preference = UserGamePreference.objects.create(
                user=self.user,
                genre=self.rpg_genre,
                weight=5
            )
    
    def test_preference_update(self):
        """Testa a atualização de uma preferência"""
        # Criar uma preferência
        preference = UserGamePreference.objects.create(
            user=self.user,
            genre=self.rpg_genre,
            weight=5
        )
        
        # Atualizar o peso
        preference.weight = 9
        preference.save()
        
        # Verificar se o peso foi atualizado
        updated_preference = UserGamePreference.objects.get(id=preference.id)
        self.assertEqual(updated_preference.weight, 9)
        
        # Verificar se o campo updated_at foi atualizado
        self.assertGreater(updated_preference.updated_at, updated_preference.created_at)
