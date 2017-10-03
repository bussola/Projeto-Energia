from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	
	url(r'^graficos$', views.graficos, name='graficos'),
    url(r'^login$', views.do_login, name='login'),
	url(r'^logout$', views.do_logout, name='logout'),
    url(r'^departamentos_json', views.departamentos_json, name='departamentos_json'),
    url(r'^transdutores_json', views.transdutores_json, name='transdutores_json'),
    url(r'^horarios_rest', views.horarios_rest.as_view()),

    # ex: /polls/5/
    url(r'^(?P<cliente_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<cliente_id>[0-9]+)/results/$', views.results, name='results'),
]

