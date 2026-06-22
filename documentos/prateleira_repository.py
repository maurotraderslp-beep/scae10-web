"""
Repositório para gerenciar Prateleiras no Firebird
"""
from documentos.firebird_service import firebird_service


class PrateleiraRepository:
    """Repositório para Prateleiras"""
    
    @staticmethod
    def get_all():
        """Listar todas as prateleiras com dados da estante e corredor"""
        query = """
            SELECT p.ID, p.CODIGO, p.DESCRICAO, p.ESTANTE_ID, p.FOTO_PATH, p.ATIVO, p.DATA_CADASTRO,
                   e.DESCRICAO as ESTANTE_DESCRICAO, e.CODIGO as ESTANTE_CODIGO,
                   c.DESCRICAO as CORREDOR_DESCRICAO, c.CODIGO as CORREDOR_CODIGO
            FROM PRATELEIRAS p
            LEFT JOIN ESTANTES e ON p.ESTANTE_ID = e.ID
            LEFT JOIN CORREDORES c ON e.CORREDOR_ID = c.ID
            ORDER BY c.CODIGO, e.CODIGO, p.CODIGO
        """
        return firebird_service.execute_query(query)
    
    @staticmethod
    def get_by_id(prateleira_id):
        """Buscar prateleira por ID"""
        query = """
            SELECT ID, CODIGO, DESCRICAO, ESTANTE_ID, FOTO_PATH, ATIVO, DATA_CADASTRO
            FROM PRATELEIRAS
            WHERE ID = ?
        """
        return firebird_service.execute_single(query, [prateleira_id])
    
    @staticmethod
    def get_por_estante(estante_id):
        """Listar prateleiras de uma estante específica"""
        query = """
            SELECT ID, CODIGO, DESCRICAO, ESTANTE_ID, FOTO_PATH, ATIVO, DATA_CADASTRO
            FROM PRATELEIRAS
            WHERE ESTANTE_ID = ? AND ATIVO = 'S'
            ORDER BY CODIGO
        """
        return firebird_service.execute_query(query)
    
    @staticmethod
    def create(dados):
        """Criar nova prateleira"""
        query = """
            INSERT INTO PRATELEIRAS (CODIGO, DESCRICAO, ESTANTE_ID, FOTO_PATH, ATIVO, DATA_CADASTRO)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        params = [
            dados.get('codigo', ''),
            dados.get('descricao', ''),
            dados.get('estante_id', None),
            dados.get('foto_path', ''),
            dados.get('ativo', 'S')
        ]
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def update(prateleira_id, dados):
        """Atualizar prateleira"""
        campos_permitidos = ['codigo', 'descricao', 'estante_id', 'foto_path', 'ativo']
        
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
        
        params.append(prateleira_id)
        
        query = f"""
            UPDATE PRATELEIRAS
            SET {', '.join(campos_update)}
            WHERE ID = ?
        """
        
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def delete(prateleira_id):
        """Desativar prateleira (não apaga fisicamente)"""
        return PrateleiraRepository.update(prateleira_id, {'ativo': 'N'})
