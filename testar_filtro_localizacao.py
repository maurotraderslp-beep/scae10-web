"""Testar filtro em cascata - verificar se dados estão sendo carregados"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.localizacao_repository import localizacao_repository

print("=" * 80)
print("VERIFICANDO DADOS DE LOCALIZAÇÃO")
print("=" * 80)

# Carregar dados
corredores = localizacao_repository.get_corredores()
estantes = localizacao_repository.get_estantes()
prateleiras = localizacao_repository.get_prateleiras()

print(f"\n✅ Corredores: {len(corredores)}")
for c in corredores[:5]:
    print(f"   ID={c['id']}, Descrição={c['descricao']}")

print(f"\n✅ Estantes: {len(estantes)}")
for e in estantes[:5]:
    print(f"   ID={e['id']}, Corredor ID={e['corredor_id']}, Descrição={e['descricao']}")

print(f"\n✅ Prateleiras: {len(prateleiras)}")
for p in prateleiras[:5]:
    print(f"   ID={p['id']}, Estante ID={p['estante_id']}, Descrição={p['descricao']}")

# Verificar JSON
estantes_json = json.dumps([{
    'id': e['id'],
    'descricao': e['descricao'],
    'corredor_id': e['corredor_id']
} for e in estantes])

prateleiras_json = json.dumps([{
    'id': p['id'],
    'descricao': p['descricao'],
    'estante_id': p['estante_id']
} for p in prateleiras])

print(f"\n✅ Estantes JSON (primeiros 200 chars):")
print(f"   {estantes_json[:200]}...")

print(f"\n✅ Prateleiras JSON (primeiros 200 chars):")
print(f"   {prateleiras_json[:200]}...")

print("\n" + "=" * 80)
print("TESTE: Selecione Corredor ID=1, deve mostrar estantes com corredor_id=1")
print("=" * 80)

corredor_teste = 1
estantes_filtradas = [e for e in estantes if e['corredor_id'] == corredor_teste]
print(f"\nEstantes do corredor {corredor_teste}:")
for e in estantes_filtradas[:5]:
    print(f"   ID={e['id']}, Descrição={e['descricao']}")

if estantes_filtradas:
    estante_teste = estantes_filtradas[0]['id']
    prateleiras_filtradas = [p for p in prateleiras if p['estante_id'] == estante_teste]
    print(f"\nPrateleiras da estante {estante_teste}:")
    for p in prateleiras_filtradas[:5]:
        print(f"   ID={p['id']}, Descrição={p['descricao']}")

print("\n" + "=" * 80)
