from rest_framework import serializers
from .models import  Content,UserInteraction,User

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'display_name', 'bio', 'avatar', 'date_of_birth', 'location',
            'interests', 'email_notifications', 'push_notifications'
        ]

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'display_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            display_name=validated_data.get('display_name', ''),
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'display_name', 'bio', 'avatar',
            'date_of_birth', 'location', 'interests', 'is_premium',
            'onboarding_complete', 'last_active', 'followers', 'following',
            'email_notifications', 'push_notifications', 'metadata',
        ]
        read_only_fields = ['id', 'last_active', 'followers', 'following']
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields ='__all__'
class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = '__all__'