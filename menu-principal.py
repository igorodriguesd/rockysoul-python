from soulup import *
from sql import *
from api import *


def mostrar_menu(pontos_ecoa: int, pontos_resgatados: int, colecao: dict, fragmentos: int, creditos_colecao: int, conn=None) -> None:
    nivel = identificar_nivel(pontos_ecoa)
    modo = "ORACLE" if conn is not None else "LOCAL"

    print("\n=== DASHBOARD SOULUP ===")
    print(f"[ Modo: {modo} | Pontos Disponiveis: {pontos_ecoa} | Ja Resgatados: {pontos_resgatados} | Nivel: {nivel} ]")
    print(f"[ Cartas: {len(colecao)}/20 | Fragmentos: {fragmentos} | Creditos de Colecao: {creditos_colecao} ]")
    print("---------------------------------------------------------------------------")
    print("1 - Registrar acao sustentavel (Criar)")
    print("2 - Ver Meu Nivel e Estatisticas")
    print("3 - Resgatar Recompensas (Beneficios Reais)")
    print("4 - Sugestao do Avatar")
    print("5 - Ver Ranking da Semana")
    print("6 - Gerenciar Historico de Acoes (CRUD local)")
    print("7 - Ver Minha Colecao de Cartas")
    print("8 - Fabrica de Cartas (Trocar Fragmentos)")
    print("9 - CRUD Banco de Dados Oracle [10 pts: menus/submenus]")
    print("10 - Exportar consultas para JSON [30 pts]")
    print("11 - Consultar API Externa Publica [20 pts]")
    print("12 - Sair")

# Retorno: None
# Mostra o menu principal e as informacoes do usuario, incluindo modo Oracle/Local.


def gerenciar_historico(acoes: list, pontos_ecoa: int, historico: list) -> int:
    print("\n--- GERENCIAR HISTORICO (local) ---")
    print("1 - Listar")
    print("2 - Editar")
    print("3 - Excluir")
    print("4 - Voltar")

    opcao = validar_opcao_numerica("Escolha: ", 1, 4)

    if opcao == 1:
        listar_historico(historico)
    elif opcao == 2:
        pontos_ecoa = editar_acao_historico(acoes, pontos_ecoa, historico)
    elif opcao == 3:
        pontos_ecoa = excluir_acao_historico(pontos_ecoa, historico)

    return pontos_ecoa

# Retorno: o saldo de pontos atualizado (ou o mesmo saldo, se apenas listou ou voltou).
# Submenu de CRUD do historico de acoes (listar, editar, excluir).



def submenu_crud_usuarios(conn) -> None:
    while True:
        print("\n--- CRUD BANCO: Usuarios (tabela Usuario) ---")
        print("1 - Inserir usuario")
        print("2 - Consultar/Listar usuarios")
        print("3 - Alterar usuario")
        print("4 - Excluir usuario")
        print("5 - Voltar")
        opcao = validar_opcao_numerica("Escolha: ", 1, 5)
        if opcao == 1:
            try:
                nome = input("Nome: ")
                email = input("Email: ")
                senha = input("Senha: ")
                pontos = int(input("Pontos iniciais (0): ") or "0")
                db_inserir_usuario(conn, nome, email, senha, pontos)
            except Exception as e:
                print("Erro: ", e)
        elif opcao == 2:
            db_listar_usuarios(conn)
            input("\nENTER para continuar...")
        elif opcao == 3:
            try:
                db_listar_usuarios(conn)
                uid = int(input("Id do usuario: "))
                nome = input("Novo nome: ")
                email = input("Novo email: ")
                pontos = int(input("Novos pontos: "))
                db_atualizar_usuario(conn, uid, nome, email, pontos)
            except Exception as e:
                print("Erro: ", e)
        elif opcao == 4:
            try:
                db_listar_usuarios(conn)
                uid = int(input("Id do usuario: "))
                db_excluir_usuario(conn, uid)
            except Exception as e:
                print("Erro: ", e)
        else:
            break

# Retorno: None. Submenu com as 4 operacoes do CRUD de Usuario.


def submenu_crud_missoes(conn) -> None:
    while True:
        print("\n--- CRUD BANCO: Missoes (tabela Missao) ---")
        print("1 - Inserir missao")
        print("2 - Consultar/Listar missoes")
        print("3 - Alterar missao")
        print("4 - Excluir missao")
        print("5 - Voltar")
        opcao = validar_opcao_numerica("Escolha: ", 1, 5)
        if opcao == 1:
            try:
                desc = input("Descricao (ex: Reciclagem): ")
                pts = int(input("Pontuacao (0-100): "))
                nv = int(input("Nivel (>0): "))
                db_inserir_missao(conn, desc, pts, nv)
            except Exception as e:
                print("Erro: ", e)
        elif opcao == 2:
            db_listar_missoes(conn)
            input("\nENTER para continuar...")
        elif opcao == 3:
            try:
                db_listar_missoes(conn)
                mid = int(input("Id da missao: "))
                desc = input("Nova descricao: ")
                pts = int(input("Nova pontuacao (0-100): "))
                nv = int(input("Novo nivel: "))
                db_atualizar_missao(conn, mid, desc, pts, nv)
            except Exception as e:
                print("Erro: ", e)
        elif opcao == 4:
            try:
                db_listar_missoes(conn)
                mid = int(input("Id da missao: "))
                db_excluir_missao(conn, mid)
            except Exception as e:
                print("Erro: ", e)
        else:
            break

# Retorno: None. Submenu com as 4 operacoes do CRUD de Missao.


def submenu_crud_historico_db(conn) -> None:
    while True:
        print("\n--- CRUD BANCO: Historico (tabela Historico_acoes) ---")
        print("1 - Inserir registro (+ soma pontos no Usuario)")
        print("2 - Consultar/Listar historico")
        print("3 - Alterar pontuacao (ajusta saldo do Usuario)")
        print("4 - Excluir registro (estorna pontos do Usuario)")
        print("5 - Voltar")
        opcao = validar_opcao_numerica("Escolha: ", 1, 5)
        if opcao == 1:
            try:
                pts = int(input("Pontuacao (0-100): "))
                db_inserir_historico(conn, pts, USUARIO_ATUAL_ID)
            except Exception as e:
                print("Erro: ", e)
        elif opcao == 2:
            db_listar_historico_db(conn)
            input("\nENTER para continuar...")
        elif opcao == 3:
            try:
                db_listar_historico_db(conn)
                hid = int(input("Id do historico: "))
                pts = int(input("Nova pontuacao (0-100): "))
                db_atualizar_historico_db(conn, hid, pts)
            except Exception as e:
                print("Erro: ", e)
        elif opcao == 4:
            try:
                db_listar_historico_db(conn)
                hid = int(input("Id do historico: "))
                db_excluir_historico_db(conn, hid)
            except Exception as e:
                print("Erro: ", e)
        else:
            break

# Retorno: None. Submenu com as 4 operacoes do CRUD de Historico_acoes.


def submenu_crud_cartas(conn) -> None:
    while True:
        print("\n--- CRUD BANCO: Cartas (tabela Carta) ---")
        print("1 - Inserir carta")
        print("2 - Consultar/Listar cartas")
        print("3 - Alterar carta")
        print("4 - Excluir carta")
        print("5 - Voltar")
        opcao = validar_opcao_numerica("Escolha: ", 1, 5)
        if opcao == 1:
            try:
                nome = input("Nome da carta: ")
                desc = input("Descricao: ")
                conj = input("Conjunto (ex: Recursos): ")
                rar = input("Raridade (Comum/Incomum/Rara/Epica/Lendaria): ")
                db_inserir_carta(conn, nome, desc, conj, rar)
            except Exception as e:
                print("Erro: ", e)
        elif opcao == 2:
            db_listar_cartas(conn)
            input("\nENTER para continuar...")
        elif opcao == 3:
            try:
                db_listar_cartas(conn)
                cid = int(input("Id da carta: "))
                nome = input("Novo nome: ")
                desc = input("Nova descricao: ")
                conj = input("Novo conjunto: ")
                rar = input("Nova raridade: ")
                db_atualizar_carta(conn, cid, nome, desc, conj, rar)
            except Exception as e:
                print("Erro: ", e)
        elif opcao == 4:
            try:
                db_listar_cartas(conn)
                cid = int(input("Id da carta: "))
                db_excluir_carta(conn, cid)
            except Exception as e:
                print("Erro: ", e)
        else:
            break

# Retorno: None. Submenu com as 4 operacoes do CRUD de Carta.


def menu_crud_banco(conn) -> None:
    if conn is None:
        print("\n[CRUD BANCO] Sem conexao Oracle. Conecte-se para usar o CRUD no banco.")
        print("O CRUD local (opcao 6) continua disponivel.")
        input("ENTER para voltar...")
        return
    while True:
        print("\n=== CRUD BANCO DE DADOS ORACLE ===")
        print("1 - Usuarios")
        print("2 - Missoes")
        print("3 - Historico de acoes (banco)")
        print("4 - Cartas")
        print("5 - Voltar ao menu principal")
        opcao = validar_opcao_numerica("Escolha: ", 1, 5)
        if opcao == 1:
            submenu_crud_usuarios(conn)
        elif opcao == 2:
            submenu_crud_missoes(conn)
        elif opcao == 3:
            submenu_crud_historico_db(conn)
        elif opcao == 4:
            submenu_crud_cartas(conn)
        else:
            break

# Retorno: None. Menu que agrupa os submenus do CRUD (vale os 10 pts de menus/submenus).


def menu_exportar_json(conn, colecao_atual, fragmentos_atual, creditos_atual,
                        pontos_ecoa_atual, pontos_resgatados_atual, historico) -> None:
    while True:
        print("\n=== EXPORTAR CONSULTAS PARA JSON ===")
        print("1 - Exportar Usuarios (banco)")
        print("2 - Exportar Missoes (banco)")
        print("3 - Exportar Historico do banco")
        print("4 - Exportar Cartas (banco)")
        print("5 - Exportar estado local do jogo (colecao/historico/pontos)")
        print("6 - Exportar TUDO (banco + local)")
        print("7 - Voltar")
        opcao = validar_opcao_numerica("Escolha: ", 1, 7)
        if opcao == 7 or opcao == 0:
            break
        if opcao in (1, 2, 3, 4, 6) and conn is None:
            print("Sem conexao Oracle: exportacao do banco indisponivel. Use a opcao 5 (local).")
            continue
        if opcao == 1:
            exportar_consulta_json(conn, "Usuario", "usuarios.json")
        elif opcao == 2:
            exportar_consulta_json(conn, "Missao", "missoes.json")
        elif opcao == 3:
            exportar_consulta_json(conn, "Historico_acoes", "historico_banco.json")
        elif opcao == 4:
            exportar_consulta_json(conn, "Carta", "cartas.json")
        elif opcao == 5:
            exportar_estado_local_json(colecao_atual, fragmentos_atual, creditos_atual,
                                       pontos_ecoa_atual, pontos_resgatados_atual,
                                       historico, "soulup_export_local.json")
        elif opcao == 6:
            exportar_consulta_json(conn, "Usuario", "usuarios.json")
            exportar_consulta_json(conn, "Missao", "missoes.json")
            exportar_consulta_json(conn, "Historico_acoes", "historico_banco.json")
            exportar_consulta_json(conn, "Carta", "cartas.json")
            exportar_estado_local_json(colecao_atual, fragmentos_atual, creditos_atual,
                                       pontos_ecoa_atual, pontos_resgatados_atual,
                                       historico, "soulup_export_local.json")
        input("ENTER para continuar...")

# Retorno: None. Disponibiliza ao menos um exemplo de exportacao por consulta (30 pts).


def menu_api_externa() -> None:
    while True:
        print("\n=== API EXTERNA PUBLICA ===")
        print("1 - Clima atual + dica sustentavel (Open-Meteo, sem chave)")
        print("2 - Consultar endereco por CEP (ViaCEP, sem chave)")
        print("3 - Salvar ultima consulta de clima em JSON")
        print("4 - Voltar")
        opcao = validar_opcao_numerica("Escolha: ", 1, 4)
        if opcao == 1:
            try:
                lat = input("Latitude (ENTER = Sao Paulo -23.55): ").strip()
                lon = input("Longitude (ENTER = Sao Paulo -46.63): ").strip()
                latitude = float(lat) if lat else -23.55
                longitude = float(lon) if lon else -46.63
            except Exception:
                latitude, longitude = -23.55, -46.63
            consumir_api_clima(latitude, longitude)
            input("ENTER para continuar...")
        elif opcao == 2:
            cep = input("CEP (8 digitos): ")
            consultar_cep_api(cep)
            input("ENTER para continuar...")
        elif opcao == 3:
            dados = consumir_api_clima()
            if "erro" not in dados:
                exportar_para_json(dados, "clima_api.json")
            input("ENTER para continuar...")
        else:
            break

# Retorno: None. Consome APIs publicas sem chave (vale os 20 pts).


def main() -> None:

    pontos_ecoa_atual = pontos_ecoa
    pontos_resgatados_atual = pontos_resgatados
    colecao_atual = colecao
    fragmentos_atual = fragmentos
    creditos_colecao_atual = creditos_colecao
    sets_completos_atual = sets_completos

    print("Conectando ao banco Oracle...")
    conn = conectar_banco()
    if conn is not None:
        print("[BANCO] Conectado ao Oracle com sucesso!")
        garantir_usuario_base(conn)
    else:
        print("[BANCO] Rodando em MODO LOCAL.")

    while True:
        mostrar_menu(pontos_ecoa_atual, pontos_resgatados_atual, colecao_atual, fragmentos_atual, creditos_colecao_atual, conn)
        opcao = input("Escolha: ").strip()

        match opcao:
            case "1":
                antes = pontos_ecoa_atual
                pontos_ecoa_atual, colecao_atual, fragmentos_atual, creditos_colecao_atual, sets_completos_atual = registrar_acao(
                    acoes, pontos_ecoa_atual, historico, colecao_atual, fragmentos_atual, creditos_colecao_atual, sets_completos_atual
                )
                ganho = pontos_ecoa_atual - antes
                if conn is not None and ganho > 0:
                    salvar_acao_no_banco(conn, ganho, USUARIO_ATUAL_ID)

            case "2":
                ver_meu_nivel(pontos_ecoa_atual, pontos_resgatados_atual, historico)

            case "3":
                pontos_ecoa_atual = resgatar_recompensas(pontos_ecoa_atual, pontos_resgatados_atual)

            case "4":
                sugestao_avatar(pontos_ecoa_atual)

            case "5":
                ver_ranking(pontos_ecoa_atual)

            case "6":
                pontos_ecoa_atual = gerenciar_historico(acoes, pontos_ecoa_atual, historico)

            case "7":
                ver_colecao(colecao_atual, fragmentos_atual, creditos_colecao_atual)

            case "8":
                colecao_atual, fragmentos_atual = fabrica_de_cartas(colecao_atual, fragmentos_atual)

            case "9":
                menu_crud_banco(conn)

            case "10":
                menu_exportar_json(conn, colecao_atual, fragmentos_atual, creditos_colecao_atual,
                                   pontos_ecoa_atual, pontos_resgatados_atual, historico)

            case "11":
                menu_api_externa()

            case "12":
                print("Saindo...")
                try:
                    if conn is not None:
                        conn.close()
                except Exception:
                    pass
                break

            case _:
                print("Opcao invalida! Digite de 1 a 12.")

# Retorno: None
# Controla o menu principal. Guarda o estado do usuario em variaveis locais e as atualiza
# a cada opcao escolhida. Integra o jogo local com o Oracle (quando conectado), JSON e API.


main()
