from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect

from .models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    nomes = User.objects.filter(pk=1)
    first_name = User.objects.values_list('first_name', flat=True).filter(pk=2)
    #nome = Cliente.objects.order_by('-nome').filter(pk=1)
    latest_question_list = User.objects.order_by('-first_name')[:5]
    context = {
        'latest_question_list': latest_question_list,
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
	latest_question_list = User.objects.order_by('-first_name')[:5]
	context = {
		'latest_question_list': latest_question_list,
		'first_name': first_name,
		}
	return render(request, 'dashboard/graficos.html', context)


def do_login(request):
    #return render(request, 'dashboard/home.html')
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			return redirect('/graficos')
	return render(request, 'dashboard/login.html')


def do_logout(request):
    #return render(request, 'dashboard/logout.html')
	logout(request)
	return redirect('/login')