ACOES_PADRAO = [
    ("Reciclagem", 30),
    ("Transporte Público", 50),
    ("Economia de Energia", 20),
    ("Economia de Água", 15),
    ("Bicicleta", 25),
    ("Plantio de Árvore", 100),
    ("Banho Rápido", 20),
]

RECOMPENSAS_PADRAO = [
    {"titulo": "Plantar 1 Árvore", "descricao": "Muda nativa", "custo": 200, "estoque": 50},
    {"titulo": "Kit Reciclagem", "descricao": "Kit doméstico", "custo": 250, "estoque": 20},
    {"titulo": "Crédito Transporte", "descricao": "R$ 20 de transporte público", "custo": 300, "estoque": 15},
    {"titulo": "Cupom Mercado Orgânico", "descricao": "R$ 30 em orgânicos", "custo": 350, "estoque": 10},
    {"titulo": "Aluguel de Bicicleta", "descricao": "1 semana grátis", "custo": 400, "estoque": 10},
    {"titulo": "Desconto na Energia", "descricao": "10% na fatura", "custo": 500, "estoque": 5},
    {"titulo": "Adotar uma Área Verde", "descricao": "Parque por 1 mês", "custo": 1500, "estoque": 2},
    {"titulo": "Mês de Energia Grátis", "descricao": "Conta zerada por 1 mês", "custo": 2000, "estoque": 1},
]

NIVEIS = (("Semente", 0), ("Broto", 100), ("Árvore", 300), ("Expert", 600))


def criar_sistema():
    acoes = []
    for acao in ACOES_PADRAO:
        acoes.append([acao[0], acao[1]])
    recompensas = []
    for r in RECOMPENSAS_PADRAO:
        nova = {"titulo": r["titulo"], "descricao": r["descricao"], "custo": r["custo"], "estoque": r["estoque"]}
        recompensas.append(nova)
    sistema = {"usuarios": [], "acoes": acoes, "recompensas": recompensas, "historico": []}
    return sistema
