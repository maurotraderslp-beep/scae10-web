"""
Repositório de Alunos - Firebird
Consulta dados reais da tabela ALUNOS do SCAE.FDB
"""
from documentos.firebird_service import firebird_service
from datetime import date


class AlunoRepository:
    """Repositório para acessar dados de alunos no Firebird"""
    
    @staticmethod
    def get_all(ativo='S', busca='', turma='', situacao=''):
        """
        Listar alunos com filtros opcionais
        
        Args:
            ativo: 'S' para ativos, 'N' para inativos, '' para todos
            busca: Termo para buscar no nome
            turma: Filtro por turma
            situacao: Filtro por situação (ATIVO, TRANSFERIDO, etc)
        """
        query = """
            SELECT 
                a.ID, a.NOME, a.DATA_NASCIMENTO, a.NOME_MAE, a.NOME_PAI,
                a.TURMA, a.ANO_CONCLUSAO, a.SITUACAO, a.ATIVO, a.MODALIDADE_ENSINO,
                a.RESOLUCAO_AUTORIZACAO, a.ID_INEP, a.COR_RACA, a.NIS,
                a.CPF, a.RG, a.TELEFONE, a.EMAIL, a.NACIONALIDADE,
                a.NATURALIDADE, a.ESTADO_NATURALIDADE,
                a.ENDERECO, a.BAIRRO, a.CIDADE, a.ESTADO, a.ZONA_RESIDENCIA, a.LOCALIZACAO_DIFERENCIADA,
                a.TRANSPORTE_ESCOLAR, a.TIPO_TRANSPORTE, a.TIPO_VEICULO_TRANSPORTE,
                a.ESCOLA_DESTINO, a.INEP_ESCOLA_DESTINO, a.CIDADE_DESTINO, a.UF_DESTINO, a.CONTATO_DESTINO,
                a.PRATELEIRA_ID, a.FICHA_HISTORICA, a.PDC, a.COMPORTAMENTO, a.OBSERVACOES,
                a.FOTO_PATH,
                a.DOC_FOTO3X4, a.DOC_HISTORICO, a.DOC_CERTIFICADO, a.DOC_RG,
                a.DOC_CPF, a.DOC_COMPROVANTE_RESIDENCIA, a.DOC_CERTIDAO_NASCIMENTO,
                a.DOC_CARTAO_SUS, a.DOC_FOLHA_RESUMO, a.DOC_CARTEIRA_VACINA,
                p.DESCRICAO as PRATELEIRA_DESCRICAO,
                e.DESCRICAO as ESTANTE_DESCRICAO,
                c.DESCRICAO as CORREDOR_DESCRICAO
            FROM ALUNOS a
            LEFT JOIN PRATELEIRAS p ON a.PRATELEIRA_ID = p.ID
            LEFT JOIN ESTANTES e ON p.ESTANTE_ID = e.ID
            LEFT JOIN CORREDORES c ON e.CORREDOR_ID = c.ID
            WHERE 1=1
        """
        params = []
        
        # Filtro por ativo
        if ativo:
            query += " AND a.ATIVO = ?"
            params.append(ativo)
        
        # Filtro por busca no nome (usando LIKE ao invés de CONTAINING)
        if busca:
            # Firebird/fdb tem problema com CONTAINING + parâmetros
            # Usar LIKE com % no início e fim
            query += " AND NOME LIKE ?"
            params.append(f'%{busca.upper()}%')
        
        # Filtro por turma
        if turma:
            query += " AND TURMA = ?"
            params.append(turma)
        
        # Filtro por situação
        if situacao:
            query += " AND SITUACAO = ?"
            params.append(situacao)
        
        # Ordena por nome
        query += " ORDER BY NOME"
        
        resultados = firebird_service.execute_query(query, params)
        
        # Calcular idade para cada aluno
        for aluno in resultados:
            if aluno.get('data_nascimento'):
                aluno['idade'] = AlunoRepository.calcular_idade(
                    aluno['data_nascimento']
                )
        
        return resultados
    
    @staticmethod
    def get_by_id(aluno_id):
        """Buscar aluno por ID com dados completos de localização"""
        query = """
            SELECT 
                a.*,
                p.DESCRICAO as PRATELEIRA_DESCRICAO,
                e.ID as ESTANTE_ID,
                e.DESCRICAO as ESTANTE_DESCRICAO,
                e.CORREDOR_ID,
                c.DESCRICAO as CORREDOR_DESCRICAO
            FROM ALUNOS a
            LEFT JOIN PRATELEIRAS p ON a.PRATELEIRA_ID = p.ID
            LEFT JOIN ESTANTES e ON p.ESTANTE_ID = e.ID
            LEFT JOIN CORREDORES c ON e.CORREDOR_ID = c.ID
            WHERE a.ID = ?
        """
        return firebird_service.execute_single(query, [aluno_id])
    
    @staticmethod
    def get_ativos_count():
        """Contar alunos ativos"""
        query = "SELECT COUNT(*) as TOTAL FROM ALUNOS WHERE ATIVO = 'S'"
        resultado = firebird_service.execute_single(query)
        return resultado['total'] if resultado else 0
    
    @staticmethod
    def calcular_idade(data_nascimento):
        """Calcular idade a partir da data de nascimento"""
        if not data_nascimento:
            return None
        
        hoje = date.today()
        
        # Se for string, converter
        if isinstance(data_nascimento, str):
            try:
                partes = data_nascimento.split('-')
                if len(partes) == 3:
                    data_nascimento = date(
                        int(partes[0]), 
                        int(partes[1]), 
                        int(partes[2])
                    )
            except:
                return None
        
        idade = hoje.year - data_nascimento.year
        
        # Ajustar se ainda não fez aniversário este ano
        if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        
        return idade
    
    @staticmethod
    def update(aluno_id, dados):
        """
        Atualizar dados de um aluno no Firebird
        
        Args:
            aluno_id: ID do aluno
            dados: Dicionário com os campos a atualizar
        """
        # Campos que serão atualizados
        campos_permitidos = [
            'nome', 'data_nascimento', 'nome_mae', 'nome_pai',
            'telefone', 'email', 'rg', 'cpf', 'nis',
            'nacionalidade', 'naturalidade', 'estado_naturalidade',
            'id_inep', 'cor_raca', 'turma', 'ano_conclusao',
            'situacao', 'modalidade_ensino', 'resolucao_autorizacao',
            'endereco', 'bairro', 'cidade', 'estado',
            'zona_residencia', 'localizacao_diferenciada',
            'transporte_escolar', 'tipo_transporte', 'tipo_veiculo_transporte',
            'escola_destino', 'inep_escola_destino', 'cidade_destino',
            'uf_destino', 'contato_destino', 'prateleira_id',
            'ficha_historica', 'pdc', 'comportamento', 'observacoes',
            'foto_path', 'ativo',
            'doc_foto3x4', 'doc_historico', 'doc_certificado', 'doc_rg',
            'doc_cpf', 'doc_comprovante_residencia', 'doc_certidao_nascimento',
            'doc_cartao_sus', 'doc_folha_resumo', 'doc_carteira_vacina'
        ]
        
        # Campos com constraint CHECK (devem ter valor válido)
        campos_obrigatorios = {
            'transporte_escolar': 'N',  # Default 'N' se vazio
            'cor_raca': 'Nao Declarada',  # Default se vazio
        }
        
        # Construir query dinâmica
        campos_update = []
        params = []
        
        for campo in campos_permitidos:
            if campo in dados:
                valor = dados[campo]
                
                # Campos obrigatórios com constraint: usar default se vazio
                if campo in campos_obrigatorios:
                    if valor == '' or valor is None:
                        valor = campos_obrigatorios[campo]
                        print(f"[DEBUG] Campo '{campo}' estava vazio, usando default: '{valor}'")
                    else:
                        print(f"[DEBUG] Campo '{campo}' com valor: '{valor}'")
                else:
                    # Outros campos: converter string vazia para None
                    if valor == '':
                        valor = None
                
                campos_update.append(f"{campo.upper()} = ?")
                params.append(valor)
        
        if not campos_update:
            raise ValueError("Nenhum campo válido para atualizar")
        
        # Adicionar ID no final
        params.append(aluno_id)
        
        query = f"""
            UPDATE ALUNOS
            SET {', '.join(campos_update)}
            WHERE ID = ?
        """
        
        # Executar update
        firebird_service.execute_update(query, params)


# Singleton
aluno_repository = AlunoRepository()


class LocalizacaoRepository:
    """Repositório para localização (Corredores, Estantes, Prateleiras)"""
    
    @staticmethod
    def get_corredores():
        """Listar todos os corredores ativos"""
        query = "SELECT ID, CODIGO, DESCRICAO FROM CORREDORES WHERE ATIVO = 'S' ORDER BY DESCRICAO"
        return firebird_service.execute_query(query)
    
    @staticmethod
    def get_estantes(corredor_id=None):
        """Listar estantes, opcionalmente filtradas por corredor"""
        query = "SELECT ID, CODIGO, DESCRICAO, CORREDOR_ID FROM ESTANTES WHERE ATIVO = 'S'"
        params = []
        
        if corredor_id:
            query += " AND CORREDOR_ID = ?"
            params.append(corredor_id)
        
        query += " ORDER BY DESCRICAO"
        return firebird_service.execute_query(query, params)
    
    @staticmethod
    def get_prateleiras(estante_id=None):
        """Listar prateleiras, opcionalmente filtradas por estante"""
        query = "SELECT ID, CODIGO, DESCRICAO, ESTANTE_ID FROM PRATELEIRAS WHERE ATIVO = 'S'"
        params = []
        
        if estante_id:
            query += " AND ESTANTE_ID = ?"
            params.append(estante_id)
        
        query += " ORDER BY DESCRICAO"
        return firebird_service.execute_query(query, params)
    
    @staticmethod
    def get_resolucoes_por_modalidade(nome_modalidade):
        """Buscar resoluções filtradas por nome da modalidade"""
        query = """
            SELECT ID, NUMERO_RESOLUCAO, DESCRICAO 
            FROM RESOLUCOES 
            WHERE MODALIDADE = ? AND ATIVO = 'S'
            ORDER BY NUMERO_RESOLUCAO
        """
        return firebird_service.execute_query(query, [nome_modalidade])


# Singleton
localizacao_repository = LocalizacaoRepository()
