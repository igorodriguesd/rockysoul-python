<div align="center">

# 🌱 SoulUp

### Sistema de Gamificação Sustentável

*Transforme atitudes ecológicas em pontos, níveis, cartas colecionáveis e recompensas reais.*

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)
![FIAP](https://img.shields.io/badge/FIAP-Computational%20Thinking-EC1D3F?style=for-the-badge)

</div>

---

## 📖 Sobre o projeto

O **SoulUp** é um sistema de linha de comando (CLI) que gamifica ações sustentáveis do dia a dia. A cada ação registrada — reciclar, pedalar, economizar água — o usuário acumula **Pontos ECOA**, evolui de nível, gira a **Roleta de Cartas Colecionáveis** e pode trocar pontos e fragmentos por recompensas reais, tudo acompanhado por um avatar que dá dicas conforme o progresso.

Projeto desenvolvido para a disciplina **Computational Thinking Using Python** (FIAP), na 3ª Sprint do projeto **RockySoulUp**, para o cliente fictício **SoulUp**.

<br>

## ✨ Funcionalidades

<table>
<tr><td>🍃</td><td><b>Registrar ação sustentável</b></td><td>Registra a ação do dia, soma os Pontos ECOA correspondentes e aciona automaticamente a Roleta de Cartas</td></tr>
<tr><td>📊</td><td><b>Ver nível e estatísticas</b></td><td>Mostra saldo, total resgatado, histórico e progresso até o próximo nível</td></tr>
<tr><td>🎁</td><td><b>Resgatar recompensas</b></td><td>Troca Pontos ECOA por benefícios reais (créditos, cupons, descontos)</td></tr>
<tr><td>🤖</td><td><b>Sugestão do avatar</b></td><td>Mensagem motivacional personalizada de acordo com o nível atual</td></tr>
<tr><td>🏆</td><td><b>Ranking da semana</b></td><td>Compara a pontuação do usuário com outros participantes</td></tr>
<tr><td>🛠️</td><td><b>Gerenciar histórico (CRUD)</b></td><td>Submenu para listar, criar, editar e excluir ações do histórico</td></tr>
<tr><td>🎴</td><td><b>Minha Coleção</b></td><td>Exibe as 20 cartas organizadas em 5 sets temáticos, com progresso geral e por set</td></tr>
<tr><td>🏭</td><td><b>Fábrica de Cartas</b></td><td>Converte fragmentos (ganhos com cartas repetidas) em cartas que ainda faltam na coleção</td></tr>
<tr><td>🚪</td><td><b>Sair</b></td><td>Encerra o programa com segurança</td></tr>
</table>

<br>

## 🌳 Jornada de níveis

<div align="center">

`🌱 Semente`   →   `🌿 Broto`   →   `🌳 Árvore`   →   `🏅 Expert`

**0 pts&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;100 pts&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;300 pts&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;600 pts**

</div>

<br>

## 🎴 Roleta e Cartas Colecionáveis

A cada ação sustentável registrada, o sistema gira automaticamente uma roleta que sorteia uma cartinha entre **20 cartas**, distribuídas em **5 sets temáticos** de 4 cartas cada:

<div align="center">

| Set | Tema | Cartas |
|---|---|---|
| 🧺 Recursos | Consumo consciente | Reciclagem · Reutilização · Sacola Reutilizável · Redução de Desperdício |
| 💧 Guardiões da Água | Preservação hídrica | Economia de Água · Banho Rápido · Garrafa Reutilizável · Captação de Chuva |
| 🏙️ Cidade Verde | Sustentabilidade urbana | Bicicleta · Transporte Público · Mobilidade Elétrica · Ciclovia |
| ⚡ Energia Limpa | Fontes renováveis | Economia de Energia · Iluminação Eficiente · Energia Solar · Energia Eólica |
| 🌾 Cultivo | Agricultura sustentável | Plantio · Compostagem · Horta Doméstica · Agrofloresta |

</div>

**Raridades, chances e fragmentos:**

<div align="center">

| Raridade | Chance de encontrar | Fragmentos por repetida | Custo p/ montar na Fábrica |
|---|---|---|---|
| Comum | 75% | +3 | 10 |
| Incomum | 55% | +5 | 16 |
| Rara | 35% | +10 | 32 |
| Épica | 20% | +20 | 70 |
| Lendária | 10% | +40 | 140 |

</div>

- Independentemente da raridade sorteada, há ainda **8% de chance** de a carta vir na versão **brilhante** (acabamento especial, não altera raridade nem pontuação).
- Se a carta sorteada já estiver na coleção, o usuário recebe **fragmentos** em vez de uma cópia duplicada.
- Ao completar as 4 cartas de um set, a **Química de Set** é ativada e credita **+150 créditos de coleção** (uma única vez por set).
- Na **Fábrica de Cartas**, os fragmentos acumulados podem ser trocados por qualquer carta que ainda falte na coleção.

<br>

## 🗂️ Estrutura do projeto

```
soulup/
├── menu-principal.py   → Interface: menus, submenu CRUD, Coleção, Fábrica de Cartas e loop principal ▶ execute este arquivo
└── soulup.py           → Núcleo: dados, cálculo de pontos, roleta de cartas, validações e regras de negócio
```

> `menu-principal.py` importa `soulup.py` como módulo e só orquestra a navegação entre telas — toda regra de negócio fica isolada no núcleo.

<br>

## ▶️ Como executar

**Pré-requisito:** Python 3.10+ (usa `match/case`)

```bash
python3 menu-principal.py
```

> Os dois arquivos precisam estar na mesma pasta.

<br>

## 🖥️ Preview

```
=== DASHBOARD SOULUP ===
[ Pontos Disponíveis: 130 | Já Resgatados: 0 | Nível: Broto ]
[ Cartas: 4/20 | Fragmentos: 12 | Créditos de Coleção: 0 ]
---------------------------------------------------------------------------
1 - Registrar ação sustentável (Criar)
2 - Ver Meu Nível e Estatísticas
3 - Resgatar Recompensas (Benefícios Reais)
4 - Sugestão do Avatar
5 - Ver Ranking da Semana
6 - Gerenciar Histórico de Ações (CRUD)
7 - Ver Minha Coleção de Cartas
8 - Fábrica de Cartas (Trocar Fragmentos)
9 - Sair
Escolha:
```

<br>

## 🛠️ Requisitos técnicos atendidos

| Requisito | Como foi implementado |
|---|---|
| **Menu com submenus / CRUD** | Menu principal com 9 opções + submenu dedicado ao CRUD do histórico (Create · Read · Update · Delete) |
| **Definição de funções** | Lógica organizada em funções pequenas e reutilizáveis, com docstrings documentando parâmetros e retorno; dados guardados em lista de tuplas (`historico`), lista de dicionários (`ranking`) e dicionário de coleção (`colecao`) |
| **Tratamento de erros** | Blocos `try / except / else / finally` nas operações de inserção, edição e exclusão de dados, incluindo o giro da roleta e a montagem de cartas na Fábrica |
| **Validação de dados** | Função central `validar_opcao_numerica()` garante entrada numérica e dentro do intervalo esperado antes de qualquer processamento |

<br>

## 👥 Equipe — RockySoulUp

<div align="center">

| Miguel | Diego Gomes | Igor Rodrigues | Rafael Santos |
|:---:|:---:|:---:|:---:|

</div>

<div align="center">

<sub>Computational Thinking Using Python · FIAP</sub>

</div>