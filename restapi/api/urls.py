from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # re_path(r'^swagger(?P\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', views.blood_test_detail, name='blood_test_detail'),
    path('blood-tests/', views.BloodTestList.as_view()),
    path('blood-tests/<int:pk>/', views.BloodTestDetail.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

urlpatterns = format_suffix_patterns(urlpatterns)
