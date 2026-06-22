"""
Repositório de Solicitações
Acesso à tabela SOLICITACOES
"""
from documentos.firebird_service import firebird_service


class SolicitacaoRepository:
    """Repositório para gerenciamento de solicitações de documentos"""
    
    @staticmethod
    def get_all(status=None, aluno_id=None, aluno_nome=None):
        """Listar todas as solicitações com filtros opcionais"""
        query = """
            SELECT s.ID, s.ALUNO_ID, s.TIPO_DOCUMENTO_ID, s.STATUS,
                   s.FUNCIONARIO_ID, s.DATA_SOLICITACAO,
                   s.CERTIFICADO_NUMERO, s.CERTIFICADO_FOLHA, s.CERTIFICADO_LIVRO,
                   s.DATA_EMISSAO, s.SECRETARIO_NOME, s.DIRETOR_NOME,
                   s.JUSTIFICATIVA, s.DATA_ENTREGA, s.QUEM_BUSCOU, s.OBSERVACOES,
                   s.MUNICIPIO, s.CERTIFICADO_VIA,
                   a.NOME as ALUNO_NOME, a.TURMA, a.ANO_CONCLUSAO,
                   td.DESCRICAO as TIPO_DOCUMENTO_DESCRICAO,
                   u.NOME as FUNCIONARIO_NOME
            FROM SOLICITACOES s
            LEFT JOIN ALUNOS a ON s.ALUNO_ID = a.ID
            LEFT JOIN TIPOS_DOCUMENTO td ON s.TIPO_DOCUMENTO_ID = td.ID
            LEFT JOIN USUARIOS u ON s.FUNCIONARIO_ID = u.ID
            WHERE 1=1
        """
        params = []
        
        if status:
            query += " AND s.STATUS = ?"
            params.append(status)
        
        if aluno_id:
            query += " AND s.ALUNO_ID = ?"
            params.append(aluno_id)
        
        if aluno_nome:
            query += " AND UPPER(a.NOME) CONTAINING UPPER(?)"
            params.append(aluno_nome)
        
        query += " ORDER BY s.DATA_SOLICITACAO DESC"
        
        return firebird_service.execute_query(query, tuple(params))
    
    @staticmethod
    def get_by_id(solicitacao_id):
        """Buscar solicitação por ID"""
        query = """
            SELECT s.ID, s.ALUNO_ID, s.TIPO_DOCUMENTO_ID, s.STATUS,
                   s.FUNCIONARIO_ID, s.DATA_SOLICITACAO,
                   s.CERTIFICADO_NUMERO, s.CERTIFICADO_FOLHA, s.CERTIFICADO_LIVRO,
                   s.DATA_EMISSAO, s.SECRETARIO_NOME, s.DIRETOR_NOME,
                   s.JUSTIFICATIVA, s.DATA_ENTREGA, s.QUEM_BUSCOU, s.OBSERVACOES,
                   s.MUNICIPIO, s.CERTIFICADO_VIA,
                   a.NOME as ALUNO_NOME, a.TURMA, a.ANO_CONCLUSAO,
                   td.DESCRICAO as TIPO_DOCUMENTO_DESCRICAO,
                   u.NOME as FUNCIONARIO_NOME
            FROM SOLICITACOES s
            LEFT JOIN ALUNOS a ON s.ALUNO_ID = a.ID
            LEFT JOIN TIPOS_DOCUMENTO td ON s.TIPO_DOCUMENTO_ID = td.ID
            LEFT JOIN USUARIOS u ON s.FUNCIONARIO_ID = u.ID
            WHERE s.ID = ?
        """
        return firebird_service.execute_single(query, (solicitacao_id,))
    
    @staticmethod
    def get_tipos_documento():
        """Buscar tipos de documento disponíveis"""
        query = """
            SELECT ID, DESCRICAO
            FROM TIPOS_DOCUMENTO
            ORDER BY DESCRICAO
        """
        return firebird_service.execute_query(query)

    @staticmethod
    def get_funcionarios_ativos():
        """Buscar funcionários/usuarios ativos"""
        query = """
            SELECT ID, NOME
            FROM USUARIOS
            ORDER BY NOME
        """
        return firebird_service.execute_query(query)

    @staticmethod
    def get_alunos_ativos():
        """Buscar alunos ativos para o select"""
        query = """
            SELECT ID, NOME, TURMA, ANO_CONCLUSAO
            FROM ALUNOS
            WHERE ATIVO = 'S'
            ORDER BY NOME
        """
        return firebird_service.execute_query(query)
    
    @staticmethod
    def get_status_list():
        """Retornar lista de status possíveis"""
        return ['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDO', 'CANCELADO']
    
    @staticmethod
    def create(dados):
        """Criar nova solicitação"""
        query = """
            INSERT INTO SOLICITACOES (
                ALUNO_ID, TIPO_DOCUMENTO_ID, FUNCIONARIO_ID, STATUS,
                CERTIFICADO_NUMERO, CERTIFICADO_FOLHA, CERTIFICADO_LIVRO,
                DATA_EMISSAO, SECRETARIO_NOME, DIRETOR_NOME,
                JUSTIFICATIVA, OBSERVACOES, MUNICIPIO, CERTIFICADO_VIA
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            dados.get('aluno_id'),
            dados.get('tipo_documento_id'),
            dados.get('funcionario_id'),
            dados.get('status', 'PENDENTE'),
            dados.get('certificado_numero'),
            dados.get('certificado_folha'),
            dados.get('certificado_livro'),
            dados.get('data_emissao'),
            dados.get('secretario_nome'),
            dados.get('diretor_nome'),
            dados.get('justificativa', ''),
            dados.get('observacoes', ''),
            dados.get('municipio'),
            dados.get('certificado_via', 1)
        )
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def update(solicitacao_id, dados):
        """Atualizar solicitação"""
        query = """
            UPDATE SOLICITACOES
            SET ALUNO_ID = ?,
                TIPO_DOCUMENTO_ID = ?,
                FUNCIONARIO_ID = ?,
                STATUS = ?,
                CERTIFICADO_NUMERO = ?,
                CERTIFICADO_FOLHA = ?,
                CERTIFICADO_LIVRO = ?,
                DATA_EMISSAO = ?,
                SECRETARIO_NOME = ?,
                DIRETOR_NOME = ?,
                JUSTIFICATIVA = ?,
                OBSERVACOES = ?,
                DATA_ENTREGA = ?,
                QUEM_BUSCOU = ?,
                MUNICIPIO = ?,
                CERTIFICADO_VIA = ?
            WHERE ID = ?
        """
        params = (
            dados.get('aluno_id'),
            dados.get('tipo_documento_id'),
            dados.get('funcionario_id'),
            dados.get('status', 'PENDENTE'),
            dados.get('certificado_numero'),
            dados.get('certificado_folha'),
            dados.get('certificado_livro'),
            dados.get('data_emissao'),
            dados.get('secretario_nome'),
            dados.get('diretor_nome'),
            dados.get('justificativa', ''),
            dados.get('observacoes', ''),
            dados.get('data_entrega'),
            dados.get('quem_buscou', ''),
            dados.get('municipio'),
            dados.get('certificado_via', 1),
            solicitacao_id
        )
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def delete(solicitacao_id):
        """Excluir solicitação"""
        query = "DELETE FROM SOLICITACOES WHERE ID = ?"
        return firebird_service.execute_update(query, (solicitacao_id,))
