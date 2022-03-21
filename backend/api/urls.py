from django.urls import path

from .api_scheme import schema_view
from .auth import CustomAuthToken

urlpatterns = [
    path(r'docs/^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth-token/', CustomAuthToken.as_view(), name='token-auth')
]