"""Verificar modalidades e resoluções disponíveis"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

print("=" * 80)
print("VERIFICANDO MODALIDADES DE ENSINO NO BANCO")
print("=" * 80)

# Buscar todas as modalidades únicas na tabela ALUNOS
cursor.execute("""
    SELECT DISTINCT MODALIDADE_ENSINO 
    FROM ALUNOS 
    WHERE MODALIDADE_ENSINO IS NOT NULL AND MODALIDADE_ENSINO <> ''
    ORDER BY MODALIDADE_ENSINO
""")

modalidades = cursor.fetchall()

print(f"\nModalidades encontradas nos alunos ({len(modalidades)}):")
for mod in modalidades:
    print(f"  - {mod[0].strip()}")

# Buscar todas as resoluções únicas
cursor.execute("""
    SELECT DISTINCT RESOLUCAO_AUTORIZACAO 
    FROM ALUNOS 
    WHERE RESOLUCAO_AUTORIZACAO IS NOT NULL AND RESOLUCAO_AUTORIZACAO <> ''
    ORDER BY RESOLUCAO_AUTORIZACAO
""")

resolucoes = cursor.fetchall()

print(f"\n\nResoluções encontradas nos alunos ({len(resolucoes)}):")
for res in resolucoes[:20]:  # Mostrar só as primeiras 20
    print(f"  - {res[0].strip()}")

if len(resolucoes) > 20:
    print(f"  ... e mais {len(resolucoes) - 20}")

# Verificar se existe tabela de resolução
cursor.execute("""
    SELECT RDB$RELATION_NAME 
    FROM RDB$RELATIONS 
    WHERE RDB$RELATION_NAME LIKE '%RESOLUCAO%' 
    OR RDB$RELATION_NAME LIKE '%MODALIDADE%'
""")

tabelas = cursor.fetchall()

print("\n\nTabelas relacionadas:")
for t in tabelas:
    print(f"  - {t[0].strip()}")

cursor.close()
conn.close()
