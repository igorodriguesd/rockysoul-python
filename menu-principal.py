from soulup import *


def mostrar_menu(pontos_ecoa: int, pontos_resgatados: int, colecao: dict, fragmentos: int, creditos_colecao: int) -> None:
    nivel = identificar_nivel(pontos_ecoa)

    print("\n=== DASHBOARD SOULUP ===")
    print(f"[ Pontos Disponíveis: {pontos_ecoa} | Já Resgatados: {pontos_resgatados} | Nível: {nivel} ]")
    print(f"[ Cartas: {len(colecao)}/20 | Fragmentos: {fragmentos} | Créditos de Coleção: {creditos_colecao} ]")
    print("---------------------------------------------------------------------------")
    print("1 - Registrar ação sustentável (Criar)")
    print("2 - Ver Meu Nível e Estatísticas")
    print("3 - Resgatar Recompensas (Benefícios Reais)")
    print("4 - Sugestão do Avatar")
    print("5 - Ver Ranking da Semana")
    print("6 - Gerenciar Histórico de Ações (CRUD)")
    print("7 - Ver Minha Coleção de Cartas")
    print("8 - Fábrica de Cartas (Trocar Fragmentos)")
    print("9 - Sair")

# Retorno: None
# Mostra o menu principal e as informações do usuário, incluindo o progresso da coleção.


def gerenciar_historico(acoes: list, pontos_ecoa: int, historico: list) -> int:
    print("\n--- GERENCIAR HISTÓRICO ---")
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
# Submenu de CRUD do histórico de ações (listar, editar, excluir).


def main() -> None:

    pontos_ecoa_atual = pontos_ecoa
    pontos_resgatados_atual = pontos_resgatados
    colecao_atual = colecao
    fragmentos_atual = fragmentos
    creditos_colecao_atual = creditos_colecao
    sets_completos_atual = sets_completos

    while True:
        mostrar_menu(pontos_ecoa_atual, pontos_resgatados_atual, colecao_atual, fragmentos_atual, creditos_colecao_atual)
        opcao = input("Escolha: ")

        match opcao:
            case "1":
                pontos_ecoa_atual, colecao_atual, fragmentos_atual, creditos_colecao_atual, sets_completos_atual = registrar_acao(
                    acoes, pontos_ecoa_atual, historico, colecao_atual, fragmentos_atual, creditos_colecao_atual, sets_completos_atual
                )

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
                print("Saindo...")
                break

            case _:
                print("Opção inválida! Digite de 1 a 9.")

# Retorno: None
# Controla o menu principal. Guarda o estado do usuário em variáveis locais e as atualiza
# a cada opção escolhida, recebendo de volta os valores retornados pelas funções chamadas.


main()