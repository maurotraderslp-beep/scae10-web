"""Verificar dados completos do aluno 4"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from alunos.models import Aluno

try:
    aluno = Aluno.objects.get(id=4)
    
    print("=" * 80)
    print(f"DADOS COMPLETOS DO ALUNO ID 4")
    print("=" * 80)
    print()
    
    campos_preenchidos = 0
    campos_vazios = []
    
    # Dados Básicos
    print("📋 DADOS BÁSICOS:")
    print(f"  Nome: {aluno.nome}")
    campos_preenchidos += 1
    
    if aluno.data_nascimento:
        print(f"  Data Nascimento: {aluno.data_nascimento}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("data_nascimento")
    
    if aluno.nome_mae:
        print(f"  Nome Mãe: {aluno.nome_mae}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("nome_mae")
    
    if aluno.nome_pai:
        print(f"  Nome Pai: {aluno.nome_pai}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("nome_pai")
    print()
    
    # Documentos
    print("📄 DOCUMENTOS:")
    if aluno.cpf:
        print(f"  CPF: {aluno.cpf}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("cpf")
    
    if aluno.rg:
        print(f"  RG: {aluno.rg}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("rg")
    
    if aluno.cor_raca:
        print(f"  Cor/Raça: {aluno.cor_raca}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("cor_raca")
    print()
    
    # Endereço
    print("📍 ENDEREÇO:")
    if aluno.endereco:
        print(f"  Endereço: {aluno.endereco}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("endereco")
    
    if aluno.bairro:
        print(f"  Bairro: {aluno.bairro}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("bairro")
    
    if aluno.cidade:
        print(f"  Cidade: {aluno.cidade}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("cidade")
    
    if aluno.estado:
        print(f"  Estado: {aluno.estado}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("estado")
    print()
    
    # Contato
    print("📞 CONTATO:")
    if aluno.telefone:
        print(f"  Telefone: {aluno.telefone}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("telefone")
    
    if aluno.email:
        print(f"  Email: {aluno.email}")
        campos_preenchidos += 1
    else:
        campos_vazios.append("email")
    print()
    
    print("=" * 80)
    print(f"RESUMO:")
    print(f"  Campos preenchidos: {campos_preenchidos}")
    print(f"  Campos vazios: {len(campos_vazios)}")
    if campos_vazios:
        print(f"  Vazios: {', '.join(campos_vazios[:10])}")
    print("=" * 80)
    
except Aluno.DoesNotExist:
    print("❌ Aluno ID 4 não encontrado!")
