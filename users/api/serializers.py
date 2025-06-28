from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Profile"""
    
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'avatar']
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User (somente leitura)"""
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'date_joined', 'is_active']
        read_only_fields = ['date_joined', 'is_active']

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar usuários"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, attrs):
        """Validar se as senhas correspondem"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não correspondem."})
        return attrs
    
    def create(self, validated_data):
        """Criar um novo usuário"""
        # Remover password2 dos dados validados
        validated_data.pop('password2')
        
        # Criar o usuário
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # O perfil é criado automaticamente pelo signal
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualizar usuários (sem senha)"""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def validate_email(self, value):
        """Validar se o email já está em uso por outro usuário"""
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value
    
    def validate_username(self, value):
        """Validar se o nome de usuário já está em uso por outro usuário"""
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        return value

class PasswordChangeSerializer(serializers.Serializer):
    """Serializer para alterar a senha"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validar se as novas senhas correspondem"""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "As senhas não correspondem."})
        return attrs
