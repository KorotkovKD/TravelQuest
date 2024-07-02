import base64
import random

from django.contrib.auth import password_validation
from django.core.files.base import ContentFile
from rest_framework import serializers

from users.models import User
from quests.models import (Matches, GameTask,
                           GameStage, MatchesTask)
from .constants import TASKS


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("email", "password",)
        model = User

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        user = User.objects.create(
               email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)
    current_password = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if user.check_password(value):
            return value
        raise serializers.ValidationError("Старый пароль неверен.")

    def validate_new_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except ValueError:
            raise serializers.ValidationError
        return value

    def save(self, **kwargs):
        password = self.validated_data["new_password"]
        user = self.context["request"].user
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)
    bio = serializers.CharField(required=False)
    balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ("email", "photo", "bio", "balance", )
        read_only_fields = ("email", "balance", )
        model = User

    def get_balance(self, obj):
        return obj.owned_by.value


class MatchesSerializer(serializers.ModelSerializer):
    current_location = serializers.CharField(required=True,
                                             write_only=True)
    game_stage = serializers.SlugRelatedField(
        queryset=GameStage.objects.all(),
        slug_field="id",
    )

    class Meta:
        fields = ("id", "game_stage", "user", "current_location", "is_completed", )
        read_only_fields = ("id", "is_completed", "user")
        model = Matches

    def validate_current_location(self, value):
        return True

    def create(self, validated_data):
        game_stage = validated_data["game_stage"]
        matches = Matches.objects.create(
                  game_stage=game_stage,
                  user=self.context["request"].user

                  )
        matches.save()
        for task in TASKS:
            task_list = list(GameTask.objects.filter(game_stage=game_stage,
                                                     id__in=task.objects.values_list('id', flat=True)))
            game_task = task_list.pop(random.randrange(len(task_list)))
            MatchesTask.objects.create(g=matches, game_task=game_task)

        return matches


class MatchesAnswersSerializer(serializers.Serializer):
    answer_1 = serializers.CharField()
    answer_2 = serializers.CharField()
    answer_3 = serializers.CharField()

    def validate_answer_1(self, value):
        return True

    def validate_answer_2(self, value):
        return True

    def validate_answer_3(self, value):
        return True
