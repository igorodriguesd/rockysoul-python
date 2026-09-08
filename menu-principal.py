from soulup import *

def mostrar_menu() -> None:
    nivel = identificar_nivel(pontos_ecoa)

    print("\n=== DASHBOARD SOULUP ===")
    print(f"[ Pontos Disponíveis: {pontos_ecoa} | Já Resgatados: {pontos_resgatados} | Nível: {nivel} ]")
    print("---------------------------------------------------------------------------")
    print("1 - Registrar ação sustentável (Criar)")
    print("2 - Ver Meu Nível e Estatísticas")
    print("3 - Resgatar Recompensas (Benefícios Reais)")
    print("4 - Sugestão do Avatar")
    print("5 - Ver Ranking da Semana")
    print("6 - Gerenciar Histórico de Ações (CRUD)")
    print("7 - Sair")

# Retorno: None
# Mostra o menu principal e as informações do usuário.

def main() -> None:
    while True:
        mostrar_menu()
        opcao = input("Escolha: ")

        match opcao:
            case "1":
                registrar_acao(acoes, pontos_ecoa, historico)

            case "2":
                ver_meu_nivel(pontos_ecoa, pontos_resgatados, historico)

            case "3":
                resgatar_recompensas(pontos_ecoa, pontos_resgatados)

            case "4":
                sugestao_avatar(pontos_ecoa)

            case "5":
                ver_ranking(pontos_ecoa)

            case "6":
                gerenciar_historico()

            case "7":
                print("Saindo...")
                break

            case _:
                print("Opção inválida! Digite de 1 a 7.")

# Retorno: None
# Controla o menu principal.
    
main()