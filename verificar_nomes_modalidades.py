"""Verificar nomes exatos das modalidades no banco"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

cursor.execute("SELECT ID, NOME FROM MODALIDADES WHERE ATIVO = 'S' ORDER BY NOME")
rows = cursor.fetchall()

print("MODALIDADES NO BANCO:")
for r in rows:
    nome = r[1].strip()
    print(f'  ID={r[0]}, NOME="{nome}"')

cursor.close()
conn.close()
