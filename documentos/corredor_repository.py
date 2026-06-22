"""
Repositório para gerenciar Corredores no Firebird
"""
from documentos.firebird_service import firebird_service


class CorredorRepository:
    """Repositório para Corredores"""
    
    @staticmethod
    def get_all():
        """Listar todos os corredores"""
        query = """
            SELECT ID, CODIGO, DESCRICAO, FOTO_PATH, ATIVO, DATA_CADASTRO
            FROM CORREDORES
            ORDER BY CODIGO
        """
        return firebird_service.execute_query(query)
    
    @staticmethod
    def get_by_id(corredor_id):
        """Buscar corredor por ID"""
        query = """
            SELECT ID, CODIGO, DESCRICAO, FOTO_PATH, ATIVO, DATA_CADASTRO
            FROM CORREDORES
            WHERE ID = ?
        """
        return firebird_service.execute_single(query, [corredor_id])
    
    @staticmethod
    def create(dados):
        """Criar novo corredor"""
        query = """
            INSERT INTO CORREDORES (CODIGO, DESCRICAO, FOTO_PATH, ATIVO, DATA_CADASTRO)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """
        params = [
            dados.get('codigo', ''),
            dados.get('descricao', ''),
            dados.get('foto_path', ''),
            dados.get('ativo', 'S')
        ]
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def update(corredor_id, dados):
        """Atualizar corredor"""
        campos_permitidos = ['codigo', 'descricao', 'foto_path', 'ativo']
        
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
        
        params.append(corredor_id)
        
        query = f"""
            UPDATE CORREDORES
            SET {', '.join(campos_update)}
            WHERE ID = ?
        """
        
        return firebird_service.execute_update(query, params)
    
    @staticmethod
    def delete(corredor_id):
        """Desativar corredor (não apaga fisicamente)"""
        return CorredorRepository.update(corredor_id, {'ativo': 'N'})
