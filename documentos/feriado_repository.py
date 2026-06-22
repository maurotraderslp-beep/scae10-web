"""
Repositório de Feriados/Calendário
Acesso à tabela FERIADOS
"""
from documentos.firebird_service import firebird_service


class FeriadoRepository:
    """Repositório para gerenciamento de feriados e eventos do calendário"""
    
    @staticmethod
    def get_all(tipo=None, ativo='S'):
        """Listar todos os feriados com filtro opcional de tipo"""
        query = """
            SELECT ID, DATA, DESCRICAO, TIPO, ATIVO
            FROM FERIADOS
            WHERE ATIVO = ?
        """
        params = [ativo]
        
        if tipo:
            query += " AND TIPO = ?"
            params.append(tipo)
        
        query += " ORDER BY DATA"
        
        return firebird_service.execute_query(query, tuple(params))
    
    @staticmethod
    def get_by_id(feriado_id):
        """Buscar feriado por ID"""
        query = """
            SELECT ID, DATA, DESCRICAO, TIPO, ATIVO
            FROM FERIADOS
            WHERE ID = ?
        """
        result = firebird_service.execute_single(query, (feriado_id,))
        return result
    
    @staticmethod
    def get_por_mes(ano, mes):
        """Buscar feriados de um mês específico"""
        query = """
            SELECT ID, DATA, DESCRICAO, TIPO, ATIVO
            FROM FERIADOS
            WHERE EXTRACT(YEAR FROM DATA) = ?
              AND EXTRACT(MONTH FROM DATA) = ?
              AND ATIVO = 'S'
            ORDER BY DATA
        """
        return firebird_service.execute_query(query, (ano, mes))
    
    @staticmethod
    def create(dados):
        """Criar novo feriado"""
        query = """
            INSERT INTO FERIADOS (DATA, DESCRICAO, TIPO, ATIVO)
            VALUES (?, ?, ?, ?)
        """
        params = (
            dados['data'],
            dados['descricao'],
            dados.get('tipo', 'FERIADO'),
            dados.get('ativo', 'S')
        )
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def update(feriado_id, dados):
        """Atualizar feriado"""
        query = """
            UPDATE FERIADOS
            SET DATA = ?,
                DESCRICAO = ?,
                TIPO = ?,
                ATIVO = ?
            WHERE ID = ?
        """
        params = (
            dados['data'],
            dados['descricao'],
            dados.get('tipo', 'FERIADO'),
            dados.get('ativo', 'S'),
            feriado_id
        )
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def delete(feriado_id):
        """Desativar feriado (delete lógico)"""
        query = """
            UPDATE FERIADOS
            SET ATIVO = 'N'
            WHERE ID = ?
        """
        return firebird_service.execute_update(query, (feriado_id,))
    
    @staticmethod
    def get_tipos():
        """Retornar lista de tipos de feriados"""
        return ['FERIADO', 'RECESSO', 'PONTO_FACULTATIVO', 'EVENTO', 'OUTRO']
