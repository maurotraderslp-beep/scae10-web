"""Restaurar dados do aluno 4 do banco do Delphi"""
import fdb

print("=" * 80)
print("RESTAURANDO DADOS DO ALUNO 4 DO BANCO DELPHI")
print("=" * 80)
print()

# Conectar ao banco do Delphi
delphi_db = r'c:\sysflor\ArquivoMortoEscolar\database\SCAE.FDB'
print(f"Banco Delphi: {delphi_db}")
print()

try:
    conn_delphi = fdb.connect(
        dsn=delphi_db,
        user='SYSDBA',
        password='masterkey',
        charset='WIN1252',
        port=3025
    )
    cursor_delphi = conn_delphi.cursor()
    
    # Buscar dados do aluno 4 no banco do Delphi
    cursor_delphi.execute("SELECT * FROM ALUNOS WHERE ID = 4")
    row_delphi = cursor_delphi.fetchone()
    columns = [desc[0] for desc in cursor_delphi.description]
    
    print("✅ Dados encontrados no banco Delphi:")
    print("-" * 80)
    
    campos_preenchidos = {}
    for col, val in zip(columns, row_delphi):
        if val is not None and val != '':
            campos_preenchidos[col] = val
            print(f"  {col}: {val}")
    
    print("-" * 80)
    print(f"Total de campos preenchidos: {len(campos_preenchidos)}")
    print()
    
    cursor_delphi.close()
    conn_delphi.close()
    
    # Agora conectar ao banco atual e atualizar
    print("Atualizando banco atual...")
    conn_atual = fdb.connect(
        dsn=r'c:\sysflor\scae10-python\database\SCAE.FDB',
        user='SYSDBA',
        password='masterkey',
        charset='WIN1252',
        port=3025
    )
    cursor_atual = conn_atual.cursor()
    
    # Criar UPDATE dinâmico
    update_fields = []
    update_values = []
    
    for col, val in campos_preenchidos.items():
        # Pular campos de controle (manter foto nova e data atualizacao)
        if col in ['ID', 'DATA_CADASTRO', 'DATA_ALTERACAO', 'FOTO_PATH']:
            continue
        
        update_fields.append(f"{col} = ?")
        update_values.append(val)
    
    if update_fields:
        update_sql = f"UPDATE ALUNOS SET {', '.join(update_fields)} WHERE ID = 4"
        
        print(f"\nCampos a atualizar ({len(update_values)}):")
        for val in update_values:
            print(f"  - {val}")
        print()
        
        resposta = input("Deseja continuar? (S/N): ")
        if resposta.upper() != 'S':
            print("❌ Cancelado pelo usuário")
        else:
            # Executar update
            cursor_atual.execute(update_sql, update_values)
            conn_atual.commit()
            
            print("\n✅ Dados restaurados com sucesso!")
            print()
            
            # Verificar
            cursor_atual.execute("SELECT * FROM ALUNOS WHERE ID = 4")
            row_atual = cursor_atual.fetchone()
            
            print("Confirmação - dados atuais:")
            for col, val in zip(columns, row_atual):
                if val is not None and val != '':
                    print(f"  ✅ {col}: {val}")
            
            cursor_atual.close()
            conn_atual.close()
    else:
        print("⚠️ Nenhum campo para atualizar")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
