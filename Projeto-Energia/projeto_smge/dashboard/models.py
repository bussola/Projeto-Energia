# Modelos das tabelas do banco projeto_sge
from __future__ import unicode_literals
import datetime

from django.db import models
from django.utils import timezone

from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    avatar = models.ImageField(upload_to='dashboard/static/avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Concessionaria(models.Model):
    nome = models.CharField(max_length=255)
    hp_inicio = models.DateTimeField('hp inicio')
    hp_fim = models.DateTimeField('hp fim')
    def __str__(self):
        return self.nome


class Cliente_has_concessionaria(models.Model):
    id_cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    id_concessionaria = models.ForeignKey(Concessionaria, on_delete=models.CASCADE)


class Classificacao(models.Model):
    nome = models.CharField(max_length=255)
    id_concessionaria = models.ForeignKey(Concessionaria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Transdutor(models.Model):
    data_instalacao = models.DateTimeField('Data instalacao')
    numero_serie = models.CharField(max_length=255)
    chave_api = models.CharField(max_length=25, default='', blank=False) #T TODO: precisamos verificar se KEY cadastrado existe em algum equipamento
    id_cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    id_classificacao = models.ForeignKey(Classificacao, on_delete=models.CASCADE)
    parametro_a = models.CharField(max_length=255)
    parametro_b = models.CharField(max_length=255)
    hora_ponto_inicio = models.TimeField('Hora inicio') 
    hora_ponto_fim = models.TimeField('Hora fim')
    nome_io6 = models.CharField(max_length=255)
    nome_io7 = models.CharField(max_length=255, blank=True)
    nome_io8 = models.CharField(max_length=255, blank=True)
    nome_io9 = models.CharField(max_length=255, blank=True)
    nome_io10 = models.CharField(max_length=255, blank=True)
    nome_io11 = models.CharField(max_length=255, blank=True)
    nome_io12 = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return (self.numero_serie)


class Servico(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    id_classificacao = models.ForeignKey(Classificacao, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao


class Coleta(models.Model):
    data_leitura = models.DateTimeField(null=True)  # TODO: MUdar isso depois
    io6 = models.FloatField(max_length=255, null=True)
    media_io6 = models.FloatField(max_length=255, null=True)
    io7 = models.FloatField(max_length=255, null=True)
    io8 = models.FloatField(max_length=255, null=True)
    io9 = models.FloatField(max_length=255, null=True)
    io10 = models.FloatField(max_length=255, null=True)
    io11 = models.FloatField(max_length=255, null=True)
    io12 = models.FloatField(max_length=255, null=True)
    id_transdutor = models.ForeignKey(Transdutor, on_delete=models.CASCADE)


class Conta_contrato(models.Model):
    conta_contrato = models.CharField(max_length=255)
    id_cliente = models.ForeignKey(User, on_delete=models.CASCADE)


class Imposto(models.Model):
    nome = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Constante(models.Model):
    nome = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
