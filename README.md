# 🌱 SOULUP — Sistema de Gamificação Sustentável

Sistema de console desenvolvido em **Python** que gamifica ações sustentáveis do dia a dia.
O usuário registra missões ecológicas, acumula **Pontos ECOA**, evolui de nível, compete no
ranking semanal e troca pontos por **benefícios reais** na vitrine de recompensas.

## 🚀 Como executar

```bash
py main.py
```

> Não há dependências externas — apenas Python 3 padrão.

## 🧭 Estrutura de menus

```
MENU PRINCIPAL
├── 1 - Uso do sistema
│     ├── 1 - Registrar ação sustentável
│     ├── 2 - Ver meu nível e estatísticas
│     ├── 3 - Resgatar recompensas (benefícios reais)
│     ├── 4 - Sugestão do avatar
│     ├── 5 - Ver ranking da semana
│     └── 0 - Voltar
├── 2 - Área de cadastro (CRUD)
│     ├── 1 - Gerenciar usuários      (incluir / alterar / excluir / listar)
│     ├── 2 - Gerenciar ações         (incluir / alterar / excluir / listar / filtrar)
│     ├── 3 - Gerenciar recompensas   (incluir / alterar / excluir / listar)
│     └── 0 - Voltar
└── 0 - Sair
```

## 📁 Organização do projeto

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Interface: menus, submenus e navegação |
| `funcoes.py` | Regras de negócio: níveis, ranking, filtros e CRUDs |
| `dados.py` | Dados iniciais (ações, recompensas, níveis) e criação da estrutura |

A modularização mantém cada arquivo com uma única responsabilidade,
facilitando manutenção, reuso e trabalho em equipe.

## 🗃️ Armazenamento em sequências

Os dados ficam guardados **em memória**, usando estruturas vistas em sala:

| Dado | Estrutura | Exemplo |
|---|---|---|
| Ações sustentáveis | lista de listas | `[["Reciclagem", 30], ...]` |
| Usuários | lista de dicionários | `[{"nome": "Ana", "pontos": 100, "resgatados": 0}]` |
| Recompensas | lista de dicionários | `[{"titulo": "Kit Reciclagem", "custo": 250, "estoque": 20}]` |
| Histórico de missões | lista de listas | `[["Ana", "Reciclagem", 30]]` |
| Níveis | tupla de tuplas | `(("Semente", 0), ("Broto", 100), ...)` |
| Menu de opções | if/elif encadeados com `while` | laço até o usuário escolher voltar/sair |

## 🛡️ Tratamento de erros

Todas as operações de inserção, alteração e exclusão usam o padrão
`try / except / else / finally`:

- **try** → leitura e conversão dos dados (`int(input(...))`)
- **except ValueError** → mensagem amigável quando o valor é inválido
- **else** → validações de negócio e gravação do dado (só executa se não houve erro)
- **finally** → pausa a tela (`pausar()`), executando sempre

Exemplos de erros tratados: valor não numérico, opção fora do intervalo,
campo vazio, nome duplicado, recompensa esgotada e pontos insuficientes.

## 🏆 Gamificação

- **Ações**: Reciclagem (+30), Transporte Público (+50), Economia de Energia (+20),
  Economia de Água (+15), Bicicleta (+25), Plantio de Árvore (+100), Banho Rápido (+20)
- **Níveis**: Semente → Broto (100 pts) → Árvore (300 pts) → Expert (600 pts)
- **Ranking**: ordenação por pontos com algoritmo de bubble sort implementado manualmente
- **Recompensas**: de *Plantar 1 Árvore* (200 pts) até *Mês de Energia Grátis* (2000 pts)

## 🎯 Conceitos aplicados

- Funções com passagem de parâmetros e valores de retorno
- Modularização (`import`) e separação de responsabilidades
- Listas, dicionários e tuplas (e combinações entre eles)
- Estruturas de repetição (`while`, `for`), condicionais e flags booleanas
- Ordenação manual (bubble sort) e filtragem de dados
- Tratamento de exceções com `try/except/else/finally`
