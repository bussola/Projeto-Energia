from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

handler400 = 'views.my_custom_bad_request_view'
handler403 = 'views.my_custom_permission_denied_view'
handler404 = 'views.my_custom_page_not_found_view'
handler500 = 'views.my_custom_error_view'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login$', views.do_login, name='login'),
	url(r'^logout$', views.do_logout, name='logout'),

    url(r'^password$', views.do_change_password, name='change_password'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),


	url(r'^graficos$', views.graficos, name='graficos'),

    url(r'^consumo_mensal', views.consumo_mensal, name='consumo_mensal'),
    url(r'^consumomensalporsetores', views.consumo_mensal_por_setores, name='consumo_mensal_setores'),
    url(r'^gasto_mensal', views.gasto_mensal, name='gasto_mensal'),
    url(r'^gastomensalporsetores', views.gasto_mensal_por_setores, name='gasto_mensal_por_setores'),

    url(r'^api_login',  views.api_login, name='api_login'),
    url(r'^coleta_exemplo/$', views.coleta_exemplo, name='coleta_exemplo'),
    url(r'^por_canal_exemplo/$', views.por_canal_exemplo, name='por_canal_exemplo'),
    url(r'^api_coletar/$', views.api_coletar, name='api_coletar'),
    url(r'^api_coletar_por_canal/$', views.api_coletar_por_canal, name='api_coletar_por_canal'),

    url(r'^horarios_rest', views.horarios_rest.as_view()),
]

