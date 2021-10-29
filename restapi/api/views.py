import time

from .forms import BloodTestForm
from .models import BloodTest
from django.shortcuts import render
from rest_framework import generics
from .serializers import BloodTestSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .parsers.gag_parser import parse_pdf
from django.core import exceptions
import threading


class BloodTestList(generics.ListCreateAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer

    def post(self, request, *args, **kwargs):
        blood_test_form = BloodTestForm(request.POST, request.FILES)
        if blood_test_form.is_valid():
            new_blood_test = BloodTest(client_ip=request.META['REMOTE_ADDR'],
                                       pdf_file_name=str(blood_test_form['pdf_file'].value()))
            new_blood_test.save()
            threading.Thread(target=parsing_function,
                             args=(blood_test_form['pdf_file'].value(), new_blood_test)).start()
            return HttpResponse(new_blood_test.id)
        raise exceptions.BadRequest()


def parsing_function(file, test):
    test.parsing_result = parse_pdf(file)
    test.parsing_completed = True
    test.save()


class BloodTestDetail(generics.RetrieveAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer


@csrf_exempt
def blood_test_detail(request):
    if request.method == 'POST':
        blood_test_form = BloodTestForm(request.POST, request.FILES)
        if blood_test_form.is_valid():
            return HttpResponse(parse_pdf(blood_test_form['pdf_file'].value()))
        raise exceptions.BadRequest()
    else:
        blood_test_form = BloodTestForm()
        return render(request, 'test_form.html', {'form': blood_test_form, 'error': blood_test_form})
