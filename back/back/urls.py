from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("movies/", include("movies.urls")),
    path("actors/", include("actors.urls")),
    path("articles/", include("articles.urls")),
    path("api-auth/", include('rest_framework.urls')),
    path("accounts/", include("dj_rest_auth.urls")),
    path("accounts/signup/", include("dj_rest_auth.registration.urls")),
    path("user/", include("accounts.urls")),
    path("auth/", include("allauth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
