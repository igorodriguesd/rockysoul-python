<div align="center">

# 🌱 SoulUp

### Sistema de Gamificação Sustentável

*Transforme atitudes ecológicas em pontos, níveis e recompensas reais.*

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)
![FIAP](https://img.shields.io/badge/FIAP-Computational%20Thinking-EC1D3F?style=for-the-badge)

</div>

---

## 📖 Sobre o projeto

O **SoulUp** é um sistema de linha de comando (CLI) que gamifica ações sustentáveis do dia a dia. A cada ação registrada — reciclar, pedalar, economizar água — o usuário acumula **Pontos ECOA**, evolui de nível e pode trocar esses pontos por recompensas reais, tudo acompanhado por um avatar que dá dicas conforme o progresso.

Projeto desenvolvido para a disciplina **Computational Thinking Using Python** (FIAP), na 3ª Sprint do projeto **RockySoulUp**, para o cliente fictício **SoulUp**.

<br>

## ✨ Funcionalidades

<table>
<tr><td>🍃</td><td><b>Registrar ação sustentável</b></td><td>Registra a ação do dia e soma os Pontos ECOA correspondentes</td></tr>
<tr><td>📊</td><td><b>Ver nível e estatísticas</b></td><td>Mostra saldo, total resgatado, histórico e progresso até o próximo nível</td></tr>
<tr><td>🎁</td><td><b>Resgatar recompensas</b></td><td>Troca Pontos ECOA por benefícios reais (créditos, cupons, descontos)</td></tr>
<tr><td>🤖</td><td><b>Sugestão do avatar</b></td><td>Mensagem motivacional personalizada de acordo com o nível atual</td></tr>
<tr><td>🏆</td><td><b>Ranking da semana</b></td><td>Compara a pontuação do usuário com outros participantes</td></tr>
<tr><td>🛠️</td><td><b>Gerenciar histórico (CRUD)</b></td><td>Submenu para listar, criar, editar e excluir ações do histórico</td></tr>
<tr><td>🚪</td><td><b>Sair</b></td><td>Encerra o programa com segurança</td></tr>
</table>

<br>

## 🌳 Jornada de níveis

<div align="center">

`🌱 Semente`   →   `🌿 Broto`   →   `🌳 Árvore`   →   `🏅 Expert`

**0 pts&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;100 pts&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;300 pts&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;600 pts**

</div>

<br>

## 🗂️ Estrutura do projeto

```
soulup/
├── menu-principal.py   → Interface: menus, submenu CRUD e loop principal ▶ execute este arquivo
└── soulup.py           → Núcleo: dados, cálculo de pontos, validações e regras de negócio
```

> `menu-principal.py` importa `soulup.py` como módulo (`import soulup as core`) e só orquestra a navegação entre telas — toda regra de negócio fica isolada no núcleo.

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
---------------------------------------------------------------------------
1 - Registrar ação sustentável (Criar)
2 - Ver Meu Nível e Estatísticas
3 - Resgatar Recompensas (Benefícios Reais)
4 - Sugestão do Avatar
5 - Ver Ranking da Semana
6 - Gerenciar Histórico de Ações (CRUD)
7 - Sair
Escolha:
```

<br>

## 🛠️ Requisitos técnicos atendidos

| Requisito | Como foi implementado |
|---|---|
| **Menu com submenus / CRUD** | Menu principal com 7 opções + submenu dedicado ao CRUD do histórico (Create · Read · Update · Delete) |
| **Definição de funções** | Lógica organizada em funções pequenas e reutilizáveis, com docstrings documentando parâmetros e retorno; dados guardados em lista de tuplas (`historico`) e lista de dicionários (`ranking`) |
| **Tratamento de erros** | Blocos `try / except / else / finally` nas operações de inserção, edição e exclusão de dados |
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