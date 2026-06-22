"""
Script para atualizar todos os paths de fotos antigos para o formato novo
Remove 'C:\SCAE10\' e mantém apenas 'Fotos/nome_arquivo.jpg'
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

# Buscar todos os alunos com path antigo
cursor.execute("""
    SELECT ID, NOME, FOTO_PATH 
    FROM ALUNOS 
    WHERE FOTO_PATH STARTING WITH 'C:'
""")

rows = cursor.fetchall()

print("=" * 80)
print(f"Encontrados {len(rows)} alunos com path antigo")
print("=" * 80)

import os

for row in rows:
    aluno_id = row[0]
    nome = row[1]
    foto_path_antigo = row[2]
    
    # Extrair apenas o nome do arquivo
    nome_arquivo = os.path.basename(foto_path_antigo)
    foto_path_novo = f'Fotos/{nome_arquivo}'
    
    print(f"ID: {aluno_id}")
    print(f"  NOME: {nome}")
    print(f"  ANTIGO: {foto_path_antigo}")
    print(f"  NOVO:   {foto_path_novo}")
    
    # Atualizar no banco
    cursor.execute("""
        UPDATE ALUNOS 
        SET FOTO_PATH = ?
        WHERE ID = ?
    """, (foto_path_novo, aluno_id))
    
    conn.commit()
    print("  ✅ Atualizado!")
    print()

print("=" * 80)
print(f"✅ {len(rows)} alunos atualizados!")
print("=" * 80)

cursor.close()
conn.close()
