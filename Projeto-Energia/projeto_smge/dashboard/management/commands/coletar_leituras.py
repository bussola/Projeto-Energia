from django.core.management import BaseCommand
from dashboard.devicewise.DevicewiseColetor import AgendadorTarefas

# A classe deve ter o nome Command, e herdar de BaseCommand
class Command(BaseCommand):
    # Exibe isso quando usuario digitar help (manage.py coletar_leituras help)
    help = "Coletor automatizado"

    # A command must define handle()
    def handle(self, *args, **options):
        AgendadorTarefas()
