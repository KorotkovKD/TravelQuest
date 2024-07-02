from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (change_password,
                    login,
                    logout,
                    profile,
                    registration,
                    MatchesViewSet)


app_name = "api"

router_v1 = SimpleRouter()
router_v1.register("matches", MatchesViewSet, basename="matches")

urlpatterns = (
    path("v1/", include(router_v1.urls)),
    path("v1/users/", registration),
    path("v1/users/login/", login),
    path("v1/users/logout/", logout),
    path("v1/users/profile/", profile),
    path("v1/users/change_password/", change_password),
)
