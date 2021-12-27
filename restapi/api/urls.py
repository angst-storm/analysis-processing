from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.blood_test_detail, name='blood_test_detail'),
    path('blood-tests/', views.BloodTestList.as_view()),
    path('blood-tests/<int:pk>/', views.BloodTestDetail.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

urlpatterns = format_suffix_patterns(urlpatterns)
