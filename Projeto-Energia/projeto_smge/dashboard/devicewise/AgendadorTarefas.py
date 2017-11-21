# -*- coding: utf-8 -*-
from dashboard.devicewise.DevicewiseColetor import DevicewiseColetor
from dashboard.models import User
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=3)
def coletar_tudo():
    print('------------------------------------------')
    print('Sincronizando com API (transdutores)')
    api = DevicewiseColetor()
    for u in User.objects.all():
        api.set_usuario(u)
        print('Coletando dados do usuário "%s"' % u.email)
        if not api.coletar_por_usuario():
            print('Não foi possível coletar dados do usuário "%s"' % u.email)

    print('Todas as leituras foram coletadas com sucesso.')

sched.start()
