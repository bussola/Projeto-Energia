# -*- coding: utf-8 -*-
from dashboard.devicewise.DevicewiseColetor import DevicewiseColetor
from dashboard.models import User
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=10, max_instances=100)
def coletar_tudo():
    coletor_api = DevicewiseColetor()
    agora = str(datetime.datetime.today())
    print('\n%s ]----------------------------------------------------------------------' % agora)
    usuario = User.objects.all()
    for u in usuario:
        print('Agendador: Sincronizando com API com usuário %s' % u.email)
        if not coletor_api.coletar_por_usuario(u):
            print('Agendador : Não foi possível coletar dados do usuário "%s"' % u.email)
            return


sched.start()
#sched.terminate()
