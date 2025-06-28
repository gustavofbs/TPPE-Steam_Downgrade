from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO


from users.models import Profile

class RegisterViewTest(TestCase):
    """Testes para a view de registro"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
    
    def test_register_view_get(self):
        """Testa o acesso à página de registro (GET)"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
    
    def test_register_view_post_valid(self):
        """Testa o registro com dados válidos (POST)"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123'
        }
        response = self.client.post(self.register_url, data)
        
        # Verificar se o usuário foi criado
        self.assertEqual(User.objects.count(), 1)
        
        # Verificar se o perfil foi criado
        self.assertEqual(Profile.objects.count(), 1)
        
        # Verificar se foi redirecionado para a página de login
        self.assertRedirects(response, self.login_url)
    
    def test_register_view_post_invalid(self):
        """Testa o registro com dados inválidos (POST)"""
        data = {
            'username': 'testuser',
            'email': 'invalid_email',  # Email inválido
            'password1': 'password123',
            'password2': 'different_password'  # Senha não correspondente
        }
        response = self.client.post(self.register_url, data)
        
        # Verificar se a página de registro foi renderizada novamente
        self.assertEqual(response.status_code, 200)
        
        # Verificar se nenhum usuário foi criado
        self.assertEqual(User.objects.count(), 0)
        
        # Verificar se há erros no formulário
        form = response.context['form']
        self.assertIn('email', form.errors)
        self.assertIn('Enter a valid email address.', form.errors['email'])
        self.assertIn("The two password fields didn", form.errors['password2'][0])


class ProfileViewTest(TestCase):
    """Testes para a view de perfil"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        self.profile_url = reverse('users:profile')
        
        # Criar um usuário para os testes
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(
            username=self.username,
            email='test@example.com',
            password=self.password
        )
        
        # O perfil é criado automaticamente pelo signal
        self.profile = Profile.objects.get(user=self.user)
    
    def test_profile_view_not_authenticated(self):
        """Testa o acesso à página de perfil sem autenticação"""
        self.login_url = reverse('users:login')
        response = self.client.get(self.profile_url)
        
        login_url_with_next = f'{self.login_url}?next={self.profile_url}'
        self.assertRedirects(response, login_url_with_next)
    
    def test_profile_view_authenticated_get(self):
        """Testa o acesso à página de perfil com autenticação (GET)"""
        # Fazer login
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.get(self.profile_url)
        
        # Verificar se a página foi renderizada corretamente
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
    
    def test_profile_view_authenticated_post_valid(self):
        """Testa a atualização do perfil com dados válidos (POST)"""
        # Fazer login
        self.client.login(username=self.username, password=self.password)
        
        def _get_valid_image_file():
            image = Image.new('RGB', (100, 100), color='blue')
            buffer = BytesIO()
            image.save(buffer, format='JPEG')
            buffer.seek(0)
            return SimpleUploadedFile('test_avatar.jpg', buffer.read(), content_type='image/jpeg')

        avatar_mock = _get_valid_image_file()
        
        data = {
            'username': 'updated_username',
            'email': 'updated@example.com',
            'bio': 'This is a test bio',
            'birth_date': '1990-01-01',
            'avatar': avatar_mock
        }
        
        response = self.client.post(self.profile_url, data, format='multipart')
        
        # Verificar se foi redirecionado para a página de perfil
        self.assertRedirects(response, self.profile_url)
        
        # Verificar se o usuário foi atualizado
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated_username')
        self.assertEqual(self.user.email, 'updated@example.com')
        
        # Verificar se o perfil foi atualizado
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'This is a test bio')
        self.assertEqual(str(self.profile.birth_date), '1990-01-01')
        self.assertTrue('test_avatar' in self.profile.avatar.name)
    
    def test_profile_view_authenticated_post_invalid(self):
        """Testa a atualização do perfil com dados inválidos (POST)"""
        # Fazer login
        self.client.login(username=self.username, password=self.password)
        
        data = {
            'username': '',  # Nome de usuário vazio (inválido)
            'email': 'invalid_email',  # Email inválido
            'bio': 'This is a test bio',
            'birth_date': 'invalid_date',  # Data inválida
        }
        
        response = self.client.post(self.profile_url, data)
        
        # Verificar se a página de perfil foi renderizada novamente
        self.assertEqual(response.status_code, 200)
        
        # Verificar se o usuário não foi atualizado
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
