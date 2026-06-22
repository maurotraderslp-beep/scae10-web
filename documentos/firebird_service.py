"""
Serviço de Conexão com Firebird
Permite ler dados do banco SCAE.FDB existente
"""
import fdb
from django.conf import settings


class FirebirdService:
    """Service para conectar e consultar o Firebird"""
    
    def __init__(self):
        self.config = settings.FIREBIRD_CONFIG
        self.connection = None
    
    def get_connection(self):
        """Obter conexão com Firebird"""
        if self.connection is None or self.connection.closed:
            # Usar formato: localhost/porta:caminho
            dsn = self.config.get('dsn')
            port = self.config.get('port', 3050)
            
            # Formato correto para Firebird 2.5 na porta 3025
            # localhost/3025:c:\caminho\banco.fdb
            if 'localhost' in dsn.lower() or '127.0.0.1' in dsn.lower():
                # Já tem host, só garantir que está correto
                connection_dsn = dsn
            else:
                # Adicionar host e porta
                # Remover barras invertidas duplas se houver
                clean_dsn = dsn.replace('\\', '\\\\')
                connection_dsn = f'localhost/{port}:{clean_dsn}'
            
            self.connection = fdb.connect(
                dsn=connection_dsn,
                user=self.config['user'],
                password=self.config['password'],
                charset=self.config.get('charset', 'WIN1252')
            )
        return self.connection
    
    def execute_query(self, query, params=None):
        """Executar query e retornar resultados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params or ())
            columns = [desc[0].lower() for desc in cursor.description]  # Converter para minúsculo
            rows = cursor.fetchall()
            results = [dict(zip(columns, row)) for row in rows]
            return results
        except Exception as e:
            print(f"Erro na query: {e}")
            return []
        finally:
            cursor.close()
    
    def execute_single(self, query, params=None):
        """Executar query e retornar um único resultado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params or ())
            if cursor.description:
                columns = [desc[0].lower() for desc in cursor.description]  # Converter para minúsculo
                row = cursor.fetchone()
                if row:
                    return dict(zip(columns, row))
            return None
        except Exception as e:
            print(f"Erro na query: {e}")
            return None
        finally:
            cursor.close()
    
    def execute_update(self, query, params=None):
        """Executar UPDATE/INSERT/DELETE e retornar número de linhas afetadas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params or ())
            conn.commit()  # Commitar a transação
            return cursor.rowcount
        except Exception as e:
            conn.rollback()  # Rollback em caso de erro
            print(f"Erro na execução: {e}")
            raise
        finally:
            cursor.close()
    
    def close(self):
        """Fechar conexão"""
        if self.connection and not self.connection.closed:
            self.connection.close()
            self.connection = None


# Singleton
firebird_service = FirebirdService()
