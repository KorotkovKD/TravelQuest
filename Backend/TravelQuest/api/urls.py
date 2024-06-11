from django.urls import include, path

from .views import login


app_name = 'api'


urlpatterns = (
    path("v1/users/login/", login),
)
