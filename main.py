import dados
import funcoes


def menu_uso_sistema(sistema):
    usuario = funcoes.identificar_usuario(sistema)
    opcao = ""
    while opcao != "0":
        print(
            f"\n[ Pontos: {usuario['pontos']} | Resgatados: {usuario['resgatados']} "
            f"| Nível: {funcoes.calcular_nivel(usuario['pontos'])} ]"
        )
        print(f"\n===== DASHBOARD SOULUP - {usuario['nome']} =====")
        print("1 - Registrar ação sustentável")
        print("2 - Ver meu nível e estatísticas")
        print("3 - Resgatar recompensas (Benefícios reais)")
        print("4 - Sugestão do avatar")
        print("5 - Ver ranking da semana")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            funcoes.registrar_acao(sistema, usuario)
        elif opcao == "2":
            funcoes.ver_nivel_estatisticas(sistema, usuario)
        elif opcao == "3":
            funcoes.resgatar_recompensa(sistema, usuario)
        elif opcao == "4":
            print("\n" + funcoes.sugestao_avatar(usuario))
        elif opcao == "5":
            funcoes.ver_ranking(sistema, usuario)
        elif opcao == "0":
            print("Voltando ao menu principal...")
        else:
            print("Opção inválida!")


def menu_crud_usuarios(sistema):
    opcao = ""
    while opcao != "0":
        print("\n===== GERENCIAR USUÁRIOS =====")
        print("1 - Incluir usuário")
        print("2 - Alterar usuário")
        print("3 - Excluir usuário")
        print("4 - Listar usuários")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            funcoes.cadastrar_usuario(sistema)
        elif opcao == "2":
            funcoes.alterar_usuario(sistema)
        elif opcao == "3":
            funcoes.excluir_usuario(sistema)
        elif opcao == "4":
            funcoes.listar_usuarios(sistema["usuarios"])
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def menu_crud_acoes(sistema):
    opcao = ""
    while opcao != "0":
        print("\n===== GERENCIAR AÇÕES =====")
        print("1 - Incluir ação")
        print("2 - Alterar ação")
        print("3 - Excluir ação")
        print("4 - Listar ações")
        print("5 - Filtrar ações por pontos")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            funcoes.incluir_acao(sistema)
        elif opcao == "2":
            funcoes.alterar_acao(sistema)
        elif opcao == "3":
            funcoes.excluir_acao(sistema)
        elif opcao == "4":
            funcoes.listar_acoes_simples(sistema["acoes"])
            funcoes.pausar()
        elif opcao == "5":
            funcoes.filtrar_acoes(sistema["acoes"])
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def menu_crud_recompensas(sistema):
    opcao = ""
    while opcao != "0":
        print("\n===== GERENCIAR RECOMPENSAS =====")
        print("1 - Incluir recompensa")
        print("2 - Alterar recompensa")
        print("3 - Excluir recompensa")
        print("4 - Listar recompensas")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            funcoes.incluir_recompensa(sistema)
        elif opcao == "2":
            funcoes.alterar_recompensa(sistema)
        elif opcao == "3":
            funcoes.excluir_recompensa(sistema)
        elif opcao == "4":
            funcoes.listar_recompensas(sistema["recompensas"])
            funcoes.pausar()
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def menu_crud(sistema):
    opcao = ""
    while opcao != "0":
        print("\n===== ÁREA DE CADASTRO (CRUD) =====")
        print("1 - Gerenciar usuários")
        print("2 - Gerenciar ações")
        print("3 - Gerenciar recompensas")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            menu_crud_usuarios(sistema)
        elif opcao == "2":
            menu_crud_acoes(sistema)
        elif opcao == "3":
            menu_crud_recompensas(sistema)
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida!")


def main():
    sistema = dados.criar_sistema()
    print("=== SISTEMA DE GAMIFICAÇÃO SUSTENTÁVEL SOULUP ===")
    opcao = ""
    while opcao != "0":
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Uso do sistema")
        print("2 - Área de cadastro (CRUD)")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            menu_uso_sistema(sistema)
        elif opcao == "2":
            menu_crud(sistema)
        elif opcao == "0":
            print("Até logo! Continue salvando o planeta!")
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
