from .models import PDFFile
from rest_framework import generics
from . import serializers


class PDFFileList(generics.ListCreateAPIView):
    queryset = PDFFile.objects.all()
    serializer_class = serializers.PDFFileSerializer


class PDFFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PDFFile.objects.all()
    serializer_class = serializers.PDFFileSerializer
