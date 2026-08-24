# Sistema de Gamificação Sustentável SoulUp com Avatar - Menu / Interface

import soulup as core


def mostrar_menu():

    nivel = core.identificar_nivel()
    print("\n=== DASHBOARD SOULUP ===")
    print(f"[ Pontos Disponíveis: {core.pontos_ecoa} | Já Resgatados: {core.pontos_resgatados} | Nível: {nivel} ]")
    print("---------------------------------------------------------------------------")
    print("1 - Registrar ação sustentável (Criar)")
    print("2 - Ver Meu Nível e Estatísticas")
    print("3 - Resgatar Recompensas (Benefícios Reais)")
    print("4 - Sugestão do Avatar")
    print("5 - Ver Ranking da Semana")
    print("6 - Gerenciar Histórico de Ações (CRUD)")
    print("7 - Sair")


def gerenciar_historico():

    while True:
        print("\n=== GERENCIAR HISTÓRICO (CRUD) ===")
        print("1 - Listar histórico completo (Read)")
        print("2 - Registrar nova ação (Create)")
        print("3 - Editar uma ação registrada (Update)")
        print("4 - Excluir uma ação registrada (Delete)")
        print("5 - Voltar ao menu principal")

        opcao = core.validar_opcao_numerica("Escolha uma opção do submenu: ", 1, 5)

        if opcao is None:
            continue
        elif opcao == 1:
            core.listar_historico()
        elif opcao == 2:
            core.registrar_acao()
        elif opcao == 3:
            core.editar_acao_historico()
        elif opcao == 4:
            core.excluir_acao_historico()
        elif opcao == 5:
            break


def main():

    while True:
        mostrar_menu()
        opcao = input("Escolha: ")

        match opcao:
            case "1":
                core.registrar_acao()
            case "2":
                core.ver_meu_nivel()
            case "3":
                core.resgatar_recompensas()
            case "4":
                core.sugestao_avatar()
            case "5":
                core.ver_ranking()
            case "6":
                gerenciar_historico()
            case "7":
                print("Saindo... Seus dados de impacto social foram salvos com segurança na Web 3.0.")
                break
            case _:
                print("Opção inválida! Digite de 1 a 7.")


if __name__ == "__main__":
    main()