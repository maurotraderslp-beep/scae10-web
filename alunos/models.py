"""
Model de Aluno - Mapeia tabela ALUNOS do Firebird
Schema PRESERVADO do sistema Delphi - 53 colunas
"""
from django.db import models


class Aluno(models.Model):
    """
    Model que mapeia a tabela ALUNOS do Firebird
    Todas as colunas preservadas do sistema Delphi
    """
    
    # Dados Básicos
    id = models.AutoField(primary_key=True, db_column='ID')
    nome = models.CharField(max_length=100, db_column='NOME')
    data_nascimento = models.DateField(null=True, blank=True, db_column='DATA_NASCIMENTO')
    nome_mae = models.CharField(max_length=100, null=True, blank=True, db_column='NOME_MAE')
    nome_pai = models.CharField(max_length=100, null=True, blank=True, db_column='NOME_PAI')
    
    # Naturalidade
    nacionalidade = models.CharField(max_length=50, null=True, blank=True, db_column='NACIONALIDADE')
    naturalidade = models.CharField(max_length=50, null=True, blank=True, db_column='NATURALIDADE')
    estado_naturalidade = models.CharField(max_length=2, null=True, blank=True, db_column='ESTADO_NATURALIDADE')
    
    # Documentos
    cpf = models.CharField(max_length=14, null=True, blank=True, db_column='CPF')
    rg = models.CharField(max_length=20, null=True, blank=True, db_column='RG')
    cor_raca = models.CharField(max_length=20, null=True, blank=True, db_column='COR_RACA')
    nis = models.CharField(max_length=20, null=True, blank=True, db_column='NIS')
    
    # Contato
    telefone = models.CharField(max_length=20, null=True, blank=True, db_column='TELEFONE')
    email = models.EmailField(max_length=100, null=True, blank=True, db_column='EMAIL')
    
    # Endereço
    endereco = models.CharField(max_length=200, null=True, blank=True, db_column='ENDERECO')
    bairro = models.CharField(max_length=50, null=True, blank=True, db_column='BAIRRO')
    cidade = models.CharField(max_length=50, null=True, blank=True, db_column='CIDADE')
    estado = models.CharField(max_length=2, null=True, blank=True, db_column='ESTADO')
    
    # Escolar
    modalidade_ensino = models.CharField(max_length=50, null=True, blank=True, db_column='MODALIDADE_ENSINO')
    turma = models.CharField(max_length=50, null=True, blank=True, db_column='TURMA')
    situacao = models.CharField(max_length=20, null=True, blank=True, db_column='SITUACAO')
    
    # Transporte Escolar
    transporte_escolar = models.CharField(max_length=1, null=True, blank=True, db_column='TRANSPORTE_ESCOLAR')
    tipo_transporte = models.CharField(max_length=50, null=True, blank=True, db_column='TIPO_TRANSPORTE')
    tipo_veiculo = models.CharField(max_length=50, null=True, blank=True, db_column='TIPO_VEICULO')
    
    # Transferência
    escola_destino = models.CharField(max_length=100, null=True, blank=True, db_column='ESCOLA_DESTINO')
    inep_escola_destino = models.CharField(max_length=20, null=True, blank=True, db_column='INEP_ESCOLA_DESTINO')
    cidade_destino = models.CharField(max_length=50, null=True, blank=True, db_column='CIDADE_DESTINO')
    uf_destino = models.CharField(max_length=2, null=True, blank=True, db_column='UF_DESTINO')
    contato_destino = models.CharField(max_length=100, null=True, blank=True, db_column='CONTATO_DESTINO')
    
    # Localização Física (Biblioteca)
    corredor = models.CharField(max_length=10, null=True, blank=True, db_column='CORREDOR')
    estante = models.CharField(max_length=10, null=True, blank=True, db_column='ESTANTE')
    prateleira = models.CharField(max_length=10, null=True, blank=True, db_column='PRATELEIRA')
    
    # Documentação Entregue
    foto_3x4 = models.CharField(max_length=1, null=True, blank=True, db_column='FOTO_3X4')
    historico = models.CharField(max_length=1, null=True, blank=True, db_column='HISTORICO')
    certificado = models.CharField(max_length=1, null=True, blank=True, db_column='CERTIFICADO')
    rg_doc = models.CharField(max_length=1, null=True, blank=True, db_column='RG_DOC')
    cpf_doc = models.CharField(max_length=1, null=True, blank=True, db_column='CPF_DOC')
    comprovante_residencia = models.CharField(max_length=1, null=True, blank=True, db_column='COMPROVANTE_RESIDENCIA')
    certidao_nascimento = models.CharField(max_length=1, null=True, blank=True, db_column='CERTIDAO_NASCIMENTO')
    cartao_sus = models.CharField(max_length=1, null=True, blank=True, db_column='CARTAO_SUS')
    folha_resumo = models.CharField(max_length=1, null=True, blank=True, db_column='FOLHA_RESUMO')
    carteira_vacina = models.CharField(max_length=1, null=True, blank=True, db_column='CARTEIRA_VACINA')
    
    # Observações
    ficha_historica = models.TextField(null=True, blank=True, db_column='FICHA_HISTORICA')
    pdc = models.TextField(null=True, blank=True, db_column='PDC')
    comportamento = models.TextField(null=True, blank=True, db_column='COMPORTAMENTO')
    observacoes = models.TextField(null=True, blank=True, db_column='OBSERVACOES')
    
    # Controle
    ativo = models.CharField(max_length=1, default='S', db_column='ATIVO')  # 'S' ou 'N'
    data_cadastro = models.DateTimeField(auto_now_add=True, db_column='DATA_CADASTRO')
    data_atualizacao = models.DateTimeField(auto_now=True, db_column='DATA_ATUALIZACAO')
    
    class Meta:
        db_table = 'ALUNOS'
        managed = False  # Django NÃO altera esta tabela
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def nome_completo(self):
        return self.nome
    
    @property
    def idade(self):
        """Calcula idade a partir da data de nascimento"""
        if self.data_nascimento:
            from datetime import date
            today = date.today()
            idade = today.year - self.data_nascimento.year
            if (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day):
                idade -= 1
            return idade
        return None
    
    @property
    def situacao_display(self):
        """Retorna situação formatada"""
        situacoes = {
            'ATIVO': 'Ativo',
            'TRANSFERIDO': 'Transferido',
            'CONCLUIDO': 'Concluído',
            'TRANCADO': 'Trancado',
        }
        return situacoes.get(self.situacao, self.situacao or 'Não informado')
