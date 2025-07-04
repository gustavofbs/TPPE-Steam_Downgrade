from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
import datetime
from decimal import Decimal

from games.models import Game, Genre, Developer, Publisher
from social.models import GameReview, ReviewVote, UserActivity


class GameReviewAPITest(TestCase):
    """Testes para a API de avaliações de jogos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuários para os testes
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword1'
        )
        
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword2'
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
            publisher=self.publisher,
            is_active=True
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
            publisher=self.publisher,
            is_active=True
        )
        self.game2.genres.add(self.genre)
        
        # Criar avaliações para os testes
        self.review = GameReview.objects.create(
            user=self.user1,
            game=self.game1,
            title='Great game',
            content='This is a great game, I recommend it!',
            rating=4,
            is_recommended=True,
            playtime_at_review=120
        )
        
        # Configurar cliente API
        self.client = APIClient()
        
        # URLs para os testes
        self.reviews_url = reverse('review-list')
        self.review_detail_url = lambda pk: reverse('review-detail', kwargs={'pk': pk})
        self.mark_helpful_url = lambda pk: reverse('review-mark-helpful', kwargs={'pk': pk})
        self.mark_not_helpful_url = lambda pk: reverse('review-mark-not-helpful', kwargs={'pk': pk})
    
    def test_review_list(self):
        """Testa listar avaliações"""
        response = self.client.get(self.reviews_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_review_detail(self):
        """Testa obter detalhes de uma avaliação"""
        url = self.review_detail_url(self.review.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.review.id)
    
    def test_create_review(self):
        """Testa criar uma avaliação"""
        self.client.force_authenticate(user=self.user2)
        data = {
            'game': self.game2.id,
            'title': 'Good game',
            'content': 'This is a good game, worth playing.',
            'rating': 3,
            'is_recommended': True
        }
        response = self.client.post(self.reviews_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se a avaliação foi criada no banco de dados
        review = GameReview.objects.filter(
            user=self.user2,
            game=self.game2,
            title='Good game'
        ).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 3)
        
        # Verificar se a atividade foi criada
        activity = UserActivity.objects.filter(
            user=self.user2,
            activity_type='review',
            game=self.game2
        ).exists()
        self.assertTrue(activity)
    
    def test_update_review(self):
        """Testa atualizar uma avaliação"""
        self.client.force_authenticate(user=self.user1)
        url = self.review_detail_url(self.review.id)
        data = {
            'game': self.game1.id,
            'title': 'Updated review',
            'content': 'I have updated my review after playing more.',
            'rating': 5,
            'is_recommended': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a avaliação foi atualizada no banco de dados
        review = GameReview.objects.get(id=self.review.id)
        self.assertEqual(review.title, 'Updated review')
        self.assertEqual(review.rating, 5)
    
    def test_delete_review(self):
        """Testa excluir uma avaliação"""
        self.client.force_authenticate(user=self.user1)
        url = self.review_detail_url(self.review.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se a avaliação foi excluída do banco de dados
        review_exists = GameReview.objects.filter(id=self.review.id).exists()
        self.assertFalse(review_exists)
    
    def test_mark_review_helpful(self):
        """Testa marcar uma avaliação como útil"""
        self.client.force_authenticate(user=self.user2)
        url = self.mark_helpful_url(self.review.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o voto foi criado
        vote = ReviewVote.objects.filter(
            user=self.user2,
            review=self.review,
            vote_type='helpful'
        ).exists()
        self.assertTrue(vote)
        
        # Verificar se o contador foi atualizado
        review = GameReview.objects.get(id=self.review.id)
        self.assertGreater(review.helpful_votes, 0)
    
    def test_mark_review_not_helpful(self):
        """Testa marcar uma avaliação como não útil"""
        self.client.force_authenticate(user=self.user2)
        url = self.mark_not_helpful_url(self.review.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o voto foi criado
        vote = ReviewVote.objects.filter(
            user=self.user2,
            review=self.review,
            vote_type='not_helpful'
        ).exists()
        self.assertTrue(vote)
        
        # Verificar se o contador foi atualizado
        review = GameReview.objects.get(id=self.review.id)
        self.assertGreater(review.not_helpful_votes, 0)
    
    def test_filter_reviews_by_game(self):
        """Testa filtrar avaliações por jogo"""
        # Criar uma segunda avaliação para outro jogo
        GameReview.objects.create(
            user=self.user2,
            game=self.game2,
            title='Another game review',
            content='This is a review for another game',
            rating=3,
            is_recommended=False,
            playtime_at_review=60
        )
        
        # Filtrar avaliações pelo game1
        response = self.client.get(f"{self.reviews_url}?game={self.game1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se apenas as avaliações do game1 são retornadas
        for review in response.data:
            if isinstance(review, dict) and 'game' in review:
                self.assertEqual(review['game'], self.game1.id)
    
    def test_cannot_vote_own_review(self):
        """Testa que um usuário não pode votar na própria avaliação"""
        self.client.force_authenticate(user=self.user1)
        url = self.mark_helpful_url(self.review.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
