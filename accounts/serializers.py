from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['rol', 'rol_display', 'avatar', 'telefono', 'departamento', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'is_staff', 'is_active', 'profile']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

    def update(self, instance, validated_data):
        # Handle nested update for user profile fields
        request = self.context.get('request')
        if request and 'profile' in request.data:
            profile_data = request.data.get('profile', {})
            profile = instance.profile
            profile.rol = profile_data.get('rol', profile.rol)
            profile.telefono = profile_data.get('telefono', profile.telefono)
            profile.departamento = profile_data.get('departamento', profile.departamento)
            
            # If a new avatar file is provided
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            elif 'avatar' in profile_data and profile_data['avatar'] is None:
                profile.avatar = None
                
            profile.save()

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        
        # Admin can toggle is_staff
        if instance.profile.rol == UserProfile.Rol.ADMIN:
            instance.is_staff = True
        elif instance.profile.rol == UserProfile.Rol.GESTOR:
            instance.is_staff = True
        else:
            instance.is_staff = False
            
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    rol = serializers.ChoiceField(choices=UserProfile.Rol.choices, default=UserProfile.Rol.USUARIO, write_only=True)
    telefono = serializers.CharField(max_length=20, required=False, allow_blank=True, write_only=True)
    departamento = serializers.CharField(max_length=100, required=False, allow_blank=True, write_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'rol', 'telefono', 'departamento']

    def create(self, validated_data):
        rol = validated_data.pop('rol', UserProfile.Rol.USUARIO)
        telefono = validated_data.pop('telefono', '')
        departamento = validated_data.pop('departamento', '')
        password = validated_data.pop('password')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        
        # Set is_staff based on role
        if rol in [UserProfile.Rol.ADMIN, UserProfile.Rol.GESTOR]:
            user.is_staff = True
            
        user.save()

        # The profile is automatically created by signals, so we retrieve and update it
        profile = user.profile
        profile.rol = rol
        profile.telefono = telefono
        profile.departamento = departamento
        profile.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})
