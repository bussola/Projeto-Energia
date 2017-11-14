from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .models import User, Coleta

from rest_framework.views import APIView
from rest_framework.response import Response

from dashboard.devicewise.DevicewiseHttp import DevicewiseHttp


def my_custom_bad_request_view(request):
    return render(request, '400.html', )
 
def my_custom_permission_denied_view(request):
    return render(request, '403.html', )
 
def my_custom_page_not_found_view(request):
    return render(request, '404.html', )
 
def my_custom_error_view(request):
    return render(request, '500.html', )

def index(request):
    nomes = User.objects.filter(pk=1)
    first_name = User.objects.values_list('first_name', flat=True).filter(pk=2)
    context = {
        'first_name': first_name,
    }
    return render(request, 'dashboard/index.html', context)


# def detail(request, cliente_id):
#     try:
#         question = User.objects.get(pk=cliente_id)
#     except User.DoesNotExist:
#         raise Http404("Cliente does not exist")
#     return render(request, 'dashboard/detail.html', {'question': question})


# def results(request, cliente_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % cliente_id)


@login_required
def graficos(request):
    first_name = User.objects.values_list('first_name', flat=True).filter(pk=2)
    last_name = User.objects.values_list('last_name', flat=True).filter(pk=2)
    date_joined = User.objects.values_list('date_joined', flat=True).filter(pk=2)
    context = {
        'last_name': last_name,
        'first_name': first_name,
        'date_joined': date_joined,
    }
    return render(request, 'dashboard/graficos.html', context)


def do_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return render(request, 'dashboard/graficos.html')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if request.POST.get('lembrar', None) is not None:
                request.session.set_expiry(
                    60 * 60 * 24 * 30 * 12)  # Se selecionar o "lembrar-me" ficará logado por 1 ano
            login(request, user)
            return redirect('/graficos')
    return render(request, 'dashboard/login.html')


def do_logout(request):
    # return render(request, 'dashboard/logout.html')
    logout(request)
    return redirect('/login')


def consumo_mensal(request, *args, **kargs):
    data1 = [
        {'Dia': '01', 'Consumo': 51333},
        {'Dia': '02', 'Consumo': 30222},
        {'Dia': '03', 'Consumo': 20442},
        {'Dia': '04', 'Consumo': 20123},
        {'Dia': '05', 'Consumo': 32333},
        {'Dia': '06', 'Consumo': 44963},
        {'Dia': '07', 'Consumo': 42124},
        {'Dia': '08', 'Consumo': 52322},
        {'Dia': '09', 'Consumo': 62223},
        {'Dia': '10', 'Consumo': 82111},
        {'Dia': '11', 'Consumo': 92223},
        {'Dia': '12', 'Consumo': 92099},
        {'Dia': '13', 'Consumo': 82724},
        {'Dia': '14', 'Consumo': 66875},
        {'Dia': '15', 'Consumo': 42312},
        {'Dia': '16', 'Consumo': 32222},
        {'Dia': '17', 'Consumo': 22222},
        {'Dia': '18', 'Consumo': 12222},
        {'Dia': '19', 'Consumo': 32222},
        {'Dia': '20', 'Consumo': 42222},
        {'Dia': '21', 'Consumo': 52222},
        {'Dia': '22', 'Consumo': 62222},
        {'Dia': '23', 'Consumo': 72222},
        {'Dia': '24', 'Consumo': 72222},
        {'Dia': '25', 'Consumo': 62222},
        {'Dia': '26', 'Consumo': 52222},
        {'Dia': '27', 'Consumo': 42222},
        {'Dia': '28', 'Consumo': 32222},
        {'Dia': '29', 'Consumo': 22222},
        {'Dia': '30', 'Consumo': 12222},
        {'Dia': '31', 'Consumo': 12222},
    ]
    return JsonResponse(data1, safe=False)


def consumo_mensal_por_setores(request, *args, **kargs):
    data2 = [
        {'value': 2554, 'label': 'Industria'},
        {'value': 242, 'label': 'Oficina'},
        {'value': 3233, 'label': 'Suprimento'},
        {'value': 122, 'label': 'Outros Departamentos'}
    ]
    return JsonResponse(data2, safe=False)


def gasto_mensal(request, *args, **kargs):
    data3 = [
        {'Dia': '01', 'Valor': 51333},
        {'Dia': '02', 'Valor': 30222},
        {'Dia': '03', 'Valor': 20442},
        {'Dia': '04', 'Valor': 20123},
        {'Dia': '05', 'Valor': 32333},
        {'Dia': '06', 'Valor': 44963},
        {'Dia': '07', 'Valor': 42124},
        {'Dia': '08', 'Valor': 52322},
        {'Dia': '09', 'Valor': 62223},
        {'Dia': '10', 'Valor': 82111},
        {'Dia': '11', 'Valor': 92223},
        {'Dia': '12', 'Valor': 92099},
        {'Dia': '13', 'Valor': 82724},
        {'Dia': '14', 'Valor': 66875},
        {'Dia': '15', 'Valor': 42312},
        {'Dia': '16', 'Valor': 32222},
        {'Dia': '17', 'Valor': 22222},
        {'Dia': '18', 'Valor': 12222},
        {'Dia': '19', 'Valor': 32222},
        {'Dia': '20', 'Valor': 42222},
        {'Dia': '21', 'Valor': 52222},
        {'Dia': '22', 'Valor': 62222},
        {'Dia': '23', 'Valor': 72222},
        {'Dia': '24', 'Valor': 72222},
        {'Dia': '25', 'Valor': 62222},
        {'Dia': '26', 'Valor': 52222},
        {'Dia': '27', 'Valor': 42222},
        {'Dia': '28', 'Valor': 32222},
        {'Dia': '29', 'Valor': 22222},
        {'Dia': '30', 'Valor': 12222},
        {'Dia': '31', 'Valor': 12222},
    ]
    return JsonResponse(data3, safe=False)


def gasto_mensal_por_setores(request, *args, **kargs):
    data = [
        {'value': 12.22, 'label': 'Industria'},
        {'value': 15.32, 'label': 'Oficina'},
        {'value': 12.12, 'label': 'Suprimento'},
        {'value': 51.30, 'label': 'Outros Departamentos'}
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


@csrf_exempt
def api_login(request):
    api = DevicewiseHttp()
    info = api.debugar()
    return HttpResponse(info)


@csrf_exempt
def coleta_exemplo(request):
    return render(request, 'dashboard/coleta_exemplo.html')


@csrf_exempt
def por_canal_exemplo(request):
    return render(request, 'dashboard/coleta_por_canal_exemplo.html')


@csrf_exempt
def api_coletar(request, *args, **kwargs):
    # Coletando dados da API
    thing_key = 'hab0001'  # Essa informacao deve estar no cadastro dele
    api = DevicewiseHttp()
    dados = api.coletar(thing_key)
    print(dados)
    '''
      coleta = Coleta()
      coleta.canal1 = 'io_6'
      coleta.canal2 = 'io_7'
      coleta.canal3 = 'io_8'
      coleta.canal4 = 'io_9'
      coleta.canal5 = 'io_10'
      coleta.canal6 = 'io_11'
      coleta.canal7 = 'io_12'

      coleta.nivel_sinal= dados['signallevel']

      coleta.valor1 = dados['io_6']
      coleta.valor2 = dados['io_7']
      coleta.valor3 = dados['io_8']
      coleta.valor4 = dados['io_9']
      coleta.valor5 = dados['io_10']
      coleta.valor6 = dados['io_11']
      coleta.valor7 = dados['io_12']

      coleta.id_transdutor
      coleta.save()
  '''
    return JsonResponse(dados, safe=False)


@csrf_exempt
def api_coletar_por_canal(request, *args, **kwargs):
    thing_key = 'hab0001'
    canal = 'io_8'
    antes = '2017-11-01T00:00:00Z'  # as datas estao fixas apenas para demonstacao
    depois = '2017-11-01T00:59:59Z'
    api = DevicewiseHttp()
    dados = api.coletar_por_canal(thing_key, canal, antes, depois)
    return JsonResponse(dados, safe=False)
