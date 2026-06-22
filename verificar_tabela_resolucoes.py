"""Verificar estrutura da tabela RESOLUCOES"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

print("=" * 80)
print("ESTRUTURA DA TABELA RESOLUCOES")
print("=" * 80)

# Buscar campos da tabela RESOLUCOES
cursor.execute("""
    SELECT RDB$FIELD_NAME 
    FROM RDB$RELATION_FIELDS 
    WHERE RDB$RELATION_NAME = 'RESOLUCOES'
    ORDER BY RDB$FIELD_POSITION
""")

campos = cursor.fetchall()

print("\nCampos da tabela RESOLUCOES:")
for campo in campos:
    print(f"  - {campo[0].strip()}")

# Buscar todas as resoluções com suas modalidades
cursor.execute("""
    SELECT r.ID, r.MODALIDADE, r.NUMERO_RESOLUCAO, r.DESCRICAO, r.ATIVO,
           m.NOME as MODALIDADE_NOME
    FROM RESOLUCOES r
    LEFT JOIN MODALIDADES m ON r.MODALIDADE = m.ID
    WHERE r.ATIVO = 'S'
    ORDER BY m.NOME, r.NUMERO_RESOLUCAO
""")

dados = cursor.fetchall()

print(f"\n\nResoluções encontradas ({len(dados)} registros):")
modalidade_atual = None
for dado in dados:
    id_resolucao = dado[0]
    id_modalidade = dado[1]
    numero = str(dado[2]).strip()
    descricao = str(dado[3]).strip() if dado[3] else ''
    ativo = dado[4]
    nome_modalidade = str(dado[5]).strip() if dado[5] else 'N/A'
    
    if nome_modalidade != modalidade_atual:
        modalidade_atual = nome_modalidade
        print(f"\n  📚 {modalidade_atual}:")
    
    print(f"     - [{id_resolucao}] {numero} - {descricao}")

cursor.close()
conn.close()
