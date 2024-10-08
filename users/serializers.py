from rest_framework import serializers


from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор профиля"""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "tg_chat_id",
        )


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации"""

    class Meta:
        model = User
        fields = ["id", "email", "tg_chat_id", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            tg_chat_id=validated_data["tg_chat_id"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class PasswordUpdateSerializer(serializers.Serializer):
    """Сериализатор для смены пароля"""

    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
