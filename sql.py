
import json
import os
import oracledb
import pandas as pd
from datetime import datetime

DB_USER = os.getenv("ORACLE_USER", "rm572019")
DB_PASSWORD = os.getenv("ORACLE_PASSWORD", "070108")
DB_DSN = os.getenv("ORACLE_DSN", "oracle.fiap.com.br:1521/ORCL")

# Usuario padrao para vincular Historico_acoes.Usuario_id_usuario (FK obrigatoria)
USUARIO_ATUAL_ID = 1


def conectar_banco():
    """Tenta conectar no Oracle e retorna a conexao ou None (modo local)."""
    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        return conn
    except Exception as erro:
        print(f"\n[AVISO] Nao foi possivel conectar ao Oracle ({erro}).")
        print("[AVISO] O programa seguira em MODO LOCAL (memoria). O CRUD local, JSON e API continuam funcionando.")
        return None

# Retorno: connection do oracledb ou None se falhar.


def obter_proximo_id(cursor, tabela: str, coluna_id: str) -> int:
    cursor.execute(f"SELECT NVL(MAX({coluna_id}), 0) + 1 FROM {tabela}")
    row = cursor.fetchone()
    return int(row[0]) if row else 1

# Recebe cursor, tabela e coluna e retorna o proximo ID (MAX+1). Necessario porque o
# modelo SQL nao usa IDENTITY/SEQUENCE automatica.


def garantir_usuario_base(conn) -> int:
    """Garante que exista ao menos o Usuario 1 para satisfazer as FKs. Retorna o ID."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, nr_pontos FROM Usuario WHERE id_usuario = :1", [USUARIO_ATUAL_ID])
        row = cur.fetchone()
        if row:
            cur.close()
            return USUARIO_ATUAL_ID
        cur.execute(
            "INSERT INTO Usuario (id_usuario, nm_usuario, ds_email, ds_senha, nr_pontos) "
            "VALUES (:1, :2, :3, :4, :5)",
            [USUARIO_ATUAL_ID, "Jogador SoulUp", "jogador@soulup.com", "123", 0],
        )
        conn.commit()
        cur.close()
        print("[BANCO] Usuario base (ID 1) criado automaticamente.")
        return USUARIO_ATUAL_ID
    except Exception as erro:
        print(f"[BANCO] Aviso ao garantir usuario base: {erro}")
        return USUARIO_ATUAL_ID

# Retorno: ID do usuario base.


# ---------------- CRUD: Usuario ----------------

def db_inserir_usuario(conn, nome: str, email: str, senha: str, pontos: int = 0) -> int:
    try:
        cur = conn.cursor()
        novo_id = obter_proximo_id(cur, "Usuario", "id_usuario")
        cur.execute(
            "INSERT INTO Usuario (id_usuario, nm_usuario, ds_email, ds_senha, nr_pontos) "
            "VALUES (:1, :2, :3, :4, :5)",
            [novo_id, nome, email, senha, pontos],
        )
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao inserir usuario: {erro}")
        return 0
    else:
        print(f"Usuario '{nome}' inserido com ID {novo_id}.")
        return novo_id
    finally:
        pass

# Recebe os dados e insere um Usuario. Retorna o novo ID ou 0 em caso de erro.


def db_listar_usuarios(conn) -> list:
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, nm_usuario, ds_email, nr_pontos FROM Usuario ORDER BY id_usuario")
        rows = cur.fetchall()
        cur.close()
    except Exception as erro:
        print(f"Erro ao consultar usuarios: {erro}")
        return []
    else:
        if not rows:
            print("Nenhum usuario cadastrado.")
            return []
        try:
            df = pd.DataFrame(rows, columns=["Id", "Nome", "Email", "Pontos"])
            print(df.to_string(index=False))
        except Exception:
            for r in rows:
                print(f"Id={r[0]} | Nome={r[1]} | Email={r[2]} | Pontos={r[3]}")
        return [{"id_usuario": r[0], "nm_usuario": r[1], "ds_email": r[2], "nr_pontos": r[3]} for r in rows]
    finally:
        pass

# Consulta todos os Usuarios, exibe e retorna lista de dicts (usada tambem no export JSON).


def db_atualizar_usuario(conn, id_usuario: int, nome: str, email: str, pontos: int) -> bool:
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM Usuario WHERE id_usuario = :1", [id_usuario])
        if not cur.fetchone():
            print("Id inexistente.")
            cur.close()
            return False
        cur.execute(
            "UPDATE Usuario SET nm_usuario = :1, ds_email = :2, nr_pontos = :3 WHERE id_usuario = :4",
            [nome, email, pontos, id_usuario],
        )
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao atualizar usuario: {erro}")
        return False
    else:
        print("Usuario atualizado com sucesso.")
        return True
    finally:
        pass

# Recebe ID + novos dados e atualiza o Usuario. Retorna True/False.


def db_excluir_usuario(conn, id_usuario: int) -> bool:
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM Usuario WHERE id_usuario = :1", [id_usuario])
        if not cur.fetchone():
            print("Id inexistente.")
            cur.close()
            return False
        cur.execute("DELETE FROM Usuario WHERE id_usuario = :1", [id_usuario])
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao excluir usuario (verifique FKs em Historico/Avatar/Selo): {erro}")
        return False
    else:
        print("Usuario excluido com sucesso.")
        return True
    finally:
        pass

# Recebe o ID e exclui o Usuario. Retorna True/False.


# ---------------- CRUD: Missao ----------------

def db_inserir_missao(conn, descricao: str, pontuacao: int, nivel: int) -> int:
    try:
        if not (0 <= pontuacao <= 100):
            raise Exception("Pontuacao deve estar entre 0 e 100 (CHECK do banco).")
        if nivel <= 0:
            raise Exception("Nivel deve ser maior que 0 (CHECK do banco).")
        cur = conn.cursor()
        novo_id = obter_proximo_id(cur, "Missao", "id_missao")
        cur.execute(
            "INSERT INTO Missao (id_missao, ds_descricao, nr_pontuacao, nr_nivel) VALUES (:1, :2, :3, :4)",
            [novo_id, descricao, pontuacao, nivel],
        )
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao inserir missao: {erro}")
        return 0
    else:
        print(f"Missao inserida com ID {novo_id}.")
        return novo_id
    finally:
        pass

# Recebe descricao/pontuacao/nivel e insere uma Missao. Retorna novo ID ou 0.


def db_listar_missoes(conn) -> list:
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_missao, ds_descricao, nr_pontuacao, nr_nivel FROM Missao ORDER BY id_missao")
        rows = cur.fetchall()
        cur.close()
    except Exception as erro:
        print(f"Erro ao consultar missoes: {erro}")
        return []
    else:
        if not rows:
            print("Nenhuma missao cadastrada.")
            return []
        try:
            df = pd.DataFrame(rows, columns=["Id", "Descricao", "Pontos", "Nivel"])
            print(df.to_string(index=False))
        except Exception:
            for r in rows:
                print(f"Id={r[0]} | {r[1]} | {r[2]} pts | Nivel {r[3]}")
        return [{"id_missao": r[0], "ds_descricao": r[1], "nr_pontuacao": r[2], "nr_nivel": r[3]} for r in rows]
    finally:
        pass

# Consulta todas as Missoes, exibe e retorna lista de dicts.


def db_atualizar_missao(conn, id_missao: int, descricao: str, pontuacao: int, nivel: int) -> bool:
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_missao FROM Missao WHERE id_missao = :1", [id_missao])
        if not cur.fetchone():
            print("Id inexistente.")
            cur.close()
            return False
        cur.execute(
            "UPDATE Missao SET ds_descricao = :1, nr_pontuacao = :2, nr_nivel = :3 WHERE id_missao = :4",
            [descricao, pontuacao, nivel, id_missao],
        )
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao atualizar missao: {erro}")
        return False
    else:
        print("Missao atualizada com sucesso.")
        return True
    finally:
        pass

# Recebe ID + novos dados e atualiza a Missao. Retorna True/False.


def db_excluir_missao(conn, id_missao: int) -> bool:
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_missao FROM Missao WHERE id_missao = :1", [id_missao])
        if not cur.fetchone():
            print("Id inexistente.")
            cur.close()
            return False
        cur.execute("DELETE FROM Missao WHERE id_missao = :1", [id_missao])
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao excluir missao: {erro}")
        return False
    else:
        print("Missao excluida com sucesso.")
        return True
    finally:
        pass

# Recebe o ID e exclui a Missao. Retorna True/False.


# ---------------- CRUD: Historico_acoes ----------------

def db_inserir_historico(conn, pontuacao: int, id_usuario: int = USUARIO_ATUAL_ID) -> int:
    try:
        if not (0 <= pontuacao <= 100):
            raise Exception("Pontuacao deve estar entre 0 e 100 (CHECK do banco).")
        cur = conn.cursor()
        novo_id = obter_proximo_id(cur, "Historico_acoes", "id_historico")
        cur.execute(
            "INSERT INTO Historico_acoes (id_historico, dt_historico, nr_pontuacao, Usuario_id_usuario) "
            "VALUES (:1, SYSDATE, :2, :3)",
            [novo_id, pontuacao, id_usuario],
        )
        cur.execute(
            "UPDATE Usuario SET nr_pontos = nr_pontos + :1 WHERE id_usuario = :2",
            [pontuacao, id_usuario],
        )
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao inserir historico: {erro}")
        return 0
    else:
        print(f"Historico inserido com ID {novo_id} (+{pontuacao} pts no usuario {id_usuario}).")
        return novo_id
    finally:
        pass

# Recebe pontuacao e insere no Historico_acoes somando pontos no Usuario. Retorna novo ID ou 0.


def db_listar_historico_db(conn) -> list:
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id_historico, dt_historico, nr_pontuacao, Usuario_id_usuario "
            "FROM Historico_acoes ORDER BY id_historico"
        )
        rows = cur.fetchall()
        cur.close()
    except Exception as erro:
        print(f"Erro ao consultar historico: {erro}")
        return []
    else:
        if not rows:
            print("Historico vazio no banco.")
            return []
        try:
            df = pd.DataFrame(rows, columns=["Id", "Data", "Pontos", "IdUsuario"])
            print(df.to_string(index=False))
        except Exception:
            for r in rows:
                print(f"Id={r[0]} | Data={r[1]} | {r[2]} pts | Usuario={r[3]}")
        return [
            {"id_historico": r[0], "dt_historico": str(r[1]), "nr_pontuacao": r[2], "Usuario_id_usuario": r[3]}
            for r in rows
        ]
    finally:
        pass

# Consulta o Historico_acoes, exibe e retorna lista de dicts.


def db_atualizar_historico_db(conn, id_historico: int, nova_pontuacao: int) -> bool:
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT nr_pontuacao, Usuario_id_usuario FROM Historico_acoes WHERE id_historico = :1",
            [id_historico],
        )
        row = cur.fetchone()
        if not row:
            print("Id inexistente.")
            cur.close()
            return False
        pontos_antigos, id_usuario = row
        diferenca = nova_pontuacao - pontos_antigos
        cur.execute(
            "UPDATE Historico_acoes SET nr_pontuacao = :1 WHERE id_historico = :2",
            [nova_pontuacao, id_historico],
        )
        cur.execute(
            "UPDATE Usuario SET nr_pontos = GREATEST(0, nr_pontos + :1) WHERE id_usuario = :2",
            [diferenca, id_usuario],
        )
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao atualizar historico: {erro}")
        return False
    else:
        print("Historico atualizado e pontos do usuario ajustados.")
        return True
    finally:
        pass

# Recebe ID + nova pontuacao, atualiza o registro e ajusta o saldo do Usuario. Retorna True/False.


def db_excluir_historico_db(conn, id_historico: int) -> bool:
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT nr_pontuacao, Usuario_id_usuario FROM Historico_acoes WHERE id_historico = :1",
            [id_historico],
        )
        row = cur.fetchone()
        if not row:
            print("Id inexistente.")
            cur.close()
            return False
        pontos, id_usuario = row
        cur.execute("DELETE FROM Historico_acoes WHERE id_historico = :1", [id_historico])
        cur.execute(
            "UPDATE Usuario SET nr_pontos = GREATEST(0, nr_pontos - :1) WHERE id_usuario = :2",
            [pontos, id_usuario],
        )
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao excluir historico: {erro}")
        return False
    else:
        print("Historico excluido e pontos estornados do usuario.")
        return True
    finally:
        pass

# Recebe o ID, exclui o registro e estorna os pontos do Usuario. Retorna True/False.


# ---------------- CRUD: Carta ----------------

def db_inserir_carta(conn, nome: str, descricao: str, conjunto: str, raridade: str) -> int:
    try:
        cur = conn.cursor()
        novo_id = obter_proximo_id(cur, "Carta", "id_carta")
        cur.execute(
            "INSERT INTO Carta (id_carta, nm_carta, ds_carta, nm_conjunto, ds_raridade) "
            "VALUES (:1, :2, :3, :4, :5)",
            [novo_id, nome, descricao, conjunto, raridade],
        )
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao inserir carta: {erro}")
        return 0
    else:
        print(f"Carta '{nome}' inserida com ID {novo_id}.")
        return novo_id
    finally:
        pass

# Recebe os dados e insere uma Carta. Retorna novo ID ou 0.


def db_listar_cartas(conn) -> list:
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_carta, nm_carta, ds_carta, nm_conjunto, ds_raridade FROM Carta ORDER BY id_carta")
        rows = cur.fetchall()
        cur.close()
    except Exception as erro:
        print(f"Erro ao consultar cartas: {erro}")
        return []
    else:
        if not rows:
            print("Nenhuma carta cadastrada no banco.")
            return []
        try:
            df = pd.DataFrame(rows, columns=["Id", "Nome", "Descricao", "Conjunto", "Raridade"])
            print(df.to_string(index=False))
        except Exception:
            for r in rows:
                print(f"Id={r[0]} | {r[1]} ({r[4]}) - {r[3]}")
        return [
            {"id_carta": r[0], "nm_carta": r[1], "ds_carta": r[2], "nm_conjunto": r[3], "ds_raridade": r[4]}
            for r in rows
        ]
    finally:
        pass

# Consulta todas as Cartas, exibe e retorna lista de dicts.


def db_atualizar_carta(conn, id_carta: int, nome: str, descricao: str, conjunto: str, raridade: str) -> bool:
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_carta FROM Carta WHERE id_carta = :1", [id_carta])
        if not cur.fetchone():
            print("Id inexistente.")
            cur.close()
            return False
        cur.execute(
            "UPDATE Carta SET nm_carta = :1, ds_carta = :2, nm_conjunto = :3, ds_raridade = :4 WHERE id_carta = :5",
            [nome, descricao, conjunto, raridade, id_carta],
        )
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao atualizar carta: {erro}")
        return False
    else:
        print("Carta atualizada com sucesso.")
        return True
    finally:
        pass

# Recebe ID + novos dados e atualiza a Carta. Retorna True/False.


def db_excluir_carta(conn, id_carta: int) -> bool:
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_carta FROM Carta WHERE id_carta = :1", [id_carta])
        if not cur.fetchone():
            print("Id inexistente.")
            cur.close()
            return False
        cur.execute("DELETE FROM Carta WHERE id_carta = :1", [id_carta])
        conn.commit()
        cur.close()
    except Exception as erro:
        print(f"Erro ao excluir carta: {erro}")
        return False
    else:
        print("Carta excluida com sucesso.")
        return True
    finally:
        pass

# Recebe o ID e exclui a Carta. Retorna True/False.


def salvar_acao_no_banco(conn, pontos: int, id_usuario: int = USUARIO_ATUAL_ID) -> int:
    """Persiste uma acao do jogo no banco (Historico + Usuario). Retorna ID ou 0."""
    if conn is None:
        return 0
    try:
        return db_inserir_historico(conn, pontos, id_usuario)
    except Exception as erro:
        print(f"[BANCO] Falha ao salvar acao: {erro}")
        return 0

# Recebe conexao e pontos, grava no Historico_acoes e soma no Usuario.


# ---------------- Exportacao JSON ----------------

def exportar_para_json(dados, nome_arquivo: str) -> str:
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
    except Exception as erro:
        print(f"Erro ao exportar JSON: {erro}")
        return ""
    else:
        print(f"Arquivo '{nome_arquivo}' exportado com sucesso ({len(dados) if isinstance(dados, list) else 1} registro(s)).")
        return nome_arquivo
    finally:
        pass

# Recebe dados (list/dict) e salva em JSON. Retorna o nome do arquivo ou "".


def exportar_consulta_json(conn, tabela: str, nome_arquivo: str) -> str:
    """Exporta SELECT * de uma tabela do banco para JSON. Retorna o nome do arquivo."""
    tabelas_permitidas = {"Usuario": "SELECT * FROM Usuario ORDER BY id_usuario",
                          "Missao": "SELECT * FROM Missao ORDER BY id_missao",
                          "Historico_acoes": "SELECT * FROM Historico_acoes ORDER BY id_historico",
                          "Carta": "SELECT * FROM Carta ORDER BY id_carta"}
    if tabela not in tabelas_permitidas:
        print(f"Tabela '{tabela}' nao permitida para exportacao.")
        return ""
    try:
        cur = conn.cursor()
        cur.execute(tabelas_permitidas[tabela])
        cols = [d[0].lower() for d in cur.description]
        rows = cur.fetchall()
        cur.close()
        dados = [dict(zip(cols, r)) for r in rows]
        return exportar_para_json(dados, nome_arquivo)
    except Exception as erro:
        print(f"Erro ao exportar '{tabela}': {erro}")
        return ""
    finally:
        pass

# Recebe conexao, tabela e nome do arquivo; consulta o banco e exporta para JSON.


def exportar_estado_local_json(colecao: dict, fragmentos: int, creditos_colecao: int,
                               pontos_ecoa: int, pontos_resgatados: int,
                               historico: list, nome_arquivo: str = "soulup_export_local.json") -> str:
    dados = {
        "exportado_em": datetime.now().isoformat(timespec="seconds"),
        "pontos_ecoa": pontos_ecoa,
        "pontos_resgatados": pontos_resgatados,
        "nivel": _nivel_local(pontos_ecoa),
        "fragmentos": fragmentos,
        "creditos_colecao": creditos_colecao,
        "colecao": colecao,
        "historico": [{"acao": a, "pontos": p} for a, p in historico],
    }
    return exportar_para_json(dados, nome_arquivo)

# Recebe o estado do jogo em memoria e exporta para JSON. Retorna o nome do arquivo.



def _nivel_local(pontos: int) -> str:
    try:
        from soulup import identificar_nivel
        return identificar_nivel(pontos)
    except Exception:
        if pontos < 100:
            return "Semente"
        elif pontos < 300:
            return "Broto"
        elif pontos < 600:
            return "Arvore"
        return "Expert"

# Retorno: nivel (import lazy para evitar import circular).
