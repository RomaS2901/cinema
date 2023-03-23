from rest_framework import serializers

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )
        write_only_fields = ("password",)
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


# noinspection PyAbstractClass
class LoginInputSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
