from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import Profile

class UserAPITest(TestCase):
    """Testes para a API de usuários"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar um cliente da API
        self.client = APIClient()
        
        # Criar usuários para os testes
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )
        
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        self.another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='anotherpassword123'
        )
        
        # URLs para os testes
        self.users_list_url = reverse('user-list')
        self.user_detail_url = lambda user_id: reverse('user-detail', kwargs={'pk': user_id})
        self.user_profile_url = lambda user_id: reverse('user-profile', kwargs={'pk': user_id})
        self.user_update_profile_url = lambda user_id: reverse('user-update-profile', kwargs={'pk': user_id})
        self.user_change_password_url = lambda user_id: reverse('user-change-password', kwargs={'pk': user_id})
        self.user_me_url = reverse('user-me')
    
    def _get_valid_image_file(self):
        """Cria um arquivo de imagem válido para testes"""
        image = Image.new('RGB', (100, 100), color='blue')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        return SimpleUploadedFile('test_avatar.jpg', buffer.read(), content_type='image/jpeg')
    
    def test_list_users_authenticated(self):
        """Testa a listagem de usuários por um usuário autenticado"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Fazer a requisição
        response = self.client.get(self.users_list_url)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # admin, regular_user, another_user
    
    def test_list_users_unauthenticated(self):
        """Testa a listagem de usuários por um usuário não autenticado"""
        # Fazer a requisição sem autenticação
        response = self.client.get(self.users_list_url)
        
        # Verificar a resposta (deve ser negada)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_user(self):
        """Testa a obtenção dos detalhes de um usuário"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Fazer a requisição
        response = self.client.get(self.user_detail_url(self.regular_user.id))
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_create_user(self):
        """Testa a criação de um novo usuário"""
        # Dados para o novo usuário
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        # Fazer a requisição (não precisa de autenticação para criar usuário)
        response = self.client.post(self.users_list_url, data)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o usuário foi criado
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Verificar se o perfil foi criado
        new_user = User.objects.get(username='newuser')
        self.assertTrue(Profile.objects.filter(user=new_user).exists())
    
    def test_create_user_invalid_data(self):
        """Testa a criação de um usuário com dados inválidos"""
        # Dados inválidos (senhas não correspondem)
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword123',
            'password2': 'differentpassword',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        # Fazer a requisição
        response = self.client.post(self.users_list_url, data)
        
        # Verificar a resposta (deve ser erro de validação)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verificar se o usuário não foi criado
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_update_user(self):
        """Testa a atualização de um usuário"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Dados para atualização
        data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        
        # Fazer a requisição
        response = self.client.put(self.user_detail_url(self.regular_user.id), data)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o usuário foi atualizado
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.username, 'updateduser')
        self.assertEqual(self.regular_user.email, 'updated@example.com')
        self.assertEqual(self.regular_user.first_name, 'Updated')
        self.assertEqual(self.regular_user.last_name, 'User')
    
    def test_update_another_user(self):
        """Testa a tentativa de atualizar outro usuário"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Dados para atualização
        data = {
            'username': 'hacked',
            'email': 'hacked@example.com',
            'first_name': 'Hacked',
            'last_name': 'User'
        }
        
        # Fazer a requisição para atualizar outro usuário
        response = self.client.put(self.user_detail_url(self.another_user.id), data)
        
        # Verificar a resposta (deve ser negada)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verificar se o outro usuário não foi atualizado
        self.another_user.refresh_from_db()
        self.assertEqual(self.another_user.username, 'anotheruser')
    
    def test_delete_user(self):
        """Testa a exclusão de um usuário"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Fazer a requisição
        response = self.client.delete(self.user_detail_url(self.regular_user.id))
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se o usuário foi excluído
        self.assertFalse(User.objects.filter(id=self.regular_user.id).exists())
    
    def test_delete_another_user(self):
        """Testa a tentativa de excluir outro usuário"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Fazer a requisição para excluir outro usuário
        response = self.client.delete(self.user_detail_url(self.another_user.id))
        
        # Verificar a resposta (deve ser negada)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verificar se o outro usuário não foi excluído
        self.assertTrue(User.objects.filter(id=self.another_user.id).exists())
    
    def test_get_profile(self):
        """Testa a obtenção do perfil de um usuário"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Fazer a requisição
        response = self.client.get(self.user_profile_url(self.regular_user.id))
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('bio', response.data)
        self.assertIn('birth_date', response.data)
        self.assertIn('avatar', response.data)
    
    def test_update_profile(self):
        """Testa a atualização do perfil de um usuário"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Dados para atualização
        data = {
            'bio': 'This is my updated bio',
            'birth_date': '1990-01-01',
        }
        
        # Fazer a requisição
        response = self.client.put(self.user_update_profile_url(self.regular_user.id), data)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o perfil foi atualizado
        profile = Profile.objects.get(user=self.regular_user)
        self.assertEqual(profile.bio, 'This is my updated bio')
        self.assertEqual(str(profile.birth_date), '1990-01-01')
    
    def test_update_profile_with_avatar(self):
        """Testa a atualização do perfil com avatar"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Criar um arquivo de imagem simulado
        avatar = self._get_valid_image_file()
        
        # Dados para atualização
        data = {
            'bio': 'This is my updated bio',
            'birth_date': '1990-01-01',
            'avatar': avatar
        }
        
        # Fazer a requisição
        response = self.client.put(
            self.user_update_profile_url(self.regular_user.id),
            data,
            format='multipart'
        )
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se o perfil foi atualizado
        profile = Profile.objects.get(user=self.regular_user)
        self.assertEqual(profile.bio, 'This is my updated bio')
        self.assertEqual(str(profile.birth_date), '1990-01-01')
        self.assertTrue('test_avatar' in profile.avatar.name)
    
    def test_change_password(self):
        """Testa a alteração de senha"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Dados para alteração de senha
        data = {
            'old_password': 'testpassword123',
            'new_password': 'newtestpassword123',
            'new_password2': 'newtestpassword123'
        }
        
        # Fazer a requisição
        response = self.client.post(self.user_change_password_url(self.regular_user.id), data)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a senha foi alterada
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.check_password('newtestpassword123'))
    
    def test_change_password_incorrect_old_password(self):
        """Testa a alteração de senha com senha antiga incorreta"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Dados para alteração de senha (senha antiga incorreta)
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newtestpassword123',
            'new_password2': 'newtestpassword123'
        }
        
        # Fazer a requisição
        response = self.client.post(self.user_change_password_url(self.regular_user.id), data)
        
        # Verificar a resposta (deve ser erro de validação)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verificar se a senha não foi alterada
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.check_password('testpassword123'))
    
    def test_me_endpoint(self):
        """Testa o endpoint 'me' para obter os detalhes do usuário autenticado"""
        # Autenticar como usuário regular
        self.client.force_authenticate(user=self.regular_user)
        
        # Fazer a requisição
        response = self.client.get(self.user_me_url)
        
        # Verificar a resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
    
    def test_me_endpoint_unauthenticated(self):
        """Testa o endpoint 'me' sem autenticação"""
        # Fazer a requisição sem autenticação
        response = self.client.get(self.user_me_url)
        
        # Verificar a resposta (deve ser negada)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
