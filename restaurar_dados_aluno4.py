"""Restaurar dados perdidos do aluno 4 - copia todos os campos do banco Delphi"""
import fdb

print("=" * 80)
print("RESTAURANDO DADOS DO ALUNO 4 DO BANCO DELPHI")
print("=" * 80)
print()

delphi_db = r'c:\sysflor\ArquivoMortoEscolar\database\SCAE.FDB'
web_db = r'c:\sysflor\scae10-python\database\SCAE.FDB'

try:
    # Conectar ao banco do Delphi (origem)
    print("1. Conectando ao banco Delphi...")
    conn_delphi = fdb.connect(
        dsn=delphi_db,
        user='SYSDBA',
        password='masterkey',
        charset='WIN1252',
        port=3025
    )
    cursor_delphi = conn_delphi.cursor()
    print("   ✅ Conectado!")
    print()
    
    # Buscar dados do aluno 4
    print("2. Buscando dados do aluno 4 no Delphi...")
    cursor_delphi.execute("SELECT * FROM ALUNOS WHERE ID = 4")
    row_delphi = cursor_delphi.fetchone()
    columns = [desc[0] for desc in cursor_delphi.description]
    
    # Criar dicionário com todos os campos preenchidos
    dados_delphi = {}
    for col, val in zip(columns, row_delphi):
        if val is not None and val != '':
            dados_delphi[col] = val
    
    print(f"   ✅ {len(dados_delphi)} campos encontrados")
    print()
    
    cursor_delphi.close()
    conn_delphi.close()
    print("   ✅ Conexão Delphi fechada")
    print()
    
    # Conectar ao banco web (destino)
    print("3. Conectando ao banco Web...")
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
    
    # Buscar dados atuais do aluno 4 (para manter a foto nova)
    print("4. Buscando dados atuais (para preservar foto)...")
    cursor_web.execute("SELECT FOTO_PATH FROM ALUNOS WHERE ID = 4")
    foto_atual = cursor_web.fetchone()[0]
    print(f"   ✅ Foto atual: {foto_atual}")
    print()
    
    # Criar UPDATE com TODOS os campos do Delphi (exceto FOTO_PATH e datas de controle)
    print("5. Preparando restauração...")
    campos_update = []
    valores = []
    
    campos_ignore = ['ID', 'DATA_CADASTRO', 'DATA_ALTERACAO', 'FOTO_PATH']
    
    for col, val in dados_delphi.items():
        if col not in campos_ignore:
            campos_update.append(f"{col} = ?")
            valores.append(val)
    
    # Manter a foto nova
    if foto_atual:
        campos_update.append("FOTO_PATH = ?")
        valores.append(foto_atual)
    
    valores.append(4)  # ID do aluno
    
    update_sql = f"UPDATE ALUNOS SET {', '.join(campos_update)} WHERE ID = 4"
    
    print(f"   📝 Campos a atualizar: {len(campos_update)}")
    print()
    
    print("6. Executando atualização...")
    cursor_web.execute(update_sql, valores)
    conn_web.commit()
    print("   ✅ Dados restaurados!")
    print()
    
    # Verificar
    print("7. Verificando dados restaurados...")
    cursor_web.execute("SELECT * FROM ALUNOS WHERE ID = 4")
    row_final = cursor_web.fetchone()
    
    campos_preenchidos = sum(1 for val in row_final if val is not None and val != '')
    print(f"   ✅ Total de campos preenchidos: {campos_preenchidos}")
    print()
    
    print("Principais campos:")
    important_cols = ['NOME', 'DATA_NASCIMENTO', 'NOME_MAE', 'NOME_PAI', 'TURMA', 'FOTO_PATH']
    for col, val in zip(columns, row_final):
        if col in important_cols and val:
            print(f"   ✅ {col}: {val}")
    
    cursor_web.close()
    conn_web.close()
    
    print()
    print("=" * 80)
    print("✅ RESTAURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
