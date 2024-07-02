from django.db import models

from users.models import User


class GameStage(models.Model):

    name = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name="Имя станции",
    )
    location = models.CharField(
        max_length=64,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Местоположение точки",
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name="Описание станции",
    )

    class Meta:
        verbose_name = "Игровая станция",
        verbose_name_plural = "Игровые станции",
        indexes = (
            models.Index(fields=("location", ), name="location_idx"),
        )
        ordering = ("-id", )

    def __str__(self) -> str:
        return self.name


class GameTask(models.Model):

    game_stage = models.ForeignKey(
        GameStage,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Игровая станция",
        related_name="belonging_to",
    )
    max_score = models.PositiveSmallIntegerField(
        verbose_name="Максимальная награда",
        null=False,
        blank=False,
    )
    question = models.TextField(
        null=False,
        blank=False,
        verbose_name="Вопрос задания",
    )

    class Meta:
        verbose_name = "Игровое задание",
        verbose_name_plural = "Игровые задания",
        indexes = (
            models.Index(fields=("game_stage", ), name="game_stage_idx"),
        )
        ordering = ("-id", )

    def __str__(self) -> str:
        return self.question


class Task1(models.Model):

    game_task = models.ForeignKey(
        GameTask,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Игровое задание",
        related_name="first_category_of",
    )
    answer_1 = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name="Ответ 1",
    )
    answer_2 = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name="Ответ 2",
    )
    answer_3 = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name="Ответ 3",
    )
    answer_4 = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name="Ответ 4",
    )
    correct_answer = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        verbose_name="Правильный ответ",
    )

    class Meta:
        verbose_name = "Задание 1-го типа",
        verbose_name_plural = "Задания 1-го типа",
        indexes = (
            models.Index(fields=("game_task", ), name="game_task1_idx"),
        )
        ordering = ("-id", )

    def __str__(self) -> str:
        return str(self.correct_answer)


class Task2(models.Model):

    game_task = models.ForeignKey(
        GameTask,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Игровое задание",
        related_name="second_category_of",
    )
    correct_answer = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        verbose_name="Правильный ответ",
    )
    radius = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        verbose_name="Интервал ответов",
    )

    class Meta:
        verbose_name = "Задание 2-го типа",
        verbose_name_plural = "Задания 2-го типа",
        indexes = (
            models.Index(fields=("game_task", ), name="game_task2_idx"),
        )
        ordering = ("-id", )

    def __str__(self) -> str:
        return str(self.correct_answer)


class Task3(models.Model):

    game_task = models.ForeignKey(
        GameTask,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Игровое задание",
        related_name="third_category_of",
    )
    picture_1 = models.ImageField(
        null=False,
        blank=False,
        verbose_name="Картинка 1",
        upload_to="quests/images/",
    )
    picture_2 = models.ImageField(
        null=False,
        blank=False,
        verbose_name="Картинка 2",
        upload_to="quests/images/",
    )
    picture_3 = models.ImageField(
        null=False,
        blank=False,
        verbose_name="Картинка 3",
        upload_to="quests/images/",
    )
    picture_4 = models.ImageField(
        null=False,
        blank=False,
        verbose_name="Картинка 4",
        upload_to="quests/images/",
    )
    description_1 = models.CharField(
        max_length=512,
        null=False,
        blank=False,
        verbose_name="Описание 1",
    )
    description_2 = models.CharField(
        max_length=512,
        null=False,
        blank=False,
        verbose_name="Описание 2",
    )
    description_3 = models.CharField(
        max_length=512,
        null=False,
        blank=False,
        verbose_name="Описание 3",
    )
    description_4 = models.CharField(
        max_length=512,
        null=False,
        blank=False,
        verbose_name="Описание 4",
    )
    correct_answer = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        verbose_name="Правильный ответ",
    )

    class Meta:
        verbose_name = "Задание 3-го типа",
        verbose_name_plural = "Задания 3-го типа",
        indexes = (
            models.Index(fields=("game_task", ), name="game_task3_idx"),
        )
        ordering = ("-id", )

    def __str__(self) -> str:
        return str(self.correct_answer)


class Matches(models.Model):

    game_stage = models.ForeignKey(
        GameStage,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Игровая станция",
        related_name="played_at",
    )
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Игрок",
        related_name="played_by",
    )
    is_completed = models.BooleanField(
        null=True,
        blank=False,
        default=False,
        verbose_name="Статус",
    )

    class Meta:
        verbose_name = "Игровой матч",
        verbose_name_plural = "Игровые матчи",
        indexes = (
            models.Index(fields=("user", ), name="match_user_idx"),
        )
        ordering = ("-id", )


class MatchesTask(models.Model):

    game_task = models.ForeignKey(
        GameTask,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Матч задания",
        related_name="part_of",
    )
    matches = models.ForeignKey(
        Matches,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Матч задания",
        related_name="part_of",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Заработанная награда",
        null=True,
        blank=False,
        default=0
    )

    class Meta:
        verbose_name = "Задание матча",
        verbose_name_plural = "Задания матча",
        indexes = (
            models.Index(fields=("matches", ),
                         name="matches_idx"),
        )
        ordering = ("-id", )

    def __str__(self) -> str:
        return str(self.score)
