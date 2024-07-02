from django.urls import include, path

from users.admin import ADMIN_SITE


urlpatterns = (
    path("users/", include("users.urls")),
    path("admin/", ADMIN_SITE.urls),
    path("api/", include("api.urls")),
)
