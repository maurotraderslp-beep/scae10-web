"""Restaurar dados do aluno 4 do backup"""
import fdb

print("=" * 80)
print("RESTAURANDO DADOS DO ALUNO 4 DO BACKUP")
print("=" * 80)
print()

# Conectar ao backup
backup_path = r'c:\sysflor\BACKUPS_BANCO\SCAE_BACKUP_SEGURO_20260417_224409.FDB'
print(f"Backup: {backup_path}")
print()

try:
    conn_backup = fdb.connect(
        dsn=backup_path,
        user='SYSDBA',
        password='masterkey',
        charset='WIN1252'
    )
    cursor_backup = conn_backup.cursor()
    
    # Buscar dados do aluno 4 no backup
    cursor_backup.execute("SELECT * FROM ALUNOS WHERE ID = 4")
    row_backup = cursor_backup.fetchone()
    columns = [desc[0] for desc in cursor_backup.description]
    
    print("✅ Dados encontrados no backup:")
    print("-" * 80)
    
    campos_preenchidos = {}
    for col, val in zip(columns, row_backup):
        if val is not None and val != '':
            campos_preenchidos[col] = val
            print(f"  {col}: {val}")
    
    print("-" * 80)
    print(f"Total de campos preenchidos: {len(campos_preenchidos)}")
    print()
    
    cursor_backup.close()
    conn_backup.close()
    
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
        # Pular campos de controle
        if col in ['ID', 'DATA_CADASTRO', 'DATA_ALTERACAO', 'FOTO_PATH']:
            continue
        
        update_fields.append(f"{col} = ?")
        update_values.append(val)
    
    if update_fields:
        update_sql = f"UPDATE ALUNOS SET {', '.join(update_fields)} WHERE ID = 4"
        
        print(f"\nSQL de atualização:")
        print(f"  {update_sql}")
        print(f"\nValores ({len(update_values)} campos):")
        for col, val in zip(campos_preenchidos.keys(), update_values):
            if col not in ['ID', 'DATA_CADASTRO', 'DATA_ALTERACAO', 'FOTO_PATH']:
                print(f"  {col}: {val}")
        print()
        
        # Executar update
        cursor_atual.execute(update_sql, update_values)
        conn_atual.commit()
        
        print("✅ Dados restaurados com sucesso!")
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
