"""Comparar dados do aluno 4 entre banco antigo e novo"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

print("=" * 80)
print("VERIFICANDO BANCO DE DADOS ATUAL")
print("=" * 80)

# Verificar qual banco está sendo usado
print(f"Database config: {firebird_service.config.get('dsn')}")
print()

conn = firebird_service.get_connection()
cursor = conn.cursor()

# Verificar se existem dados completos no banco atual
cursor.execute("""
    SELECT ID, NOME, DATA_NASCIMENTO, NATURALIDADE, 
           ENDERECO, NUMERO, BAIRRO, CIDADE, ESTADO,
           RG, CPF, COR_RACA, TRANSPORTE_ESCOLAR
    FROM ALUNOS 
    WHERE ID = 4
""")

row = cursor.fetchone()
columns = [desc[0] for desc in cursor.description]

print("Dados do aluno 4 no banco WEB:")
print("-" * 80)

for col, val in zip(columns, row):
    if val is not None and val != '':
        print(f"  {col}: {val}")
    else:
        print(f"  {col}: (vazio)")

print("-" * 80)
print()

# Agora verificar quantos campos tem preenchidos
campos_preenchidos = sum(1 for val in row if val is not None and val != '')
print(f"Campos preenchidos: {campos_preenchidos} de {len(columns)}")

cursor.close()
conn.close()

print()
print("=" * 80)
print("CONCLUSÃO:")
print("=" * 80)
if campos_preenchidos < 10:
    print("⚠️  O aluno 4 tem POUCOS dados preenchidos no banco web")
    print("💡 Sugestão: Importar dados completos do banco antigo do Delphi")
else:
    print("✅ O aluno 4 já tem dados suficientes no banco web")

print("=" * 80)
