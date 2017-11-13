from django.contrib import admin

from .models import User, UserManager, Concessionaria, Classificacao, Transdutor, Servico, Imposto, Constante 

admin.site.register(User, UserManager, Concessionaria, Classificacao, Transdutor, Servico, Imposto, Constante)