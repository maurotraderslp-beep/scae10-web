"""
Repositório de Equipamentos
Acesso à tabela EQUIPAMENTO_DATA_SHOW
"""
import fdb
from documentos.firebird_service import firebird_service


class EquipamentoRepository:
    """Repositório para gerenciamento de equipamentos"""
    
    @staticmethod
    def get_all():
        """Listar todos os equipamentos"""
        query = """
            SELECT ID, CODIGO, DESCRICAO, LOCALIZACAO, ATIVO
            FROM EQUIPAMENTO_DATA_SHOW
            ORDER BY CODIGO
        """
        return firebird_service.execute_query(query)
    
    @staticmethod
    def get_by_id(equipamento_id):
        """Buscar equipamento por ID"""
        query = """
            SELECT ID, CODIGO, DESCRICAO, LOCALIZACAO, ATIVO
            FROM EQUIPAMENTO_DATA_SHOW
            WHERE ID = ?
        """
        return firebird_service.execute_single(query, (equipamento_id,))
    
    @staticmethod
    def create(dados):
        """Criar novo equipamento"""
        query = """
            INSERT INTO EQUIPAMENTO_DATA_SHOW (CODIGO, DESCRICAO, LOCALIZACAO, ATIVO)
            VALUES (?, ?, ?, ?)
        """
        params = (
            dados['codigo'],
            dados['descricao'],
            dados.get('localizacao', ''),
            dados.get('ativo', 'S')
        )
        return firebird_service.execute_insert(query, params)
    
    @staticmethod
    def update(equipamento_id, dados):
        """Atualizar equipamento"""
        query = """
            UPDATE EQUIPAMENTO_DATA_SHOW
            SET CODIGO = ?,
                DESCRICAO = ?,
                LOCALIZACAO = ?,
                ATIVO = ?
            WHERE ID = ?
        """
        params = (
            dados['codigo'],
            dados['descricao'],
            dados.get('localizacao', ''),
            dados.get('ativo', 'S'),
            equipamento_id
        )
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def delete(equipamento_id):
        """Desativar equipamento (delete lógico)"""
        query = """
            UPDATE EQUIPAMENTO_DATA_SHOW
            SET ATIVO = 'N'
            WHERE ID = ?
        """
        return firebird_service.execute_update(query, (equipamento_id,))
