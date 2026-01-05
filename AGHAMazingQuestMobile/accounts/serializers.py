from rest_framework import serializers
from .models import User
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "display_name", "email", "scores", "avatar", "avatar_url", "created_at", "updated_at")

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=10)

class CustomLoginSerializer(LoginSerializer):
    # Accept email as the main login field
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        # Copy email into username for allauth
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)
    