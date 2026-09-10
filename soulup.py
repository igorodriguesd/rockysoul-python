import random

acoes = ("Reciclagem", "Transporte Público", "Economia de Energia", "Economia de Água", "Bicicleta", "Plantio de Árvore", "Banho Rápido")

pontos_ecoa = 0
pontos_resgatados = 0
historico = []

# --- Estado da Coleção de Cartas (novo) ---
colecao = {}          # nome_carta -> {"set": str, "raridade": str, "brilhante": bool}
fragmentos = 0
creditos_colecao = 0
sets_completos = set()  # nomes dos sets que já ativaram a Química de Set

# 5 sets temáticos com 4 cartas cada (20 cartas no total), conforme a documentação da Sprint 3
SETS = {
    "Recursos": [
        ("Reciclagem", "Comum"),
        ("Reutilização", "Incomum"),
        ("Sacola Reutilizável", "Rara"),
        ("Redução de Desperdício", "Épica"),
    ],
    "Guardiões da Água": [
        ("Economia de Água", "Comum"),
        ("Banho Rápido", "Incomum"),
        ("Garrafa Reutilizável", "Rara"),
        ("Captação de Chuva", "Épica"),
    ],
    "Cidade Verde": [
        ("Bicicleta", "Comum"),
        ("Transporte Público", "Incomum"),
        ("Mobilidade Elétrica", "Rara"),
        ("Ciclovia", "Épica"),
    ],
    "Energia Limpa": [
        ("Economia de Energia", "Comum"),
        ("Iluminação Eficiente", "Incomum"),
        ("Energia Solar", "Rara"),
        ("Energia Eólica", "Épica"),
    ],
    "Cultivo": [
        ("Plantio", "Comum"),
        ("Compostagem", "Incomum"),
        ("Horta Doméstica", "Rara"),
        ("Agrofloresta", "Lendária"),
    ],
}

CHANCE_POR_RARIDADE = {"Lendária": 10, "Épica": 20, "Rara": 35, "Incomum": 55, "Comum": 75}
FRAGMENTOS_POR_RARIDADE = {"Comum": 3, "Incomum": 5, "Rara": 10, "Épica": 20, "Lendária": 40}
CUSTO_FABRICA_POR_RARIDADE = {"Comum": 10, "Incomum": 16, "Rara": 32, "Épica": 70, "Lendária": 140}
CHANCE_BRILHANTE = 8


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


def sortear_raridade() -> str:
    for raridade, chance in CHANCE_POR_RARIDADE.items():
        if random.random() * 100 < chance:
            return raridade

    return "Comum"

# Sorteia e retorna a raridade da cartinha, testando da mais rara para a mais comum
# conforme as chances da tabela (Lendária 10%, Épica 20%, Rara 35%, Incomum 55%, Comum 75%),
# com fallback garantido em "Comum".


def sortear_carta(raridade: str) -> tuple:
    cartas_da_raridade = []

    for set_nome, cartas in SETS.items():
        for nome_carta, raridade_carta in cartas:
            if raridade_carta == raridade:
                cartas_da_raridade.append((set_nome, nome_carta))

    return random.choice(cartas_da_raridade)

# Recebe uma raridade e retorna (nome do set, nome da carta) sorteados entre as cartas daquela raridade.


def sortear_brilhante() -> bool:
    return random.random() * 100 < CHANCE_BRILHANTE

# Sorteia, de forma independente da raridade, se a carta vem na versão brilhante (8% de chance).


def set_completo(set_nome: str, colecao: dict) -> bool:
    cartas_do_set = SETS[set_nome]
    return all(nome_carta in colecao for nome_carta, _ in cartas_do_set)

# Recebe o nome de um set e a coleção, e retorna True se as 4 cartas do set já foram obtidas.


def girar_roleta(colecao: dict, fragmentos: int, creditos_colecao: int, sets_completos: set) -> tuple:
    try:
        raridade = sortear_raridade()
        set_nome, nome_carta = sortear_carta(raridade)
        brilhante = sortear_brilhante()

    except Exception as erro:
        print(f"Ocorreu um erro ao girar a roleta: {erro}")
        return colecao, fragmentos, creditos_colecao, sets_completos

    else:
        print("\n*** GIRANDO A ROLETA DE CARTAS... ***")
        print(f"Raridade sorteada: {raridade}" + (" ✦ Versão Brilhante!" if brilhante else ""))

        if nome_carta in colecao:
            ganho = FRAGMENTOS_POR_RARIDADE[raridade]
            fragmentos += ganho
            print(f"Você já possui '{nome_carta}'. Convertido em +{ganho} fragmentos!")
        else:
            colecao[nome_carta] = {"set": set_nome, "raridade": raridade, "brilhante": brilhante}
            print(f"Nova carta! Você ganhou '{nome_carta}' ({raridade}) do set {set_nome}.")

            if set_completo(set_nome, colecao) and set_nome not in sets_completos:
                sets_completos.add(set_nome)
                creditos_colecao += 150
                print(f"Química de Set ativada para '{set_nome}'! +150 créditos de coleção!")

        return colecao, fragmentos, creditos_colecao, sets_completos

    finally:
        print("Giro de roleta finalizado.")

# Recebe a coleção, os fragmentos, os créditos de coleção e os sets já completados; sorteia uma
# cartinha (raridade + carta + versão brilhante), credita fragmentos em caso de repetida, ativa a
# Química de Set quando aplicável, e retorna os quatro valores atualizados.


def registrar_acao(acoes: list, pontos_ecoa: int, historico: list, colecao: dict, fragmentos: int, creditos_colecao: int, sets_completos: set) -> tuple:
    print("\nAções Sustentáveis disponíveis:")

    for i, acao in enumerate(acoes):
        print(f"{i + 1} - {acao}")

    escolha = validar_opcao_numerica("\nQual ação sustentável você realizou hoje? ", 1, len(acoes))

    if escolha == 0:
        print("Não foi possível registrar a ação. Tente novamente.")
        return pontos_ecoa, colecao, fragmentos, creditos_colecao, sets_completos

    try:
        acao_escolhida = acoes[escolha - 1]
        pontos = calcular_pontos(acao_escolhida)

    except Exception as erro:
        print(f"Ocorreu um erro ao registrar a ação: {erro}")
        return pontos_ecoa, colecao, fragmentos, creditos_colecao, sets_completos

    else:
        pontos_ecoa += pontos
        historico.append((acao_escolhida, pontos))

        print(f"Boa! Você ganhou +{pontos} Pontos ECOA com: {acao_escolhida}!")
        print("Transação validada e registrada com sucesso via Blockchain.")

        # Toda ação verificada com sucesso concede uma tentativa na roleta de cartas.
        colecao, fragmentos, creditos_colecao, sets_completos = girar_roleta(colecao, fragmentos, creditos_colecao, sets_completos)

        return pontos_ecoa, colecao, fragmentos, creditos_colecao, sets_completos

    finally:
        print("Operação de registro finalizada.")

# Recebe as ações, o saldo, o histórico e o estado da coleção; registra uma ação, aciona a roleta
# de cartas e retorna o novo saldo junto com o estado atualizado da coleção.


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


def ver_colecao(colecao: dict, fragmentos: int, creditos_colecao: int) -> None:
    print("\n=== MINHA COLEÇÃO ===")
    print(f"Progresso: {len(colecao)}/20 cartas | Fragmentos: {fragmentos} | Créditos de Coleção: {creditos_colecao}")

    for set_nome, cartas in SETS.items():
        obtidas = sum(1 for nome_carta, _ in cartas if nome_carta in colecao)
        print(f"\n-- {set_nome} ({obtidas}/4) --")

        for nome_carta, raridade in cartas:
            if nome_carta in colecao:
                brilho = " ✦ Brilhante" if colecao[nome_carta]["brilhante"] else ""
                print(f"  [OK] {nome_carta} ({raridade}){brilho}")
            else:
                print(f"  [ ? ] ??? ({raridade}) - ainda não obtida")

# Recebe a coleção, os fragmentos e os créditos, e exibe o progresso da coleção organizado por set.


def fabrica_de_cartas(colecao: dict, fragmentos: int) -> tuple:
    faltantes = []

    for set_nome, cartas in SETS.items():
        for nome_carta, raridade in cartas:
            if nome_carta not in colecao:
                faltantes.append((set_nome, nome_carta, raridade))

    if not faltantes:
        print("\nParabéns! Você já possui todas as cartas da coleção.")
        return colecao, fragmentos

    print(f"\n=== FÁBRICA DE CARTAS (Saldo de Fragmentos: {fragmentos}) ===")

    for i, (set_nome, nome_carta, raridade) in enumerate(faltantes):
        custo = CUSTO_FABRICA_POR_RARIDADE[raridade]
        print(f"{i + 1} - {nome_carta} ({raridade}, {set_nome}) - {custo} fragmentos")

    print(f"{len(faltantes) + 1} - Voltar")

    escolha = validar_opcao_numerica("\nQual carta deseja montar? ", 1, len(faltantes) + 1)

    if escolha == 0 or escolha == len(faltantes) + 1:
        return colecao, fragmentos

    try:
        set_nome, nome_carta, raridade = faltantes[escolha - 1]
        custo = CUSTO_FABRICA_POR_RARIDADE[raridade]

        if fragmentos < custo:
            raise Exception(f"Fragmentos insuficientes! Você precisa de {custo}, mas tem apenas {fragmentos}.")

    except Exception as erro:
        print(f"\n{erro}")
        return colecao, fragmentos

    else:
        fragmentos -= custo
        colecao[nome_carta] = {"set": set_nome, "raridade": raridade, "brilhante": False}

        print(f"\nSucesso! Você montou a carta '{nome_carta}' ({raridade}) do set {set_nome}!")

        return colecao, fragmentos

    finally:
        print("Operação da Fábrica de Cartas finalizada.")

# Recebe a coleção e os fragmentos, permite montar (craftar) uma carta faltante e retorna os
# valores atualizados. Não é possível montar uma carta já possuída (lista só mostra faltantes).