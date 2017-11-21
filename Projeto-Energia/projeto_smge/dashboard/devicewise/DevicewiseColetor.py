from dashboard.devicewise.DevicewiseHttp import DevicewiseHttp
from dashboard.models import Transdutor, Coleta, User


class DevicewiseColetor(object):

    def __init__(self):
        self.api = DevicewiseHttp()


    def coletar_por_usuario(self, usuario):
        print('DevicewiseColetor.coletar_por_usuario()')

        transdutores = Transdutor.objects.filter(id_cliente=usuario.id)
        if transdutores is None or len(transdutores) < 1:
            print('Nenhum transdutor encontrado')
            return False

        print('Qtde encontrados: ' + str(len(transdutores)))
        for t in transdutores:
            print('Transdutor: ' + str(t.id))
            dados = self.api.coletar(t.chave_api)
            if dados is None:
                print('Nada encontrado para o transdutor: ' + t.chave_api)

            data_ultima_leitura = dados['lastCommunication']
            if Coleta.objects.filter(data_leitura=data_ultima_leitura):
                print('Leitura já coletada')
                return False

            coleta = Coleta()
            coleta.data_leitura = dados['lastCommunication']
            coleta.io6 = dados['io_6']['value']
            coleta.io7 = dados['io_7']['value']
            coleta.io8 = dados['io_8']['value']
            coleta.io9 = dados['io_9']['value']
            coleta.io10 = dados['io_10']['value']
            coleta.io11 = dados['io_11']['value']
            coleta.io12 = dados['io_12']['value']
            coleta.id_transdutor = t
            coleta.save()

        return True
