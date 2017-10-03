from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import User

from rest_framework.views import APIView
from rest_framework.response import Response


def index(request):
    nomes = User.objects.filter(pk=1)
    first_name = User.objects.values_list('first_name', flat=True).filter(pk=2)
    context = {
        'first_name': first_name,
    }
    return render(request, 'dashboard/index.html', context)


def detail(request, cliente_id):
    try:
        question = User.objects.get(pk=cliente_id)
    except User.DoesNotExist:
        raise Http404("Cliente does not exist")
    return render(request, 'dashboard/detail.html', {'question': question})


def results(request, cliente_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % cliente_id)


@login_required
def graficos(request):
    first_name = User.objects.values_list('first_name', flat=True).filter(pk=2)
    last_name = User.objects.values_list('last_name', flat=True).filter(pk=2)
    context = {
        'last_name': last_name,
        'first_name': first_name,
    }
    return render(request, 'dashboard/graficos.html', context)


def do_login(request):
    # return render(request, 'dashboard/home.html')
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/graficos')
    return render(request, 'dashboard/login.html')


def do_logout(request):
    # return render(request, 'dashboard/logout.html')
    logout(request)
    return redirect('/login')


def departamentos_json(request, *args, **kargs):
    # Substituiremos pelos dados do banco (models), isso é apenas demonstração
    data = [
        {'value': 70, 'label': 'Industria'},
        {'value': 15, 'label': 'Oficina'},
        {'value': 10, 'label': 'Suprimento'},
        {'value': 5, 'label': 'Outros Departamentos'}
    ]
    return JsonResponse(data, safe=False)


def transdutores_json(request, *args, **kargs):
    # Substituiremos pelos dados do banco (models), isso é apenas demonstração
    data = [
        {'Hora': '00:00', 't1': 51, 't2': 55, 't3': 31, 't4': 66},
        {'Hora': '01:00', 't1': 51, 't2': 55, 't3': 33, 't4': 67},
        {'Hora': '02:00', 't1': 50, 't2': 40, 't3': 33, 't4': 67},
        {'Hora': '03:00', 't1': 53, 't2': 55, 't3': 23, 't4': 68},
        {'Hora': '04:00', 't1': 50, 't2': 40, 't3': 39, 't4': 68},
        {'Hora': '05:00', 't1': 53, 't2': 55, 't3': 44, 't4': 60},
        {'Hora': '06:00', 't1': 44, 't2': 55, 't3': 44, 't4': 71},
        {'Hora': '07:00', 't1': 56, 't2': 55, 't3': 41, 't4': 71},
        {'Hora': '08:00', 't1': 44, 't2': 65, 't3': 41, 't4': 75},
        {'Hora': '09:00', 't1': 44, 't2': 65, 't3': 41, 't4': 81},
        {'Hora': '10:00', 't1': 48, 't2': 65, 't3': 41, 't4': 87},
        {'Hora': '11:00', 't1': 49, 't2': 72, 't3': 41, 't4': 87},
        {'Hora': '12:00', 't1': 55, 't2': 72, 't3': 42, 't4': 92},
        {'Hora': '13:00', 't1': 55, 't2': 73, 't3': 41, 't4': 92},
        {'Hora': '14:00', 't1': 55, 't2': 74, 't3': 33, 't4': 95},
        {'Hora': '15:00', 't1': 66, 't2': 75, 't3': 31, 't4': 97},
        {'Hora': '16:00', 't1': 55, 't2': 88, 't3': 31, 't4': 99},
        {'Hora': '17:00', 't1': 55, 't2': 88, 't3': 25, 't4': 99},
        {'Hora': '18:00', 't1': 55, 't2': 89, 't3': 25, 't4': 99},
        {'Hora': '19:00', 't1': 65, 't2': 77, 't3': 25, 't4': 100},
        {'Hora': '20:00', 't1': 67, 't2': 76, 't3': 24, 't4': 100},
        {'Hora': '21:00', 't1': 77, 't2': 76, 't3': 24, 't4': 100},
        {'Hora': '22:00', 't1': 75, 't2': 75, 't3': 21, 't4': 100},
        {'Hora': '23:00', 't1': 82, 't2': 65, 't3': 21, 't4': 100},
        {'Hora': '24:00', 't1': 85, 't2': 65, 't3': 19, 't4': 100}
    ]
    return JsonResponse(data, safe=False)


class horarios_rest(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # Substituiremos pelos dados do banco (models), isso é apenas demonstração
        data = [
            {'ano': '2016', 'ponta': 24, 'normal': 76},
            {'ano': '2017', 'ponta': 13, 'normal': 87},
        ]
        return Response(data)
