from .forms import BloodTestForm
from .models import BloodTest
from django.shortcuts import render
from rest_framework import generics
from .serializers import BloodTestSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .parsers.gag_parser import parse_pdf


class BloodTestList(generics.ListAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer


class BloodTestDetail(generics.RetrieveAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer


@csrf_exempt
def blood_test_detail(request):
    if request.method == 'POST':
        blood_test_form = BloodTestForm(request.POST, request.FILES)
        if blood_test_form.is_valid():
            new_blood_test = BloodTest(user=blood_test_form['user'].value(),
                                       pdf_file_name=str(blood_test_form['pdf_file'].value()),
                                       parsing_result=parse_pdf(blood_test_form['pdf_file'].value()))
            new_blood_test.save()
            return HttpResponse(new_blood_test.id)
        return HttpResponse('The file isn\'t PDF')
    else:
        blood_test_form = BloodTestForm()
        return render(request, 'test_form.html', {'form': blood_test_form, 'error': blood_test_form})
