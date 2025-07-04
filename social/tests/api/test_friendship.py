from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from social.models import Friendship


class FriendshipAPITest(TestCase):
    """Testes para a API de amizades"""
    
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
        
        self.user3 = User.objects.create_user(
            username='testuser3',
            email='test3@example.com',
            password='testpassword3'
        )
        
        # Criar amizades para os testes
        self.friendship_pending = Friendship.objects.create(
            sender=self.user1,
            receiver=self.user2,
            status='pending'
        )
        
        self.friendship_accepted = Friendship.objects.create(
            sender=self.user2,
            receiver=self.user3,
            status='accepted'
        )
        
        # Configurar cliente API
        self.client = APIClient()
        
        # URLs para os testes
        self.friendships_url = reverse('friendship-list')
        self.friendship_detail_url = lambda pk: reverse('friendship-detail', kwargs={'pk': pk})
        self.my_friends_url = reverse('friendship-my-friends')
        self.pending_requests_url = reverse('friendship-pending-requests')
        self.accept_url = lambda pk: reverse('friendship-accept', kwargs={'pk': pk})
        self.reject_url = lambda pk: reverse('friendship-reject', kwargs={'pk': pk})
        self.block_url = lambda pk: reverse('friendship-block', kwargs={'pk': pk})
    
    def test_friendship_unauthenticated(self):
        """Testa que usuários não autenticados não podem acessar amizades"""
        response = self.client.get(self.friendships_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_friendship_list(self):
        """Testa listar amizades do usuário"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.friendships_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_send_friend_request(self):
        """Testa enviar uma solicitação de amizade"""
        self.client.force_authenticate(user=self.user1)
        data = {
            'receiver': self.user3.id
        }
        response = self.client.post(self.friendships_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se a amizade foi criada no banco de dados
        friendship = Friendship.objects.filter(
            sender=self.user1,
            receiver=self.user3,
            status='pending'
        ).exists()
        self.assertTrue(friendship)
    
    def test_accept_friend_request(self):
        """Testa aceitar uma solicitação de amizade"""
        self.client.force_authenticate(user=self.user2)
        url = self.accept_url(self.friendship_pending.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a amizade foi atualizada no banco de dados
        friendship = Friendship.objects.get(id=self.friendship_pending.id)
        self.assertEqual(friendship.status, 'accepted')
    
    def test_reject_friend_request(self):
        """Testa rejeitar uma solicitação de amizade"""
        self.client.force_authenticate(user=self.user2)
        url = self.reject_url(self.friendship_pending.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a amizade foi atualizada no banco de dados
        friendship = Friendship.objects.get(id=self.friendship_pending.id)
        self.assertEqual(friendship.status, 'rejected')
    
    def test_block_user(self):
        """Testa bloquear um usuário"""
        self.client.force_authenticate(user=self.user2)
        url = self.block_url(self.friendship_pending.id)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a amizade foi atualizada no banco de dados
        friendship = Friendship.objects.get(id=self.friendship_pending.id)
        self.assertEqual(friendship.status, 'blocked')
    
    def test_my_friends(self):
        """Testa listar apenas amizades aceitas"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.my_friends_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve mostrar apenas a amizade aceita com o user3
        friendship_ids = [f.get('id') for f in response.data if isinstance(f, dict) and 'id' in f]
        self.assertIn(self.friendship_accepted.id, friendship_ids)
        self.assertNotIn(self.friendship_pending.id, friendship_ids)
    
    def test_pending_requests(self):
        """Testa listar solicitações de amizade pendentes"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.pending_requests_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Deve mostrar apenas a solicitação pendente do user1
        friendship_ids = [f.get('id') for f in response.data if isinstance(f, dict) and 'id' in f]
        self.assertIn(self.friendship_pending.id, friendship_ids)
        self.assertNotIn(self.friendship_accepted.id, friendship_ids)
    
    def test_delete_friendship(self):
        """Testa excluir uma amizade"""
        self.client.force_authenticate(user=self.user1)
        url = self.friendship_detail_url(self.friendship_pending.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se a amizade foi excluída do banco de dados
        friendship_exists = Friendship.objects.filter(id=self.friendship_pending.id).exists()
        self.assertFalse(friendship_exists)
