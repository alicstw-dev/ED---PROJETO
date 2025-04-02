dados = []  

def carregar_dados(nome_arquivo):
    global dados
    dados = []
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            for linha in linhas:
                partes = linha.strip().split(",")
                if len(partes) == 5:
                    dados.append([float(partes[i]) for i in range(4)] + [partes[4]])
        print(f"{len(dados)} amostras carregadas com sucesso!\n")
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")

def distancia_euclidiana(a, b):
    soma = 0
    for i in range(4):
        soma += (a[i] - b[i]) ** 2
    return soma ** 0.5

def encontrar_moda(lista):
    contagem = {}
    for item in lista:
        if item in contagem:
            contagem[item] += 1
        else:
            contagem[item] = 1
    mais_frequente = None
    max_contagem = 0
    for chave, valor in contagem.items():
        if valor > max_contagem:
            mais_frequente = chave
            max_contagem = valor
    return mais_frequente

def predizer_amostra(amostra, k):
    if not dados:
        print("Erro: Nenhuma amostra carregada. Calibre os dados primeiro!")
        return None
    
    distancias = []
    for d in dados:
        dist = distancia_euclidiana(amostra, d[:-1])
        distancias.append((dist, d[-1]))
    
    distancias.sort()
    k_vizinhos = [distancias[i][1] for i in range(k)]
    return encontrar_moda(k_vizinhos)

def predizer_por_arquivo(arquivo_entrada, arquivo_saida, k):
    if not dados:
        print("Erro: Nenhuma amostra carregada. Calibre os dados primeiro!")
        return
    try:
        with open(arquivo_entrada, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            amostras = [[float(valor) for valor in linha.strip().split(",")[:4]] for linha in linhas]
        
        resultados = []
        for amostra in amostras:
            classe = predizer_amostra(amostra, k)
            resultados.append(amostra + [classe])
        
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write("SepalLength,SepalWidth,PetalLength,PetalWidth,Classe Predita\n")
            for resultado in resultados:
                f.write(",".join(map(str, resultado)) + "\n")
        print(f"Predições salvas em {arquivo_saida}")
    except FileNotFoundError:
        print("Erro: Arquivo de entrada não encontrado.")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

def menu():
    while True:
        print("\nMENU:")
        print("1) Calibrar as amostras (carregar CSV)")
        print("2) Predizer uma flor manualmente")
        print("3) Predizer flores a partir de um arquivo")
        print("4) Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            nome_arquivo = input("Digite o nome do arquivo CSV: ")
            carregar_dados(nome_arquivo)
        elif opcao == "2":
            try:
                amostra = [float(input(f"Digite {atrib}: ")) for atrib in ["o comprimento da sépala", "a largura da sépala", "o comprimento da pétala", "a largura da pétala"]]
                k = int(input("Digite o número de vizinhos (k): "))
                classe = predizer_amostra(amostra, k)
                if classe:
                    print(f"A amostra foi classificada como: {classe}")
            except ValueError:
                print("Erro: Certifique-se de inserir valores numéricos.")
        elif opcao == "3":
            entrada = input("Digite o nome do arquivo CSV de entrada: ")
            saida = input("Digite o nome do arquivo CSV para salvar os resultados: ")
            k = int(input("Digite o número de vizinhos (k): "))
            predizer_por_arquivo(entrada, saida, k)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
