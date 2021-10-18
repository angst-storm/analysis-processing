from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('pdfFiles/', views.PDFFileList.as_view()),
    path('pdfFiles/<int:pk>/', views.PDFFileDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
