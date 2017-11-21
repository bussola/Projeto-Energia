from django.core.management.base import BaseCommand, CommandError
from dashboard.devicewise.DevicewiseHttp import DevicewiseHttp
from dashboard.devicewise.DevicewiseColetor import DevicewiseColetor

class Command(BaseCommand):
    def iniciar_coletas(request):
        api = DevicewiseColetor(request.user)
        ok = api.coletar_por_usuario()
        resposta = 'Coleta efetuada com exito' if ok else 'Erro ao coletar dados'
        return HttpResponse(resposta)

    def handle(self, **options):
        self.stdout.write("oi")
