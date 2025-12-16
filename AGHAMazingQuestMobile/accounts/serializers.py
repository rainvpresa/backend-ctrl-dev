from rest_framework import serializers
from .models import User


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
