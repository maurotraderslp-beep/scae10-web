import os
import sys

sys.path.insert(0, r'c:\sysflor\scae10-web\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

import django
django.setup()

from documentos.firebird_service import firebird_service

# Buscar campos relacionados a documentação
query = """
    SELECT RDB$FIELD_NAME 
    FROM RDB$RELATION_FIELDS 
    WHERE RDB$RELATION_NAME = 'ALUNOS' 
    AND (
        RDB$FIELD_NAME CONTAINING 'FOTO' OR 
        RDB$FIELD_NAME CONTAINING 'HISTORICO' OR 
        RDB$FIELD_NAME CONTAINING 'CERTIFICADO' OR 
        RDB$FIELD_NAME CONTAINING 'CERTIDAO' OR 
        RDB$FIELD_NAME CONTAINING 'SUS' OR 
        RDB$FIELD_NAME CONTAINING 'VACINA' OR 
        RDB$FIELD_NAME CONTAINING 'RESUMO' OR 
        RDB$FIELD_NAME CONTAINING 'RESIDENCIA' OR
        RDB$FIELD_NAME CONTAINING 'DOCUMENTO'
    )
    ORDER BY RDB$FIELD_POSITION
"""

campos = firebird_service.execute_query(query)

print("Campos de documentação encontrados:")
for c in campos:
    campo_nome = list(c.values())[0].strip()
    print(f"  {campo_nome}")
