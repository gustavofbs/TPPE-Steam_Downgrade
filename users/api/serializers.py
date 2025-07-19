from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Profile"""
    
    def to_representation(self, instance):
        """Customiza a representação para incluir avatar como URL absoluta"""
        data = super().to_representation(instance)
        # Converter avatar para URL absoluta
        if instance.avatar:
            request = self.context.get('request')
            if request:
                # Sempre usar build_absolute_uri para garantir URL completa
                data['avatar'] = request.build_absolute_uri(instance.avatar.url)
            else:
                # Fallback se não houver request no context
                avatar_url = instance.avatar.url
                if not avatar_url.startswith('http'):
                    # Se não é uma URL completa, adicionar o domínio padrão
                    data['avatar'] = f"http://localhost:8000{avatar_url}"
                else:
                    data['avatar'] = avatar_url
        else:
            data['avatar'] = None
        return data
    
    def update(self, instance, validated_data):
        """Customiza o update para ignorar avatar se for string (base64 ou URL)"""
        avatar_data = validated_data.get('avatar')
        
        # Se avatar é uma string (base64 ou URL), ignorar para evitar erro de validação
        if avatar_data and isinstance(avatar_data, str):
            # Ignorar dados de avatar que são strings (base64, URLs, etc)
            validated_data.pop('avatar', None)
        
        return super().update(instance, validated_data)
    
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
