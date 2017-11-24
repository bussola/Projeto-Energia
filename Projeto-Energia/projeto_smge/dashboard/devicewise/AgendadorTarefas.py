# -*- coding: utf-8 -*-
from dashboard.devicewise.DevicewiseColetor import DevicewiseColetor
from dashboard.models import User
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=10, max_instances=100)
def coletar_tudo():
    agora = str(datetime.datetime.today())
    print('\n%s ]----------------------------------------------------------------------' % agora)
    coletor_api = DevicewiseColetor()
    usuarios = User.objects.all()
    for u in usuarios:
        print('Sincronizando com usuário %s' % u.email)
        if not coletor_api.coletar_por_usuario(u):
            print('Agendador : Não foi possível coletar dados do usuário "%s"' % u.email)
            return


sched.start()
# sched.terminate()
