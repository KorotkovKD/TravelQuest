from django.contrib import admin

from users.admin import ADMIN_SITE
from .models import (GameStage,
                     GameTask,
                     Task1,
                     Task2,
                     Task3,
                     Matches,
                     MatchesTask,
                     )


@admin.register(GameStage, site=ADMIN_SITE)
class TravelQuestGameStageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "location",
        "description",
    )
    search_fields = ("name", )
    empty_value_display = "-пусто-"


@admin.register(GameTask, site=ADMIN_SITE)
class TravelQuestGameTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "game_stage",
        "max_score",
        "question",
    )
    search_fields = ("game_stage", )
    empty_value_display = "-пусто-"


@admin.register(Task1, site=ADMIN_SITE)
class TravelQuestTask1Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "game_task",
        "answer_1",
        "answer_2",
        "answer_3",
        "answer_4",
        "correct_answer",
    )
    search_fields = ("game_task", )
    empty_value_display = "-пусто-"


@admin.register(Task2, site=ADMIN_SITE)
class TravelQuestTask3Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "game_task",
        "radius",
        "correct_answer",
    )
    search_fields = ("game_task", )
    empty_value_display = "-пусто-"


@admin.register(Task3, site=ADMIN_SITE)
class TravelQuestTask3Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "game_task",
        "picture_1",
        "picture_2",
        "picture_3",
        "picture_4",
        "description_1",
        "description_2",
        "description_3",
        "description_4",
        "correct_answer",
    )
    search_fields = ("game_task", )
    empty_value_display = "-пусто-"


@admin.register(Matches, site=ADMIN_SITE)
class TravelQuestMatchesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "game_stage",
        "user",
        "is_completed",
    )
    search_fields = ("game_stage", "user",)
    empty_value_display = "-пусто-"


@admin.register(MatchesTask, site=ADMIN_SITE)
class TravelQuestMatchesTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "matches",
        "game_task",
        "score",
    )
    search_fields = ("matches", "game_task",)
    empty_value_display = "-пусто-"
