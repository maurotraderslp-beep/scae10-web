"""Restaurar dados do aluno 4 - copia banco primeiro para evitar lock"""
import fdb
import shutil
import os

print("=" * 80)
print("RESTAURANDO DADOS DO ALUNO 4 (CÓPIA TEMPORÁRIA)")
print("=" * 80)
print()

delphi_db = r'c:\sysflor\ArquivoMortoEscolar\database\SCAE.FDB'
temp_db = r'c:\sysflor\temp_scae.fdb'
web_db = r'c:\sysflor\scae10-python\database\SCAE.FDB'

try:
    # Copiar banco do Delphi para temp
    print("1. Copiando banco do Delphi para temporário...")
    if os.path.exists(temp_db):
        os.remove(temp_db)
    shutil.copy2(delphi_db, temp_db)
    print(f"   ✅ Copiado: {temp_db}")
    print()
    
    # Conectar ao temp
    print("2. Conectando ao banco temporário...")
    conn_temp = fdb.connect(
        dsn=temp_db,
        user='SYSDBA',
        password='masterkey',
        charset='WIN1252',
        port=3025
    )
    cursor_temp = conn_temp.cursor()
    print("   ✅ Conectado!")
    print()
    
    # Buscar dados do aluno 4
    print("3. Buscando dados do aluno 4...")
    cursor_temp.execute("SELECT * FROM ALUNOS WHERE ID = 4")
    row_delphi = cursor_temp.fetchone()
    columns = [desc[0] for desc in cursor_temp.description]
    
    dados_delphi = {}
    for col, val in zip(columns, row_delphi):
        if val is not None and val != '':
            dados_delphi[col] = val
    
    print(f"   ✅ {len(dados_delphi)} campos encontrados")
    print()
    
    # Mostrar dados importantes
    print("   Dados encontrados:")
    important = ['NOME', 'DATA_NASCIMENTO', 'NOME_MAE', 'NOME_PAI', 'TURMA', 'SITUACAO']
    for col in important:
        if col in dados_delphi:
            print(f"     {col}: {dados_delphi[col]}")
    print()
    
    cursor_temp.close()
    conn_temp.close()
    
    # Conectar ao banco web
    print("4. Conectando ao banco Web...")
    conn_web = fdb.connect(
        dsn=web_db,
        user='SYSDBA',
        password='masterkey',
        charset='WIN1252',
        port=3025
    )
    cursor_web = conn_web.cursor()
    print("   ✅ Conectado!")
    print()
    
    # Manter foto atual
    print("5. Verificando foto atual...")
    cursor_web.execute("SELECT FOTO_PATH FROM ALUNOS WHERE ID = 4")
    foto_atual = cursor_web.fetchone()[0]
    print(f"   ✅ Foto atual: {foto_atual}")
    print()
    
    # Criar UPDATE
    print("6. Restaurando dados...")
    campos_update = []
    valores = []
    
    campos_ignore = ['ID', 'DATA_CADASTRO', 'DATA_ALTERACAO', 'FOTO_PATH']
    
    for col, val in dados_delphi.items():
        if col not in campos_ignore:
            campos_update.append(f"{col} = ?")
            valores.append(val)
    
    # Manter foto
    if foto_atual:
        campos_update.append("FOTO_PATH = ?")
        valores.append(foto_atual)
    
    valores.append(4)
    
    update_sql = f"UPDATE ALUNOS SET {', '.join(campos_update)} WHERE ID = 4"
    cursor_web.execute(update_sql, valores)
    conn_web.commit()
    print("   ✅ Dados restaurados!")
    print()
    
    # Verificar
    print("7. Verificando restauração...")
    cursor_web.execute("SELECT * FROM ALUNOS WHERE ID = 4")
    row_final = cursor_web.fetchone()
    
    campos_preenchidos = sum(1 for val in row_final if val is not None and val != '')
    print(f"   ✅ Total de campos preenchidos: {campos_preenchidos}")
    print()
    
    print("   Principais campos:")
    for col, val in zip(columns, row_final):
        if col in important and val:
            print(f"     ✅ {col}: {val}")
    
    cursor_web.close()
    conn_web.close()
    
    # Limpar temp
    if os.path.exists(temp_db):
        os.remove(temp_db)
        print()
        print(f"   🗑️ Arquivo temporário removido")
    
    print()
    print("=" * 80)
    print("✅ RESTAURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    
    # Limpar temp em caso de erro
    if os.path.exists(temp_db):
        try:
            os.remove(temp_db)
        except:
            pass
