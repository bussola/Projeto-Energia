from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count, Sum
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
from datetime import datetime
from datetime import timedelta

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
    #filtro = Coleta.objects.all().annotate(Count('io6'))
    #filtro = Employee.objects.values('department__dept_name', 'level__level_name').annotate(employee_count = Count('id')).order_by('-employee_count')[:1]

    # last_5_min = datetime.now() - timedelta(seconds=5*60)
    # soma_5_min = (Coleta.objects
    # .filter(data_leitura__gt=last_5_min)
    # .extra(select={'day': 'date(data_leitura)'})
    # .values('day')
    # .annotate(sum=Sum('io6')))
    # for f in soma_5_min:
    #     filtro = f['sum'] #pega o dicionario sum

    #media_io6 = Coleta.objects.values_list('media_io6', flat=True).filter(id_transdutor=1).order_by('-id').first() #TODO ajustar id_transdutor=1

        
    #adicionar no BD Coleta na coluna media_io6

    # qnt_dados = (Coleta.objects
    # .filter(data_leitura__gt=last_5_min)
    # .extra(select={'day': 'date(data_leitura)'})
    # .values('day')
    # .annotate(contador=Count('io6')))
    # for q in qnt_dados:
    #     qnt = q['contador'] #pega o dicionario contador

    coletas = Coleta.objects.all().order_by('-id')
    transdutores = Transdutor.objects.filter(chave_api="hab0001")
    #io6_name = Transdutor.objects.values_list('nome_io6', flat=True).filter(chave_api="hab0001")
    parametros = Transdutor.objects.all().filter(chave_api="hab0001").order_by('-id')
    parametro_a = Transdutor.objects.values_list('parametro_a', flat=True).filter(chave_api="hab0001").order_by('-id').first()
    parametro_b = Transdutor.objects.values_list('parametro_b', flat=True).filter(chave_api="hab0001").order_by('-id').first()
    parametro_a_float = float(parametro_a.replace(',','.'))
    parametro_b_float = float(parametro_b.replace(',','.'))
    # io6 = Coleta.objects.values_list('io6', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    data = Coleta.objects.values_list('data_leitura', flat=True).filter(id_transdutor=1).order_by('-id')[:10]
    context = {
        #'media_io6': media_io6,
        #'qnt': qnt,
        'filtro': filtro,
        'transdutores': transdutores,
        'parametro_a_float': parametro_a_float,
        'parametro_b_float': parametro_b_float,
        'coletas': coletas,
        #'io6_name': io6_name,
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
    #io6_name = Transdutor.objects.values_list('nome_io6', flat=True).filter(chave_api="hab0001")
    data2 = [
        {'value': 2554, 'label': 'Industria'},
        {'value': 242, 'label': 'Oficina'},
        {'value': 3233, 'label': 'Suprimento'},
        {'value': 122, 'label': 'Outros Departamentos'}
    ]
    return JsonResponse(data2, safe=False)


# def gasto_mensal(request, *args, **kargs):
#     mes = request.GET['mes']  # TODO: avaliar a forma como isso ta sendo feito
#     data3 = []
#     transdutores1 = Transdutor.objects.filter(id_cliente=request.user.id)
#     for t in transdutores1:
#         coletas1 = Coleta.objects.filter(id_transdutor_id=t.id, data_leitura__month=mes).order_by('data_leitura')
#         for c in coletas1:
#             # soma os valores dos canais
#             valores1 = [float(c.io6), float(c.io7), float(c.io8), float(c.io9), float(c.io10), float(c.io11),
#                        float(c.io12)]
#             soma1 = sum(valores1)
#             dia1 = int(c.data_leitura.day)
#             adicionado1 = False
#             for dado in data3:
#                 if dado['Dia'] == dia1:
#                     novo_valor1 = float(dado['Valor']) + soma1
#                     dado['Valor'] = "%.4f" % novo_valor1
#                     adicionado1 = True

#             if not adicionado1:
#                 data3.append({'Dia': dia1, 'Valor': "%.4f" % soma1})
#     return JsonResponse(data3, safe=False)


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
