from django.contrib import admin

from .models import User, Concessionaria, Classificacao, Transdutor, Servico, Imposto, Constante 

admin.site.register(User)
admin.site.register(Concessionaria)
admin.site.register(Classificacao)
admin.site.register(Transdutor)
admin.site.register(Servico)
admin.site.register(Imposto)
admin.site.register(Constante)

