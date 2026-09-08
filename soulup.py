
acoes = ("Reciclagem", "Transporte Público", "Economia de Energia", "Economia de Água", "Bicicleta", "Plantio de Árvore", "Banho Rápido")

pontos_ecoa = 0
pontos_resgatados = 0
historico = []


def identificar_nivel(pontos_ecoa: int) -> str:
    if pontos_ecoa < 100:
        return "Semente"
    elif pontos_ecoa < 300:
        return "Broto"
    elif pontos_ecoa < 600:
        return "Árvore"
    else:
        return "Expert"

# Recebe os pontos e retorna o nível atual do usuário.


def validar_opcao_numerica(mensagem: str, minimo: int, maximo: int) -> int:
    try:
        valor = int(input(mensagem))

        if not (minimo <= valor <= maximo):
            raise Exception(f"Opção fora do intervalo permitido ({minimo} a {maximo})!")

    except Exception as erro:
        print(f"Entrada inválida! {erro}")
        return 0

    else:
        return valor

    finally:
        pass

# Recebe uma mensagem, um valor mínimo e máximo e valida a opção digitada.


def calcular_pontos(acao: str) -> int:
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

# Recebe uma ação e retorna a quantidade de pontos que ela vale.


def registrar_acao(acoes: list, pontos_ecoa: int, historico: list) -> int:
    print("\nAções Sustentáveis disponíveis:")

    for i, acao in enumerate(acoes):
        print(f"{i + 1} - {acao}")

    escolha = validar_opcao_numerica("\nQual ação sustentável você realizou hoje? ", 1, len(acoes))

    if escolha == 0:
        print("Não foi possível registrar a ação. Tente novamente.")
        return pontos_ecoa

    try:
        acao_escolhida = acoes[escolha - 1]
        pontos = calcular_pontos(acao_escolhida)

    except Exception as erro:
        print(f"Ocorreu um erro ao registrar a ação: {erro}")
        return pontos_ecoa

    else:
        pontos_ecoa += pontos
        historico.append((acao_escolhida, pontos))

        print(f"Boa! Você ganhou +{pontos} Pontos ECOA com: {acao_escolhida}!")
        print("Transação validada e registrada com sucesso via Blockchain.")

        return pontos_ecoa

    finally:
        print("Operação de registro finalizada.")

# Recebe as ações, o saldo e o histórico, registra uma ação e retorna o novo saldo.


def ver_meu_nivel(pontos_ecoa: int, pontos_resgatados: int, historico: list) -> str:
    nivel = identificar_nivel(pontos_ecoa)

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

    return nivel

# Recebe os dados do usuário, mostra suas informações e retorna o nível atual.


def resgatar_recompensas(pontos_ecoa: int, pontos_resgatados: int) -> int:
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

    if opcao_troca == 0 or opcao_troca == 9:
        return pontos_ecoa

    recompensas = {
        1: (200, "Plantar 1 Árvore"),
        2: (250, "Kit Reciclagem"),
        3: (300, "Crédito Transporte (R$ 20)"),
        4: (350, "Cupom Mercado Orgânico (R$ 30)"),
        5: (400, "Aluguel de Bicicleta (1 semana grátis)"),
        6: (500, "Desconto na Energia (10% na fatura)"),
        7: (1500, "Adotar uma Área Verde (Parque por 1 mês)"),
        8: (2000, "Mês de Energia Grátis")
    }

    try:
        custo, recompensa = recompensas[opcao_troca]

        if pontos_ecoa < custo:
            raise Exception(f"Pontos insuficientes! Você precisa de {custo} pontos, mas tem apenas {pontos_ecoa}.")

    except Exception as erro:
        print(f"\n{erro}")
        return pontos_ecoa

    else:
        pontos_ecoa -= custo
        pontos_resgatados += custo

        print(f"\nSucesso! Você resgatou: {recompensa}!")
        print(f"Foram utilizados {custo} Pontos ECOA.")

        return pontos_ecoa

    finally:
        print("Operação de resgate finalizada.")

# Recebe o saldo e os pontos resgatados, realiza o resgate e retorna o novo saldo.


def sugestao_avatar(pontos_ecoa: int) -> str:
    nivel = identificar_nivel(pontos_ecoa)

    print("\n--- MENSAGEM DO AVATAR ---")

    if nivel == "Semente":
        mensagem = "Avatar: Que ótimo ver você por aqui! Registre missões diárias para fazermos nossa semente brotar."
    elif nivel == "Broto":
        mensagem = "Avatar: Crescendo firme! Junte 200 pontos para resgatar 'Plantar 1 Árvore' na aba de Recompensas!"
    else:
        mensagem = f"Avatar: Parabéns pelo nível {nivel}! Continue acumulando pontos para desbloquear recompensas avançadas."

    print(mensagem)

    return mensagem

# Recebe os pontos, identifica o nível e retorna uma mensagem do avatar.


def ver_ranking(pontos_ecoa: int) -> list:
    competidores = [
        {"nome": "Ana", "pontos": 350},
        {"nome": "Carlos", "pontos": 280},
        {"nome": "Você", "pontos": pontos_ecoa},
        {"nome": "Marina", "pontos": 150},
        {"nome": "Pedro", "pontos": 120}
    ]

    competidores_ordenados = sorted(competidores, key=lambda x: x["pontos"], reverse=True)

    print("\n==============================")
    print("      RANKING DA SEMANA")
    print("==============================")

    for indice, usuario in enumerate(competidores_ordenados):
        posicao = indice + 1
        nome = usuario["nome"]
        pontos = usuario["pontos"]

        if nome == "Você":
            print(f"-> {posicao}º {nome:<10} | {pontos} pts * (Sua posição)")
        else:
            print(f"   {posicao}º {nome:<10} | {pontos} pts")

    print("==============================")

    return competidores_ordenados

# Recebe os pontos do usuário, monta o ranking, exibe e retorna a lista ordenada.


def listar_historico(historico: list) -> bool:
    print("\n--- HISTÓRICO DE AÇÕES ---")

    if not historico:
        print("Nenhuma ação registrada ainda.")
        return False

    for indice, (acao, pontos) in enumerate(historico):
        print(f"{indice + 1} - {acao} (+{pontos} pts)")

    return True

# Recebe o histórico, mostra as ações e retorna True se houver registros.


def editar_acao_historico(acoes: list, pontos_ecoa: int, historico: list) -> int:
    if not listar_historico(historico):
        return pontos_ecoa

    indice = validar_opcao_numerica("\nQual registro deseja editar? (número) ", 1, len(historico))

    if indice == 0:
        print("Edição cancelada: registro inválido.")
        return pontos_ecoa

    print("\nAções Sustentáveis disponíveis:")

    for i, acao in enumerate(acoes):
        print(f"{i + 1} - {acao}")

    nova_escolha = validar_opcao_numerica("Digite a nova ação para substituir o registro: ", 1, len(acoes))

    if nova_escolha == 0:
        print("Edição cancelada: nova ação inválida.")
        return pontos_ecoa

    try:
        acao_antiga, pontos_antigos = historico[indice - 1]
        nova_acao = acoes[nova_escolha - 1]
        novos_pontos = calcular_pontos(nova_acao)

    except Exception as erro:
        print(f"Não foi possível editar o registro: {erro}")
        return pontos_ecoa

    else:
        pontos_ecoa = pontos_ecoa - pontos_antigos + novos_pontos
        historico[indice - 1] = (nova_acao, novos_pontos)

        print(f"Registro atualizado: '{acao_antiga}' -> '{nova_acao}' ({novos_pontos} pts).")

        return pontos_ecoa

    finally:
        print("Operação de edição finalizada.")

# Recebe as ações, o saldo e o histórico, altera uma ação e retorna o novo saldo.


def excluir_acao_historico(pontos_ecoa: int, historico: list) -> int:
    if not listar_historico(historico):
        return pontos_ecoa

    indice = validar_opcao_numerica("\nQual registro deseja excluir? (número) ", 1, len(historico))

    if indice == 0:
        print("Exclusão cancelada: registro inválido.")
        return pontos_ecoa

    try:
        acao_removida, pontos_removidos = historico[indice - 1]

    except Exception as erro:
        print(f"Não foi possível excluir o registro: {erro}")
        return pontos_ecoa

    else:
        del historico[indice - 1]
        pontos_ecoa = max(0, pontos_ecoa - pontos_removidos)

        print(f"Registro '{acao_removida}' removido. {pontos_removidos} pontos estornados do saldo.")

        return pontos_ecoa

    finally:
        print("Operação de exclusão finalizada.")

# Recebe o saldo e o histórico, remove uma ação e retorna o novo saldo.

