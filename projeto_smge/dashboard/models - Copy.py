# Modelos das tabelas do banco projeto_sge
from __future__ import unicode_literals
import datetime

from django.db import models
from django.utils import timezone


class Cliente(models.Model):
	def __str__(self):
		return self.nome
	nome = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	senha = models.CharField(max_length=255)
	cpf = models.CharField(max_length=255)
	cnpj = models.CharField(max_length=255)
	telefone = models.CharField(max_length=255)
	logradouro = models.CharField(max_length=255)
	cidade = models.CharField(max_length=255)
	estado = models.CharField(max_length=255)


class Concessionaria(models.Model):
	def __str__(self):
		return self.nome
	nome = models.CharField(max_length=255)
	hp_inicio = models.DateTimeField('hp inicio')
	hp_fim = models.DateTimeField('hp fim')
	

class Cliente_has_concessionaria(models.Model):
	id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	id_concessionaria = models.ForeignKey(Concessionaria, on_delete=models.CASCADE)
	
	
class Classificacao(models.Model):
	def __str__(self):
		return self.nome
	nome = models.CharField(max_length=255)
	id_concessionaria = models.ForeignKey(Concessionaria, on_delete=models.CASCADE)
	
	
class Transdutor(models.Model):
	def __str__(self):
		return (self.numero_serie)
	data_instalacao = models.DateTimeField('Data instalacao')
	numero_serie = models.CharField(max_length=255)
	id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	id_classificacao = models.ForeignKey(Classificacao, on_delete=models.CASCADE)
	
	
class Servico(models.Model):
	def __str__(self):
		return self.descricao
	descricao = models.CharField(max_length=255)
	valor = models.CharField(max_length=255)
	id_classificacao = models.ForeignKey(Classificacao, on_delete=models.CASCADE)
	

class Coleta(models.Model):
	data_instalacao = models.DateTimeField('data')
	hora_instalacao = models.DateTimeField('hora')
	saida1 = models.CharField(max_length=255)
	saida2 = models.CharField(max_length=255)
	saida3 = models.CharField(max_length=255)
	saida4 = models.CharField(max_length=255)
	saida5 = models.CharField(max_length=255)
	saida6 = models.CharField(max_length=255)
	saida7 = models.CharField(max_length=255)
	saida8 = models.CharField(max_length=255)
	id_transdutor = models.ForeignKey(Transdutor, on_delete=models.CASCADE)
	

class Conta_contrato(models.Model):
	conta_contrato = models.CharField(max_length=255)
	id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	
	
class Imposto(models.Model):
	def __str__(self):
		return self.nome
	nome = models.CharField(max_length=255)
	estado = models.CharField(max_length=255)
	valor = models.CharField(max_length=255)
	

class Constante(models.Model):
	def __str__(self):
		return self.nome
	nome = models.CharField(max_length=255)
	valor = models.CharField(max_length=255)