"""
Repositório para gerenciar Estantes no Firebird
"""
from documentos.firebird_service import firebird_service


class EstanteRepository:
    """Repositório para Estantes"""
    
    @staticmethod
    def get_all():
        """Listar todas as estantes com dados do corredor"""
        query = """
            SELECT e.ID, e.CODIGO, e.DESCRICAO, e.CORREDOR_ID, e.FOTO_PATH, e.ATIVO, e.DATA_CADASTRO,
                   c.DESCRICAO as CORREDOR_DESCRICAO, c.CODIGO as CORREDOR_CODIGO
            FROM ESTANTES e
            LEFT JOIN CORREDORES c ON e.CORREDOR_ID = c.ID
            ORDER BY c.CODIGO, e.CODIGO
        """
        return firebird_service.execute_query(query)
    
    @staticmethod
    def get_by_id(estante_id):
        """Buscar estante por ID"""
        query = """
            SELECT ID, CODIGO, DESCRICAO, CORREDOR_ID, FOTO_PATH, ATIVO, DATA_CADASTRO
            FROM ESTANTES
            WHERE ID = ?
        """
        return firebird_service.execute_single(query, [estante_id])
    
    @staticmethod
    def get_por_corredor(corredor_id):
        """Listar estantes de um corredor específico"""
        query = """
            SELECT ID, CODIGO, DESCRICAO, CORREDOR_ID, FOTO_PATH, ATIVO, DATA_CADASTRO
            FROM ESTANTES
            WHERE CORREDOR_ID = ? AND ATIVO = 'S'
            ORDER BY CODIGO
        """
        return firebird_service.execute_query(query)
    
    @staticmethod
    def create(dados):
        """Criar nova estante"""
        query = """
            INSERT INTO ESTANTES (CODIGO, DESCRICAO, CORREDOR_ID, FOTO_PATH, ATIVO, DATA_CADASTRO)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        params = [
            dados.get('codigo', ''),
            dados.get('descricao', ''),
            dados.get('corredor_id', None),
            dados.get('foto_path', ''),
            dados.get('ativo', 'S')
        ]
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def update(estante_id, dados):
        """Atualizar estante"""
        campos_permitidos = ['codigo', 'descricao', 'corredor_id', 'foto_path', 'ativo']
        
        campos_update = []
        params = []
        
        for campo in campos_permitidos:
            if campo in dados:
                valor = dados[campo]
                if valor == '':
                    valor = None
                campos_update.append(f"{campo.upper()} = ?")
                params.append(valor)
        
        if not campos_update:
            raise ValueError("Nenhum campo válido para atualizar")
        
        params.append(estante_id)
        
        query = f"""
            UPDATE ESTANTES
            SET {', '.join(campos_update)}
            WHERE ID = ?
        """
        
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def delete(estante_id):
        """Desativar estante (não apaga fisicamente)"""
        return EstanteRepository.update(estante_id, {'ativo': 'N'})
