from .forms import BloodTestForm
from .models import BloodTest
from django.shortcuts import render
from rest_framework import generics
from .serializers import BloodTestSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import exceptions
from threading import Thread
from rest_framework.renderers import JSONRenderer


def parsing_function(blood_test):
    blood_test.launch_parsing()
    blood_test.remove_file()
    blood_test.save()


class BloodTestList(generics.ListCreateAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer

    def post(self, request, *args, **kwargs):
        blood_test_form = BloodTestForm(request.POST, request.FILES)
        if blood_test_form.is_valid():
            new_blood_test = BloodTest(client_ip=request.META['REMOTE_ADDR'],
                                       client_file=blood_test_form['client_file'].value())
            new_blood_test.save()
            Thread(target=parsing_function, args=(new_blood_test,)).start()
            # parsing_function(new_blood_test)
            return HttpResponse(JSONRenderer().render({'id': new_blood_test.id}))
        raise exceptions.BadRequest()


class BloodTestDetail(generics.RetrieveAPIView):
    queryset = BloodTest.objects.all()
    serializer_class = BloodTestSerializer


@csrf_exempt
def blood_test_detail(request):
    if request.method == 'POST':
        blood_test_form = BloodTestForm(request.POST, request.FILES)
        if blood_test_form.is_valid():
            new_blood_test = BloodTest(client_ip=request.META['REMOTE_ADDR'],
                                       client_file=blood_test_form['client_file'].value())
            new_blood_test.save()
            parsing_function(new_blood_test)
            return HttpResponse(JSONRenderer().render(BloodTestSerializer(new_blood_test).data))
        raise exceptions.BadRequest()
    else:
        return render(request, 'form.html')
