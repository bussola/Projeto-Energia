from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import User, Coleta, Transdutor
from rest_framework.views import APIView
from rest_framework.response import Response
from dashboard.devicewise.DevicewiseHttp import DevicewiseHttp
from dashboard.devicewise.DevicewiseColetor import DevicewiseColetor

from django.core.urlresolvers import reverse


def my_custom_bad_request_view(request):
    return render(request, '400.html', )


def my_custom_permission_denied_view(request):
    return render(request, '403.html', )


def my_custom_page_not_found_view(request):
    return render(request, '404.html', )


def my_custom_error_view(request):
    return render(request, '500.html', )


def index(request):
    return render(request, 'dashboard/index.html')


def do_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/change_password.html', {
        'form': form
    })


# def reset_confirm(request, uidb36=None, token=None):
#     return password_reset_confirm(request, template_name='dashboard/password_reset_confirm.html',
#         uidb36=uidb36, token=token, post_reset_redirect=reverse('dashboard:login'))


# def reset(request):
#     return password_reset(request, template_name='dashboard/reset.html',
#         email_template_name='dashboard/reset_email.html',
#         subject_template_name='dashboard/reset_subject.txt',
#         post_reset_redirect=reverse('dashboard:login'))


@login_required
def graficos(request):
    current_user = request.user
    first_name = User.objects.values_list('first_name', flat=True).filter(pk=current_user.id)
    last_name = User.objects.values_list('last_name', flat=True).filter(pk=current_user.id)
    date_joined = User.objects.values_list('date_joined', flat=True).filter(pk=current_user.id)
    context = {
        'last_name': last_name,
        'first_name': first_name,
        'date_joined': date_joined,
    }
    return render(request, 'dashboard/graficos.html', context)

def printa(request):
    io6 = Coleta.objects.values_list('io6', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    io7 = Coleta.objects.values_list('io7', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    io8 = Coleta.objects.values_list('io8', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    io9 = Coleta.objects.values_list('io9', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    io10 = Coleta.objects.values_list('io10', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    io11 = Coleta.objects.values_list('io11', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    io12 = Coleta.objects.values_list('io12', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    data = Coleta.objects.values_list('data_leitura', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    context = {
        'io6': io6,
        'io7': io7,
        'io8': io8,
        'io9': io9,
        'io10': io10,
        'io11': io11,
        'io12': io12,
        'data': data,
    }
    return render(request, 'dashboard/print.html', context)


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
    mes = request.GET['mes']  # TODO: avaliar a forma como isso ta sendo feito
    dados = []
    transdutores = Transdutor.objects.filter(id_cliente=request.user.id)
    for t in transdutores:
        coletas = Coleta.objects.filter(id_transdutor_id=t.id, data_leitura__month=mes).order_by('data_leitura')
        for c in coletas:
            # soma os valores dos canais
            valores = [float(c.io6), float(c.io7), float(c.io8), float(c.io9), float(c.io10), float(c.io11),
                       float(c.io12)]
            soma = sum(valores)
            dia = int(c.data_leitura.day)
            adicionado = False
            for dado in dados:
                if dado['Dia'] == dia:
                    novo_valor = float(dado['Consumo']) + soma
                    dado['Consumo'] = "%.4f" % novo_valor
                    adicionado = True

            if not adicionado:
                dados.append({'Dia': dia, 'Consumo': "%.4f" % soma})

    return JsonResponse(dados, safe=False)


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
