from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login$', views.do_login, name='login'),
	url(r'^logout$', views.do_logout, name='logout'),

	url(r'^graficos$', views.graficos, name='graficos'),

    url(r'^consumo_mensal', views.consumo_mensal, name='consumo_mensal'),
    url(r'^consumomensalporsetor', views.consumo_mensal_setores, name='consumo_mensal_setores'),
    url(r'^gasto_mensal', views.gasto_mensal, name='gasto_mensal'),
    url(r'^gastomensalporsetor', views.gasto_mensal_por_setor, name='gasto_mensal_por_setor'),

    url(r'^horarios_rest', views.horarios_rest.as_view()),

    # ex: /polls/5/
    url(r'^(?P<cliente_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<cliente_id>[0-9]+)/results/$', views.results, name='results'),
]

