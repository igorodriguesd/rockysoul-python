import json
import urllib.request


def consumir_api_clima(latitude=-23.55, longitude=-46.63):
    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(latitude)
    url = url + "&longitude=" + str(longitude)
    url = url + "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    url = url + "&timezone=America%2FSao_Paulo"

    try:
        resposta = urllib.request.urlopen(url, timeout=15)
        payload = json.loads(resposta.read().decode("utf-8"))

        atual = payload["current"]
        temp = atual["temperature_2m"]
        umid = atual["relative_humidity_2m"]
        vento = atual["wind_speed_10m"]

        if temp >= 30:
            dica = "Dia quente: tome Banho Rapido e Economize Agua."
        elif temp <= 17:
            dica = "Dia frio: Economize Energia e use Transporte Publico."
        else:
            dica = "Clima bom: va de Bicicleta e ganhe Pontos ECOA!"

        print("\n--- CLIMA ATUAL (API Open-Meteo) ---")
        print("Temperatura:", temp, "C")
        print("Umidade:", umid, "%")
        print("Vento:", vento, "km/h")
        print("Dica SoulUp:", dica)

        return {"temperatura_c": temp, "umidade_pct": umid, "vento_kmh": vento, "dica_sustentavel": dica}

    except Exception as erro:
        print("Erro ao buscar o clima:", erro)
        return {"erro": str(erro)}


def consultar_cep_api(cep):
    so_numeros = ""
    for letra in cep:
        if letra.isdigit():
            so_numeros = so_numeros + letra

    if len(so_numeros) != 8:
        print("CEP invalido. Exemplo: 01310-100")
        return {"erro": "CEP invalido"}

    url = "https://viacep.com.br/ws/" + so_numeros + "/json/"

    try:
        resposta = urllib.request.urlopen(url, timeout=15)
        dados = json.loads(resposta.read().decode("utf-8"))

        if "erro" in dados:
            print("CEP nao encontrado.")
            return {"erro": "CEP nao encontrado"}

        print("\n--- ENDERECO ---")
        print(dados.get("logradouro", ""), "-", dados.get("bairro", ""))
        print(dados.get("localidade", ""), "/", dados.get("uf", ""))
        print("CEP:", dados.get("cep", ""))

        return dados

    except Exception as erro:
        print("Erro ao buscar o CEP:", erro)
        return {"erro": str(erro)}
