"""Testar busca de resoluções por modalidade"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.aluno_repository import localizacao_repository

print("=" * 80)
print("TESTANDO BUSCA DE RESOLUÇÕES POR MODALIDADE")
print("=" * 80)

# Testar com diferentes modalidades
modalidades_teste = [
    "ENSINO MÉDIO - REGULAR",
    "ENSINO FUNDAMENTAL - 1º GRAU",
    "ENSINO MÉDIO - MAGISTÉRIO",
]

for modalidade in modalidades_teste:
    print(f"\n📋 Testando: {modalidade}")
    print("-" * 80)
    try:
        resolucoes = localizacao_repository.get_resolucoes_por_modalidade(modalidade)
        print(f"✅ Encontradas {len(resolucoes)} resoluções:")
        for r in resolucoes:
            print(f"   - ID={r['id']}, NÚMERO={r['numero_resolucao']}, DESC={r['descricao']}")
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
