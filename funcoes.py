from dados import NIVEIS


def pausar():
    input("\nPressione Enter para continuar...")


def calcular_nivel(pontos):
    nivel = NIVEIS[0][0]
    for i in range(len(NIVEIS)):
        if pontos >= NIVEIS[i][1]:
            nivel = NIVEIS[i][0]
    return nivel


def proximo_nivel(pontos):
    nome_atual = calcular_nivel(pontos)
    for i in range(len(NIVEIS)):
        if NIVEIS[i][0] == nome_atual and i + 1 < len(NIVEIS):
            return [NIVEIS[i + 1][0], NIVEIS[i + 1][1] - pontos]
    return None


def buscar_usuario(usuarios, nome):
    for usuario in usuarios:
        if usuario["nome"].lower() == nome.lower():
            return usuario
    return None


def filtrar_acoes_por_pontos(acoes, minimo):
    resultado = []
    for acao in acoes:
        if acao[1] >= minimo:
            resultado.append(acao)
    return resultado


def ordenar_ranking(usuarios):
    copia = []
    for u in usuarios:
        copia.append(u)
    for i in range(len(copia)):
        for j in range(len(copia) - 1 - i):
            if copia[j]["pontos"] < copia[j + 1]["pontos"]:
                aux = copia[j]
                copia[j] = copia[j + 1]
                copia[j + 1] = aux
    return copia


def historico_do_usuario(historico, nome):
    registros = []
    for registro in historico:
        if registro[0].lower() == nome.lower():
            registros.append(registro)
    return registros


def identificar_usuario(sistema):
    usuarios = sistema["usuarios"]
    print("\n--- IDENTIFICAÇÃO ---")
    logado = None
    while logado is None:
        nome = input("Nome: ").strip()
        if nome == "":
            print("Preencha o nome!")
        else:
            logado = buscar_usuario(usuarios, nome)
            if logado is not None:
                print(f"Bem-vindo de volta, {logado['nome']}!")
            else:
                novo = {"nome": nome, "pontos": 0, "resgatados": 0}
                usuarios.append(novo)
                print("Cadastro criado com sucesso! Bem-vindo!")
                logado = novo
    return logado


def registrar_acao(sistema, usuario):
    acoes = sistema["acoes"]
    print("\nAções Sustentáveis disponíveis:")
    indice = 1
    for acao in acoes:
        print(f"{indice} - {acao[0]} ({acao[1]} pts)")
        indice = indice + 1
    try:
        escolha = int(input("\nQual ação sustentável você realizou hoje? "))
    except ValueError:
        print("Erro: digite um número válido!")
    else:
        if escolha < 1 or escolha > len(acoes):
            print("Erro: opção inválida!")
        else:
            nome_acao = acoes[escolha - 1][0]
            pontos = acoes[escolha - 1][1]
            usuario["pontos"] = usuario["pontos"] + pontos
            sistema["historico"].append([usuario["nome"], nome_acao, pontos])
            print(f"Boa! Você ganhou +{pontos} Pontos ECOA com: {nome_acao}!")
    finally:
        pausar()


def ver_nivel_estatisticas(sistema, usuario):
    print(f"\n--- SEU NÍVEL ATUAL: {calcular_nivel(usuario['pontos'])} ---")
    print(f"Saldo Disponível: {usuario['pontos']} Pontos ECOA")
    print(f"Total já Resgatado: {usuario['resgatados']} Pontos ECOA")

    registros = historico_do_usuario(sistema["historico"], usuario["nome"])
    if len(registros) == 0:
        print("Histórico de Missões: vazio. Comece hoje!")
    else:
        print("Histórico de Missões:")
        for registro in registros:
            print(f"  • {registro[1]} (+{registro[2]} pts)")

    proximo = proximo_nivel(usuario["pontos"])
    if proximo is None:
        print("Você alcançou o nível máximo! Você é lenda!")
    else:
        print(f"Progresso: Faltam {proximo[1]} pontos para evoluir para {proximo[0]}!")
    pausar()


def resgatar_recompensa(sistema, usuario):
    recompensas = sistema["recompensas"]
    print("\n=== VITRINE DE RECOMPENSAS SOULUP ===")
    indice = 1
    for r in recompensas:
        if r["estoque"] > 0:
            situacao = f"estoque {r['estoque']}"
        else:
            situacao = "ESGOTADO"
        print(f"{indice} - {r['titulo']} ---- {r['custo']} pts ({situacao})")
        indice = indice + 1
    print("0 - Voltar")
    try:
        escolha = int(input(f"\nSeu Saldo: {usuario['pontos']} pts. Escolha um benefício: "))
    except ValueError:
        print("Erro: digite um número válido!")
    else:
        if escolha == 0:
            print("Operação cancelada.")
        elif escolha < 0 or escolha > len(recompensas):
            print("Erro: opção inválida!")
        else:
            recompensa = recompensas[escolha - 1]
            if recompensa["estoque"] <= 0:
                print("Erro: recompensa esgotada!")
            elif usuario["pontos"] < recompensa["custo"]:
                print(
                    f"Erro: pontos insuficientes! "
                    f"Você precisa de {recompensa['custo']}, mas tem apenas {usuario['pontos']}."
                )
            else:
                recompensa["estoque"] = recompensa["estoque"] - 1
                usuario["pontos"] = usuario["pontos"] - recompensa["custo"]
                usuario["resgatados"] = usuario["resgatados"] + recompensa["custo"]
                print(f"\nSucesso! Você resgatou: {recompensa['titulo']}!")
                print(f"Foram utilizados {recompensa['custo']} Pontos ECOA.")
    finally:
        pausar()


def sugestao_avatar(usuario):
    pontos = usuario["pontos"]
    if pontos < 100:
        return "Avatar: Registre missões diárias para fazermos nossa semente brotar!"
    elif pontos < 300:
        return "Avatar: Crescendo firme! Junte pontos para resgatar benefícios reais!"
    else:
        proximo = proximo_nivel(pontos)
        if proximo is None:
            return "Avatar: Você é Expert! O planeta agradece, lenda!"
        else:
            return (
                f"Avatar: Parabéns pelo nível {calcular_nivel(pontos)}! "
                f"Faltam só {proximo[1]} pontos para virar {proximo[0]}."
            )


def ver_ranking(sistema, usuario):
    ordenados = ordenar_ranking(sistema["usuarios"])
    print("\n==============================")
    print("      RANKING DA SEMANA       ")
    print("==============================")
    posicao = 1
    for u in ordenados:
        if u["nome"] == usuario["nome"]:
            print(f"-> {posicao}º {u['nome']:<15} | {u['pontos']} pts * (Sua posição)")
        else:
            print(f"   {posicao}º {u['nome']:<15} | {u['pontos']} pts")
        posicao = posicao + 1
    print("==============================")
    pausar()


def cadastrar_usuario(sistema):
    usuarios = sistema["usuarios"]
    try:
        nome = input("Nome: ").strip()
    except ValueError:
        print("Erro: dados inválidos!")
    else:
        erro = ""
        if nome == "":
            erro = "O nome é obrigatório!"
        elif buscar_usuario(usuarios, nome) is not None:
            erro = "Já existe um usuário com este nome!"
        if erro != "":
            print(f"Erro: {erro}")
        else:
            usuarios.append({"nome": nome, "pontos": 0, "resgatados": 0})
            print(f"Usuário '{nome}' cadastrado com sucesso!")
    finally:
        pausar()


def alterar_usuario(sistema):
    usuarios = sistema["usuarios"]
    try:
        nome = input("Nome do usuário a alterar: ").strip()
    except ValueError:
        print("Erro: dados inválidos!")
    else:
        usuario = buscar_usuario(usuarios, nome)
        if usuario is None:
            print("Erro: usuário não encontrado!")
        else:
            novo_nome = input(f"Novo nome [{usuario['nome']}]: ").strip()
            erro = ""
            if novo_nome != "" and novo_nome.lower() != usuario["nome"].lower():
                if buscar_usuario(usuarios, novo_nome) is not None:
                    erro = "Este nome já está em uso!"
            if erro != "":
                print(f"Erro: {erro}")
            else:
                if novo_nome != "":
                    usuario["nome"] = novo_nome
                print("Usuário alterado com sucesso!")
    finally:
        pausar()


def excluir_usuario(sistema):
    usuarios = sistema["usuarios"]
    try:
        nome = input("Nome do usuário a excluir: ").strip()
    except ValueError:
        print("Erro: dados inválidos!")
    else:
        usuario = buscar_usuario(usuarios, nome)
        if usuario is None:
            print("Erro: usuário não encontrado!")
        else:
            confirmou = input(f"Confirmar exclusão de '{usuario['nome']}'? (S/N): ").strip().upper()
            if confirmou == "S":
                usuarios.remove(usuario)
                print("Usuário excluído com sucesso!")
            else:
                print("Exclusão cancelada.")
    finally:
        pausar()


def listar_usuarios(usuarios):
    if len(usuarios) == 0:
        print("Nenhum usuário cadastrado.")
    for u in usuarios:
        print(f"• {u['nome']} | {u['pontos']} pts | {u['resgatados']} resgatados")
    pausar()


def listar_acoes_simples(acoes):
    if len(acoes) == 0:
        print("Nenhuma ação cadastrada.")
    indice = 1
    for acao in acoes:
        print(f"{indice} - {acao[0]} ({acao[1]} pts)")
        indice = indice + 1


def incluir_acao(sistema):
    acoes = sistema["acoes"]
    try:
        nome = input("Nome da ação: ").strip()
        pontos = int(input("Pontos da ação: "))
    except ValueError:
        print("Erro: os pontos devem ser um número inteiro!")
    else:
        erro = ""
        if nome == "":
            erro = "O nome é obrigatório!"
        elif pontos <= 0:
            erro = "Os pontos devem ser maiores que zero!"
        else:
            for acao in acoes:
                if acao[0].lower() == nome.lower():
                    erro = "Já existe uma ação com este nome!"
        if erro != "":
            print(f"Erro: {erro}")
        else:
            acoes.append([nome, pontos])
            print(f"Ação '{nome}' cadastrada com sucesso!")
    finally:
        pausar()


def alterar_acao(sistema):
    acoes = sistema["acoes"]
    print("\nAções cadastradas:")
    listar_acoes_simples(acoes)
    try:
        escolha = int(input("\nNúmero da ação a alterar (0 cancela): "))
        novos_pontos = int(input("Novos pontos: "))
    except ValueError:
        print("Erro: digite números válidos!")
    else:
        if escolha == 0:
            print("Alteração cancelada.")
        elif escolha < 0 or escolha > len(acoes):
            print("Erro: opção inválida!")
        elif novos_pontos <= 0:
            print("Erro: os pontos devem ser maiores que zero!")
        else:
            acoes[escolha - 1][1] = novos_pontos
            print("Ação alterada com sucesso!")
    finally:
        pausar()


def excluir_acao(sistema):
    acoes = sistema["acoes"]
    print("\nAções cadastradas:")
    listar_acoes_simples(acoes)
    try:
        escolha = int(input("\nNúmero da ação a excluir (0 cancela): "))
    except ValueError:
        print("Erro: digite um número válido!")
    else:
        if escolha == 0:
            print("Exclusão cancelada.")
        elif escolha < 0 or escolha > len(acoes):
            print("Erro: opção inválida!")
        else:
            removida = acoes.pop(escolha - 1)
            print(f"Ação '{removida[0]}' excluída com sucesso!")
    finally:
        pausar()


def filtrar_acoes(acoes):
    try:
        minimo = int(input("Filtrar ações com quantos pontos ou mais? "))
    except ValueError:
        print("Erro: digite um número válido!")
    else:
        if minimo < 0:
            print("Erro: o mínimo não pode ser negativo!")
        else:
            resultado = filtrar_acoes_por_pontos(acoes, minimo)
            if len(resultado) == 0:
                print("Nenhuma ação encontrada nesse filtro.")
            for acao in resultado:
                print(f"• {acao[0]} ({acao[1]} pts)")
    finally:
        pausar()


def listar_recompensas(recompensas):
    if len(recompensas) == 0:
        print("Nenhuma recompensa cadastrada.")
    for r in recompensas:
        print(f"• {r['titulo']} | {r['custo']} pts | estoque {r['estoque']}")


def incluir_recompensa(sistema):
    recompensas = sistema["recompensas"]
    try:
        titulo = input("Título: ").strip()
        custo = int(input("Custo em pontos: "))
        estoque = int(input("Estoque: "))
    except ValueError:
        print("Erro: custo e estoque devem ser números!")
    else:
        erro = ""
        if titulo == "":
            erro = "O título é obrigatório!"
        elif custo <= 0 or estoque < 0:
            erro = "O custo deve ser positivo e o estoque não pode ser negativo!"
        else:
            for r in recompensas:
                if r["titulo"].lower() == titulo.lower():
                    erro = "Já existe recompensa com este título!"
        if erro != "":
            print(f"Erro: {erro}")
        else:
            descricao = input("Descrição (opcional): ").strip()
            nova = {"titulo": titulo, "descricao": descricao, "custo": custo, "estoque": estoque}
            recompensas.append(nova)
            print("Recompensa cadastrada com sucesso!")
    finally:
        pausar()


def alterar_recompensa(sistema):
    recompensas = sistema["recompensas"]
    print("\nRecompensas cadastradas:")
    listar_recompensas(recompensas)
    try:
        escolha = int(input("\nNúmero da recompensa a alterar (0 cancela): "))
        novo_custo = int(input("Novo custo: "))
        novo_estoque = int(input("Novo estoque: "))
    except ValueError:
        print("Erro: digite números válidos!")
    else:
        if escolha == 0:
            print("Alteração cancelada.")
        elif escolha < 0 or escolha > len(recompensas):
            print("Erro: opção inválida!")
        elif novo_custo <= 0 or novo_estoque < 0:
            print("Erro: o custo deve ser positivo e o estoque não pode ser negativo!")
        else:
            recompensas[escolha - 1]["custo"] = novo_custo
            recompensas[escolha - 1]["estoque"] = novo_estoque
            print("Recompensa alterada com sucesso!")
    finally:
        pausar()


def excluir_recompensa(sistema):
    recompensas = sistema["recompensas"]
    print("\nRecompensas cadastradas:")
    listar_recompensas(recompensas)
    try:
        escolha = int(input("\nNúmero da recompensa a excluir (0 cancela): "))
    except ValueError:
        print("Erro: digite um número válido!")
    else:
        if escolha == 0:
            print("Exclusão cancelada.")
        elif escolha < 0 or escolha > len(recompensas):
            print("Erro: opção inválida!")
        else:
            removida = recompensas.pop(escolha - 1)
            print(f"Recompensa '{removida['titulo']}' excluída com sucesso!")
    finally:
        pausar()
