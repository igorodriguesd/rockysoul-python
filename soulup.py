# Sistema de Gamificação Sustentável SoulUp com Avatar - Lógica / Regras de Negócio

acoes = ("Reciclagem", "Transporte Público", "Economia de Energia", "Economia de Água", "Bicicleta",
        "Plantio de Árvore", "Banho Rápido")

pontos_ecoa = 0
pontos_resgatados = 0
historico = []


def identificar_nivel():

    if pontos_ecoa < 100:
        return "Semente"
    elif pontos_ecoa < 300:
        return "Broto"
    elif pontos_ecoa < 600:
        return "Árvore"
    else:
        return "Expert"


def validar_opcao_numerica(mensagem, minimo, maximo):

    try:
        valor = int(input(mensagem))
        if not (minimo <= valor <= maximo):
            raise Exception(f"Opção fora do intervalo permitido ({minimo} a {maximo})!")
    except Exception as erro:
        print(f"Entrada inválida! {erro}")
        return None
    else:
        return valor
    finally:
        pass


def calcular_pontos(acao):

    if acao == "Reciclagem":
        return 30
    elif acao == "Transporte Público":
        return 50
    elif acao == "Economia de Energia":
        return 20
    elif acao == "Economia de Água":
        return 15
    elif acao == "Bicicleta":
        return 25
    elif acao == "Plantio de Árvore":
        return 100
    elif acao == "Banho Rápido":
        return 20
    else:
        return 10


def registrar_acao():

    global pontos_ecoa
    print("\nAções Sustentáveis disponíveis:")
    for i, acao in enumerate(acoes):
        print(f"{i + 1} - {acao}")

    escolha = validar_opcao_numerica("\nQual ação sustentável você realizou hoje? ", 1, len(acoes))

    if escolha is None:
        print("Não foi possível registrar a ação. Tente novamente.")
        return

    try:
        acao_escolhida = acoes[escolha - 1]
        pontos = calcular_pontos(acao_escolhida)
    except Exception as erro:
        print(f"Ocorreu um erro ao registrar a ação: {erro}")
    else:
        pontos_ecoa += pontos
        historico.append((acao_escolhida, pontos))
        print(f"Boa! Você ganhou +{pontos} Pontos ECOA com: {acao_escolhida}!")
        print("Transação validada e registrada com sucesso via Blockchain.")
    finally:
        print("Operação de registro finalizada.")


def ver_meu_nivel():

    nivel = identificar_nivel()
    print(f"\n--- SEU NÍVEL ATUAL: {nivel} ---")
    print(f"Saldo Disponível: {pontos_ecoa} Pontos ECOA")
    print(f"Total já Resgatado: {pontos_resgatados} Pontos ECOA")
    print(f"Histórico de Missões: {historico}")

    if nivel == "Semente":
        print(f"Progresso: Faltam {100 - pontos_ecoa} pontos para evoluir para Broto!")
    elif nivel == "Broto":
        print(f"Progresso: Faltam {300 - pontos_ecoa} pontos para evoluir para Árvore!")
    elif nivel == "Árvore":
        print(f"Progresso: Faltam {600 - pontos_ecoa} pontos para evoluir para Expert!")


def resgatar_recompensas():

    global pontos_ecoa, pontos_resgatados
    print("\n=== VITRINE DE RECOMPENSAS SOULUP ===")
    print("1 - Plantar 1 Árvore ------------ 200 pontos")
    print("2 - Kit Reciclagem -------------- 250 pontos")
    print("3 - Crédito Transporte ---------- 300 pontos")
    print("4 - Cupom Mercado Orgânico ------ 350 pontos")
    print("5 - Aluguel de Bicicleta -------- 400 pontos")
    print("6 - Desconto na Energia --------- 500 pontos")
    print("7 - Adotar uma Área Verde ------- 1500 pontos")
    print("8 - Mês de Energia Grátis ------- 2000 pontos")
    print("9 - Voltar")

    opcao_troca = validar_opcao_numerica(f"\nSeu Saldo: {pontos_ecoa} pts. Escolha um benefício: ", 1, 9)

    if opcao_troca is None:
        print("Não foi possível concluir o resgate. Tente novamente.")
        return

    if opcao_troca == 9:
        return

    recompensas = {
        1: (200, "Plantar 1 Árvore"),
        2: (250, "Kit Reciclagem"),
        3: (300, "Crédito Transporte (R$ 20)"),
        4: (350, "Cupom Mercado Orgânico (R$ 30)"),
        5: (400, "Aluguel de Bicicleta (1 semana grátis)"),
        6: (500, "Desconto na Energia (10% na fatura)"),
        7: (1500, "Adotar uma Área Verde (Parque por 1 mês)"),
        8: (2000, "Mês de Energia Grátis"),
    }

    try:
        custo, recompensa = recompensas[opcao_troca]
        if pontos_ecoa < custo:
            raise Exception(f"Pontos insuficientes! Você precisa de {custo} pontos, mas tem apenas {pontos_ecoa}.")
    except Exception as erro:
        print(f"\n{erro}")
    else:
        pontos_ecoa -= custo
        pontos_resgatados += custo
        print(f"\nSucesso! Você resgatou: {recompensa}!")
        print(f"Foram utilizados {custo} Pontos ECOA.")
    finally:
        print("Operação de resgate finalizada.")


def sugestao_avatar():

    nivel = identificar_nivel()
    print(f"\n--- MENSAGEM DO AVATAR ---")
    if nivel == "Semente":
        print("Avatar: Que ótimo ver você por aqui! Registre missões diárias para fazermos nossa semente brotar.")
    elif nivel == "Broto":
        print("Avatar: Crescendo firme! Junte 200 pontos para resgatar 'Plantar 1 Árvore' na aba de Recompensas!")
    else:
        print(f"Avatar: Parabéns pelo nível {nivel}! Continue acumulando pontos para desbloquear recompensas avançadas.")


def ver_ranking():

    competidores = [
        {"nome": "Ana", "pontos": 350},
        {"nome": "Carlos", "pontos": 280},
        {"nome": "Você", "pontos": pontos_ecoa},
        {"nome": "Marina", "pontos": 150},
        {"nome": "Pedro", "pontos": 120}
    ]

    competidores_ordenados = sorted(competidores, key=lambda x: x['pontos'], reverse=True)

    print("\n==============================")
    print("      RANKING DA SEMANA       ")
    print("==============================")

    for indice, usuario in enumerate(competidores_ordenados):
        posicao = indice + 1
        nome = usuario['nome']
        pontos = usuario['pontos']

        if nome == "Você":
            print(f"-> {posicao}º {nome:<10} | {pontos} pts * (Sua posição)")
        else:
            print(f"   {posicao}º {nome:<10} | {pontos} pts")
    print("==============================")


def listar_historico():

    print("\n--- HISTÓRICO DE AÇÕES ---")
    if not historico:
        print("Nenhuma ação registrada ainda.")
        return False

    for indice, (acao, pontos) in enumerate(historico):
        print(f"{indice + 1} - {acao} (+{pontos} pts)")
    return True


def editar_acao_historico():

    global pontos_ecoa

    if not listar_historico():
        return

    indice = validar_opcao_numerica("\nQual registro deseja editar? (número) ", 1, len(historico))
    if indice is None:
        print("Edição cancelada: registro inválido.")
        return

    print("\nAções Sustentáveis disponíveis:")
    for i, acao in enumerate(acoes):
        print(f"{i + 1} - {acao}")
    nova_escolha = validar_opcao_numerica("Digite a nova ação para substituir o registro: ", 1, len(acoes))
    if nova_escolha is None:
        print("Edição cancelada: nova ação inválida.")
        return

    try:
        acao_antiga, pontos_antigos = historico[indice - 1]
        nova_acao = acoes[nova_escolha - 1]
        novos_pontos = calcular_pontos(nova_acao)
    except Exception as erro:
        print(f"Não foi possível editar o registro: {erro}")
    else:
        pontos_ecoa = pontos_ecoa - pontos_antigos + novos_pontos
        historico[indice - 1] = (nova_acao, novos_pontos)
        print(f"Registro atualizado: '{acao_antiga}' -> '{nova_acao}' ({novos_pontos} pts).")
    finally:
        print("Operação de edição finalizada.")


def excluir_acao_historico():

    global pontos_ecoa

    if not listar_historico():
        return

    indice = validar_opcao_numerica("\nQual registro deseja excluir? (número) ", 1, len(historico))
    if indice is None:
        print("Exclusão cancelada: registro inválido.")
        return

    try:
        acao_removida, pontos_removidos = historico[indice - 1]
    except Exception as erro:
        print(f"Não foi possível excluir o registro: {erro}")
    else:
        del historico[indice - 1]
        pontos_ecoa = max(0, pontos_ecoa - pontos_removidos)
        print(f"Registro '{acao_removida}' removido. {pontos_removidos} pontos estornados do saldo.")
    finally:
        print("Operação de exclusão finalizada.")