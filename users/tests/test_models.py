from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import Profile

class ProfileModelTest(TestCase):
    """Testes para o modelo Profile"""
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        # O perfil é criado automaticamente pelo signal
        self.profile = Profile.objects.get(user=self.user)
    
    def test_profile_creation(self):
        """Testa se um perfil é criado automaticamente quando um usuário é criado"""
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.bio, '')
        self.assertIsNone(self.profile.birth_date)
        self.assertEqual(self.profile.avatar, 'default_avatar.png')
    
    def test_profile_string_representation(self):
        """Testa a representação em string de um perfil"""
        expected_string = f'{self.user.username} Profile'
        self.assertEqual(str(self.profile), expected_string)
    
    def test_profile_update(self):
        """Testa a atualização de um perfil"""
        # Atualizar campos do perfil
        self.profile.bio = 'This is a test bio'
        self.profile.save()
        
        # Recuperar o perfil atualizado
        updated_profile = Profile.objects.get(id=self.profile.id)
        self.assertEqual(updated_profile.bio, 'This is a test bio')
    
    def test_profile_avatar_upload(self):
        """Testa o upload de avatar para um perfil"""
        # Criar um arquivo de imagem simulado
        avatar_mock = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        
        # Atualizar o avatar
        self.profile.avatar = avatar_mock
        self.profile.save()
        
        # Verificar se o avatar foi atualizado
        updated_profile = Profile.objects.get(id=self.profile.id)
        self.assertTrue('test_avatar' in updated_profile.avatar.name)
    
    def test_user_profile_relationship(self):
        """Testa o relacionamento entre usuário e perfil"""
        # Verificar se o usuário tem acesso ao perfil
        self.assertEqual(self.user.profile, self.profile)
        
        # Verificar se o perfil tem acesso ao usuário
        self.assertEqual(self.profile.user, self.user)
    
    def test_profile_signal_on_user_update(self):
        """Testa se o perfil é atualizado quando o usuário é atualizado"""
        # Atualizar o nome de usuário
        self.user.username = 'updated_username'
        self.user.save()
        
        # Verificar se o perfil ainda está associado ao usuário atualizado
        updated_profile = Profile.objects.get(id=self.profile.id)
        self.assertEqual(updated_profile.user.username, 'updated_username')
    
    def test_profile_deletion_on_user_deletion(self):
        """Testa se o perfil é excluído quando o usuário é excluído"""
        # Armazenar o ID do perfil
        profile_id = self.profile.id
        
        # Excluir o usuário
        self.user.delete()
        
        # Verificar se o perfil foi excluído
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(id=profile_id)
