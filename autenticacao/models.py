"""
Model de Usuário - Mapeia tabela USUARIOS do Firebird
Preserva sistema de senhas SHA256 do Delphi
"""
from django.db import models
import hashlib


class UsuarioManager(models.Manager):
    """Manager customizado para autenticação com SHA256"""
    
    def authenticate(self, login=None, password=None):
        """
        Autentica usuário verificando hash SHA256 da senha
        Igual ao sistema Delphi original
        """
        if login is None or password is None:
            return None
        
        # Converte login para maiúsculas (igual Delphi)
        login = login.upper().strip()
        
        # Gera hash SHA256 da senha
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        try:
            # Busca usuário com login e senha hash
            usuario = self.get(
                login=login,
                senha=password_hash,
                ativo='S'  # Campo ATIVO = 'S'/'N' do Firebird
            )
            return usuario
        except self.model.DoesNotExist:
            return None


class Usuario(models.Model):
    """
    Model que mapeia a tabela USUARIOS do Firebird
    Schema PRESERVADO do sistema Delphi
    """
    id = models.AutoField(primary_key=True, db_column='ID')
    nome = models.CharField(max_length=100, db_column='NOME')
    login = models.CharField(max_length=50, db_column='LOGIN', unique=True)
    senha = models.CharField(max_length=64, db_column='SENHA')  # SHA256 = 64 chars hex
    perfil = models.CharField(max_length=50, db_column='PERFIL')  # ADMINISTRADOR, PROFESSOR, SECRETARIA
    ativo = models.CharField(max_length=1, db_column='ATIVO')  # 'S' ou 'N'
    ultimo_acesso = models.DateTimeField(null=True, blank=True, db_column='ULTIMO_ACESSO')
    data_criacao = models.DateTimeField(null=True, blank=True, db_column='DATA_CRIACAO')
    
    objects = UsuarioManager()
    
    class Meta:
        db_table = 'USUARIOS'
        managed = False  # Django NÃO altera esta tabela
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f'{self.nome} ({self.login})'
    
    def get_full_name(self):
        return self.nome
    
    def get_short_name(self):
        return self.nome
    
    def has_perm(self, perm, obj=None):
        """Verifica permissões baseadas no perfil"""
        return self.ativo == 'S'
    
    def has_module_perms(self, app_label):
        """Verifica permissões de módulo"""
        return self.ativo == 'S'
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return self.ativo == 'S'
    
    @property
    def is_staff(self):
        """Administradores são staff"""
        return self.perfil == 'ADMINISTRADOR'
    
    @property
    def is_administrador(self):
        return self.perfil == 'ADMINISTRADOR'
    
    @property
    def is_professor(self):
        return self.perfil == 'PROFESSOR'
    
    @property
    def is_secretaria(self):
        return self.perfil == 'SECRETARIA'
