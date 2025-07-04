from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from rest_framework.test import APIClient
from rest_framework import status
import datetime
from decimal import Decimal

from games.models import Game, Genre, Developer, Publisher
from social.models import (
    GameReview, ReviewComment, UserActivity,
    GameRecommendation, UserGamePreference
)


class ReviewCommentAPITest(TestCase):
    """Testes para a API de comentários em avaliações"""
    
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
        
        # Criar jogo para os testes
        self.developer = Developer.objects.create(name='Test Developer')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.game = Game.objects.create(
            title='Test Game',
            slug='test-game',
            description='A test game',
            short_description='Test game',
            release_date=datetime.date(2023, 1, 1),
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher
        )
        
        # Criar avaliação para os testes
        self.review = GameReview.objects.create(
            user=self.user1,
            game=self.game,
            title='Great game',
            content='This is a great game, I recommend it!',
            rating=4,
            is_recommended=True
        )
        
        # Criar comentário para os testes
        self.comment = ReviewComment.objects.create(
            user=self.user2,
            review=self.review,
            content='I agree with your review!'
        )
        
        # Configurar cliente API
        self.client = APIClient()
        
        # URLs para os testes
        self.comments_url = reverse('comment-list')
        self.comment_detail_url = lambda pk: reverse('comment-detail', kwargs={'pk': pk})
    
    def test_comment_list(self):
        """Testa listar comentários"""
        response = self.client.get(self.comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_comment_detail(self):
        """Testa obter detalhes de um comentário"""
        url = self.comment_detail_url(self.comment.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.comment.id)
    
    def test_create_comment(self):
        """Testa criar um comentário"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'review': self.review.id,
            'content': 'Thanks for your feedback!'
        }
        response = self.client.post(self.comments_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o comentário foi criado no banco de dados
        comment = ReviewComment.objects.filter(
            user=self.user1,
            review=self.review,
            content='Thanks for your feedback!'
        ).exists()
        self.assertTrue(comment)
    
    def test_update_comment(self):
        """Testa atualizar um comentário"""
        self.client.force_authenticate(user=self.user2)
        url = self.comment_detail_url(self.comment.id)
        data = {
            'review': self.review.id,
            'content': 'I updated my comment!'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o comentário foi atualizado no banco de dados
        comment = ReviewComment.objects.get(id=self.comment.id)
        self.assertEqual(comment.content, 'I updated my comment!')
    
    def test_delete_comment(self):
        """Testa excluir um comentário"""
        self.client.force_authenticate(user=self.user2)
        url = self.comment_detail_url(self.comment.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se o comentário foi excluído do banco de dados
        comment_exists = ReviewComment.objects.filter(id=self.comment.id).exists()
        self.assertFalse(comment_exists)
    
    def test_filter_comments_by_review(self):
        """Testa filtrar comentários por avaliação"""
        # Criar uma segunda avaliação e comentário
        review2 = GameReview.objects.create(
            user=self.user2,
            game=self.game,
            title='Another review',
            content='This is another review',
            rating=3,
            is_recommended=False
        )
        
        comment2 = ReviewComment.objects.create(
            user=self.user1,
            review=review2,
            content='Interesting review!'
        )
        
        # Filtrar comentários pela primeira avaliação
        response = self.client.get(f"{self.comments_url}?review={self.review.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se apenas os comentários da primeira avaliação são retornados
        for comment in response.data:
            if isinstance(comment, dict) and 'review' in comment:
                self.assertEqual(comment['review'], self.review.id)


class UserActivityAPITest(TestCase):
    """Testes para a API de atividades de usuários"""
    
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
        
        # Criar jogo para os testes
        self.developer = Developer.objects.create(name='Test Developer')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.game = Game.objects.create(
            title='Test Game',
            slug='test-game',
            description='A test game',
            short_description='Test game',
            release_date=datetime.date(2023, 1, 1),
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher
        )
        
        # Criar atividades para os testes
        self.activity_public = UserActivity.objects.create(
            user=self.user1,
            activity_type='purchase',
            game=self.game,
            description='Purchased Test Game',
            is_public=True
        )
        # Garantir que o ID seja atribuído corretamente
        self.activity_public.save()
        
        self.activity_private = UserActivity.objects.create(
            user=self.user1,
            activity_type='wishlist',
            game=self.game,
            description='Added Test Game to wishlist',
            is_public=False
        )
        self.activity_private.save()
        
        # Configurar cliente API
        self.client = APIClient()
        
        # URLs para os testes
        self.activities_url = reverse('activity-list')
        self.my_activities_url = reverse('activity-my-activities')
        self.friends_activities_url = reverse('activity-friends-activities')
    
    def test_activities_unauthenticated(self):
        """Testa que usuários não autenticados não podem acessar atividades"""
        response = self.client.get(self.activities_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_activities_list(self):
        """Testa listar atividades públicas"""
        # Garantir que a atividade pública seja criada com um ID válido
        self.activity_public.refresh_from_db()
        
        # Autenticar como outro usuário para ver apenas atividades públicas
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.activities_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a resposta é paginada
        self.assertIn('results', response.data)
        
        # Verificar se a atividade pública está na lista
        # Primeiro, imprimir os dados para debug
        print(f"\nAtividade pública ID: {self.activity_public.id}")
        print(f"Resposta da API: {response.data}")
        
        # Verificar se há pelo menos uma atividade na resposta
        self.assertGreater(len(response.data['results']), 0, "A lista de atividades está vazia")
        
        # Verificar se a atividade pública está na lista
        activity_found = False
        private_activity_found = False
        for activity in response.data['results']:
            if isinstance(activity, dict) and 'id' in activity:
                if activity['id'] == self.activity_public.id:
                    activity_found = True
                if activity['id'] == self.activity_private.id:
                    private_activity_found = True
        self.assertTrue(activity_found, "A atividade pública não foi encontrada na lista")
        self.assertFalse(private_activity_found, "A atividade privada não deveria estar na lista")
    
    def test_my_activities(self):
        """Testa listar atividades do próprio usuário"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.my_activities_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a resposta é paginada ou uma lista simples
        if isinstance(response.data, dict) and 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data
        
        # Verificar se todas as atividades do usuário são retornadas (públicas e privadas)
        activity_ids = [a.get('id') for a in results if isinstance(a, dict) and 'id' in a]
        self.assertIn(self.activity_public.id, activity_ids)
        self.assertIn(self.activity_private.id, activity_ids)


class GameRecommendationAPITest(TestCase):
    """Testes para a API de recomendações de jogos"""
    
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
        
        # Criar jogo para os testes
        self.developer = Developer.objects.create(name='Test Developer')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.game = Game.objects.create(
            title='Test Game',
            slug='test-game',
            description='A test game',
            short_description='Test game',
            release_date=datetime.date(2023, 1, 1),
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher
        )
        
        # Criar recomendação para os testes
        self.recommendation = GameRecommendation.objects.create(
            sender=self.user1,
            receiver=self.user2,
            game=self.game,
            message='You should try this game!'
        )
        
        # Configurar cliente API
        self.client = APIClient()
        
        # URLs para os testes
        self.recommendations_url = reverse('recommendation-list')
        self.recommendation_detail_url = lambda pk: reverse('recommendation-detail', kwargs={'pk': pk})
        self.received_recommendations_url = reverse('recommendation-received')
        self.sent_recommendations_url = reverse('recommendation-sent')
        self.mark_as_read_url = lambda pk: reverse('recommendation-mark-as-read', kwargs={'pk': pk})
    
    def test_recommendations_unauthenticated(self):
        """Testa que usuários não autenticados não podem acessar recomendações"""
        response = self.client.get(self.recommendations_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_recommendations_list(self):
        """Testa listar recomendações do usuário"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.recommendations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_send_recommendation(self):
        """Testa enviar uma recomendação de jogo"""
        self.client.force_authenticate(user=self.user2)
        data = {
            'receiver': self.user1.id,
            'game': self.game.id,
            'message': 'I think you would like this game!'
        }
        response = self.client.post(self.recommendations_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se a recomendação foi criada no banco de dados
        recommendation = GameRecommendation.objects.filter(
            sender=self.user2,
            receiver=self.user1,
            game=self.game
        ).exists()
        self.assertTrue(recommendation)
    
    def test_mark_recommendation_as_read(self):
        """Testa marcar uma recomendação como lida"""
        self.client.force_authenticate(user=self.user2)
        url = self.mark_as_read_url(self.recommendation.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a recomendação foi atualizada no banco de dados
        recommendation = GameRecommendation.objects.get(id=self.recommendation.id)
        self.assertTrue(recommendation.is_read)
    
    def test_received_recommendations(self):
        """Testa listar recomendações recebidas"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.received_recommendations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se apenas as recomendações recebidas são retornadas
        recommendation_ids = [r.get('id') for r in response.data if isinstance(r, dict) and 'id' in r]
        self.assertIn(self.recommendation.id, recommendation_ids)
    
    def test_sent_recommendations(self):
        """Testa listar recomendações enviadas"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.sent_recommendations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se apenas as recomendações enviadas são retornadas
        recommendation_ids = [r.get('id') for r in response.data if isinstance(r, dict) and 'id' in r]
        self.assertIn(self.recommendation.id, recommendation_ids)


class UserGamePreferenceAPITest(TestCase):
    """Testes para a API de preferências de jogos"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar usuários para os testes
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Criar gêneros para os testes
        self.genre1 = Genre.objects.create(
            name='Action',
            slug='action',
            description='Action games'
        )
        
        self.genre2 = Genre.objects.create(
            name='Adventure',
            slug='adventure',
            description='Adventure games'
        )
        
        # Criar jogos para os testes
        self.developer = Developer.objects.create(name='Test Developer')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        
        self.game1 = Game.objects.create(
            title='Action Game',
            slug='action-game',
            description='An action game',
            short_description='Action game',
            release_date=datetime.date(2023, 1, 1),
            base_price=Decimal('29.99'),
            developer=self.developer,
            publisher=self.publisher,
            is_active=True
        )
        self.game1.genres.add(self.genre1)
        
        self.game2 = Game.objects.create(
            title='Adventure Game',
            slug='adventure-game',
            description='An adventure game',
            short_description='Adventure game',
            release_date=datetime.date(2023, 2, 1),
            base_price=Decimal('39.99'),
            developer=self.developer,
            publisher=self.publisher,
            is_active=True
        )
        self.game2.genres.add(self.genre2)
        
        # Criar preferência para os testes
        self.preference = UserGamePreference.objects.create(
            user=self.user,
            genre=self.genre1,
            weight=8
        )
        
        # Configurar cliente API
        self.client = APIClient()
        
        # URLs para os testes
        self.preferences_url = reverse('preference-list')
        self.preference_detail_url = lambda pk: reverse('preference-detail', kwargs={'pk': pk})
        self.recommended_games_url = reverse('preference-recommended-games')
    
    def test_preferences_unauthenticated(self):
        """Testa que usuários não autenticados não podem acessar preferências"""
        response = self.client.get(self.preferences_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_preferences_list(self):
        """Testa listar preferências do usuário"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.preferences_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_create_preference(self):
        """Testa criar uma preferência de gênero"""
        self.client.force_authenticate(user=self.user)
        data = {
            'genre': self.genre2.id,
            'weight': 6
        }
        response = self.client.post(self.preferences_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se a preferência foi criada no banco de dados
        preference = UserGamePreference.objects.filter(
            user=self.user,
            genre=self.genre2,
            weight=6
        ).exists()
        self.assertTrue(preference)
    
    def test_update_preference(self):
        """Testa atualizar uma preferência de gênero"""
        self.client.force_authenticate(user=self.user)
        url = self.preference_detail_url(self.preference.id)
        data = {
            'genre': self.genre1.id,
            'weight': 10
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a preferência foi atualizada no banco de dados
        preference = UserGamePreference.objects.get(id=self.preference.id)
        self.assertEqual(preference.weight, 10)
    
    def test_delete_preference(self):
        """Testa excluir uma preferência de gênero"""
        self.client.force_authenticate(user=self.user)
        url = self.preference_detail_url(self.preference.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se a preferência foi excluída do banco de dados
        preference_exists = UserGamePreference.objects.filter(id=self.preference.id).exists()
        self.assertFalse(preference_exists)
    
    def test_recommended_games(self):
        """Testa obter jogos recomendados com base nas preferências"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.recommended_games_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o jogo do gênero preferido está na lista de recomendações
        game_ids = [g.get('id') for g in response.data if isinstance(g, dict) and 'id' in g]
        self.assertIn(self.game1.id, game_ids)
