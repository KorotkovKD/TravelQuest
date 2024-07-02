from django.urls import include, path

from .views import activate

app_name = "users"


urlpatterns = (
    path('activate/<uidb64>/<token>', activate, name='activate'),
)
