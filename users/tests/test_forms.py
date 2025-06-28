from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
from datetime import date

from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile

from PIL import Image
from io import BytesIO


class UserRegisterFormTest(TestCase):
    """Testes para o formulário de registro de usuário"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.password = 'SuperSafePassword123!'
    
    def test_register_form_valid_data(self):
        """Testa o formulário de registro com dados válidos"""
        form_data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_register_form_invalid_data(self):
        """Testa o formulário de registro com dados inválidos"""
        # Senha não correspondente
        form_data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': 'different_password'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        # Email inválido
        form_data = {
            'username': self.username,
            'email': 'invalid_email',
            'password1': self.password,
            'password2': self.password
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_register_form_duplicate_username(self):
        """Testa o formulário de registro com nome de usuário duplicado"""
        # Criar um usuário com o mesmo nome de usuário
        User.objects.create_user(
            username=self.username,
            email='another@example.com',
            password='anotherpassword'
        )
        
        # Tentar registrar outro usuário com o mesmo nome de usuário
        form_data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_register_form_duplicate_email(self):
        """Testa o formulário de registro com email duplicado"""
        # Criar um usuário com o mesmo email
        User.objects.create_user(
            username='another_user',
            email=self.email,
            password='anotherpassword'
        )
        
        # Tentar registrar outro usuário com o mesmo email
        form_data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class UserUpdateFormTest(TestCase):
    """Testes para o formulário de atualização de usuário"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
    
    def test_update_form_valid_data(self):
        """Testa o formulário de atualização com dados válidos"""
        form_data = {
            'username': 'updated_username',
            'email': 'updated@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_update_form_duplicate_username(self):
        """Testa o formulário de atualização com nome de usuário duplicado"""
        # Criar outro usuário com um nome de usuário diferente
        User.objects.create_user(
            username='another_user',
            email='another@example.com',
            password='anotherpassword'
        )
        
        # Tentar atualizar para um nome de usuário já existente
        form_data = {
            'username': 'another_user',
            'email': 'updated@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

class ProfileUpdateFormTest(TestCase):
    """Testes para o formulário de atualização de perfil"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.profile = Profile.objects.get(user=self.user)

    def _get_valid_image_file(self):
        image = Image.new('RGB', (100, 100), color='blue')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        buffer.seek(0)
        return SimpleUploadedFile('test.jpg', buffer.read(), content_type='image/jpeg')
    
    def test_profile_update_form_valid_data(self):
        """Testa o formulário de atualização de perfil com dados válidos"""
        # Criar um arquivo de imagem simulado
        avatar_mock = self._get_valid_image_file()
        
        form_data = {
            'bio': 'This is a test bio',
            'birth_date': '1990-01-01',
            'avatar': avatar_mock
        }
        form = ProfileUpdateForm(data=form_data, files={'avatar': avatar_mock}, instance=self.profile)
        print(form.errors)
        self.assertTrue(form.is_valid())
    
    def test_profile_update_form_invalid_date(self):
        """Testa o formulário de atualização de perfil com data inválida"""
        form_data = {
            'bio': 'This is a test bio',
            'birth_date': 'invalid_date',  # Data inválida
        }
        form = ProfileUpdateForm(data=form_data, instance=self.profile)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)
    
    def test_profile_update_form_future_date(self):
        """Testa o formulário de atualização de perfil com data futura"""
        # Data no futuro
        future_date = datetime.date.today() + datetime.timedelta(days=10)
        
        form_data = {
            'bio': 'This is a test bio',
            'birth_date': future_date.strftime('%Y-%m-%d'),
        }
        form = ProfileUpdateForm(data=form_data, instance=self.profile)
        
        # O Django não valida automaticamente se a data de nascimento está no futuro
        # Em um sistema real, você poderia adicionar essa validação personalizada
        self.assertTrue(form.is_valid())
