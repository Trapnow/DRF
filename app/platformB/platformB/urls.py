from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Polls API",
        default_version='v1',
        description="Polls application documentation",
        permission_classes=[],
    ),
    public=True
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("swagger.<format>/", schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("api/users/", include("users.urls")),
    path("api/", include("project.urls")),
    path('api/api/v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

