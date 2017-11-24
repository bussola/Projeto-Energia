# -*- coding: utf-8 -*-
from dashboard.devicewise.DevicewiseColetor import DevicewiseColetor
from dashboard.models import User
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=10, max_instances=100)
def coletar_tudo():
<<<<<<< HEAD
    agora = str(datetime.datetime.today())
    print('\n%s ]----------------------------------------------------------------------' % agora)
    coletor_api = DevicewiseColetor()
    usuarios = User.objects.all()
    for u in usuarios:
=======
    coletor_api = DevicewiseColetor()
    agora = str(datetime.datetime.today())
    print('\n%s ]----------------------------------------------------------------------' % agora)
    for u in User.objects.all():
>>>>>>> 26e84a4d86d59e40aef679e764d178636fe6a619
        print('Sincronizando com usuário %s' % u.email)
        if not coletor_api.coletar_por_usuario(u):
            print('Agendador : Não foi possível coletar dados do usuário "%s"' % u.email)
            return


sched.start()
# sched.terminate()
