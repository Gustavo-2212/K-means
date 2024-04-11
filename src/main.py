from bokeh.plotting import figure, show, output_file, gridplot
import random


grupos = ('blue', 'red', 'green', 'brown', 'purple', 'midnightblue', 'teal', 'lawngreen', 'deeppink')
E = []
iteracao_acumulada = 0

def calcula_distancia(x1, y1, x2, y2):
    return ( (x1 - x2)**2 + (y1 - y2)**2 )**(.5)


def read_data(X, Y):
    with open("./data/dados.txt", "r") as arq:
        linhas = arq.readlines() # [first line, second line, ...] | first line = 'x y\n'
        for linha in linhas:
            valores = linha.split()
            X.append( float(valores[0]) )
            Y.append( float(valores[1][:-1]) )
        
    return None


def plot_spread_graph(X, Y, pontos_grupo=None, centroides=None):
    output_file("./tmp/pontos.html")
    
    grafico_dispersao = figure(title="Distribuição de Pontos", x_axis_label='X', y_axis_label='Y', width=800, tools=["pan","box_zoom","wheel_zoom","hover","save","reset"])
    
    grafico_lms = None

    if centroides:
        for i, ponto in enumerate(pontos_grupo):
            grafico_dispersao.square(X[i], Y[i], legend_label="Dados", size=7, color=grupos[ponto % len(grupos)])
            
        for centroide in centroides:
            grafico_dispersao.dot(centroide[0], centroide[1], legend_label="Centródes", size=30, color="black")
            
            
        Erro_X = [i for i in range(len(E))]
        grafico_lms = figure(title="Erro LMS", x_axis_label='Ciclos', y_axis_label='E', width=800, tools=["pan","box_zoom","wheel_zoom","hover","save","reset"])
        grafico_lms.line(Erro_X, E, legend_label="LMS", color="red")
    else:
        grafico_dispersao.square(X, Y, legend_label="Dados", size=7, color="blue")
    
    layout = gridplot([[grafico_dispersao], [grafico_lms]])
    show(layout)


def calcula_media(X, Y, pontos_grupo, centroides):
    media = [0 for _ in centroides]
    elementos = [0 for _ in centroides]
    for i, ponto in enumerate(pontos_grupo):
        media[ponto] += calcula_distancia(X[i], Y[i], centroides[ponto][0], centroides[ponto][1])
        elementos[ponto] += 1
        
    for i in range(len(media)):
        media[i] /= elementos[i] if elementos[i] != 0 else 1

    return media


def calcula_pesos(centroides, copia_x, copia_y):
    dist = [0 for _ in range(len(copia_x))]
    pesos = [0 for _ in range(len(copia_x))]
    for i in range(len(copia_x)):
        for centroide in centroides:
            dist[i] = max(dist[i], calcula_distancia(centroide[0], centroide[1], copia_x[i], copia_y[i]))
            pesos[i] = dist[i] ** 2
            
    return pesos


def inicializa_centroides(X, Y, k):
    copia_x, copia_y = X[::], Y[::]
    i = random.randint(0, len(X)-1)
    centroides = [[X[i], Y[i]]]
    k -= 1
    
    copia_x = copia_x[:i] + copia_x[i+1:]
    copia_y = copia_y[:i] + copia_y[i+1:]
    
    pesos = calcula_pesos(centroides, copia_x, copia_y)
    
    while(k != 0):      
        i = random.choices(range(len(pesos)), weights=pesos)[0] 
        centroides.append([copia_x[i], copia_y[i]])
        
        copia_x = copia_x[:i] + copia_x[i+1:]
        copia_y = copia_y[:i] + copia_y[i+1:]
        
        pesos = calcula_pesos(centroides, copia_x, copia_y)
        
        k -= 1
    
    return centroides


def calcula_k(X, Y):
    pontos_grupo, centroides, iteracao = k_means(X, Y)
    media = calcula_media(X, Y, pontos_grupo, centroides)
    k = 3
    media_anterior = 0
    
    while abs(media_anterior - sum(media)) > 1:
        media_anterior = sum(media)
        pontos_grupo, centroides, it = k_means(X, Y, k)
        iteracao += it
        media = calcula_media(X, Y, pontos_grupo, centroides)
        k += 1
    
    pontos_grupo, centroides, it = k_means(X, Y, k)
    
    return pontos_grupo, centroides, it + iteracao


def k_means(X, Y, k=2):
    centroides = inicializa_centroides(X, Y, k)
    pontos_grupo = [-1 for _ in X]
    diferenca = True
    iteracao = 0
    
    print(f"\t=> {centroides}")
    
    while(diferenca):
        iteracao += 1
        
        # Encontra a centróide "pai" de cada ponto e armazena em um vetor 'pontos_grupo'
        for i in range(len(X)):
            ponto_centroides = [calcula_distancia(X[i], Y[i], centroide[0], centroide[1]) for centroide in centroides]
            pontos_grupo[i] = ponto_centroides.index( min(ponto_centroides) )

        # Faz a 'deep copy' das coordenadas das centróides deste ciclo antes de serem atualizadas
        centroides_anteriores = [[centroides[i][0], centroides[i][1]] for i in range(k)]
        
        # Calcula a média das distâncias dos pontos as suas centróides, para depois serem atualizadas
        for centroide_index, centroide in enumerate(centroides):
            media = [0,0]
            elementos = 0
            for i in range(len(pontos_grupo)):
                if pontos_grupo[i] == centroide_index:
                    media[0] += X[i]
                    media[1] += Y[i]
                    elementos += 1
            
            if elementos != 0:
                centroide[0] = (media[0] / elementos)
                centroide[1] = (media[1] / elementos)
        
        # Faz a comparação entre as centróides do ciclo anterior (antes de atualizar) com as do ciclo corrente (atualizadas)
        # Se não houve alteração, chagamos na posição final da centróide
        for i in range(k):
            if centroides[i][0] != centroides_anteriores[i][0] or centroides[i][1] != centroides_anteriores[i][1]:
                diferenca = True
            else:
                diferenca = False    
        
        # Calculo do Erro
        # Média por centróide
        erro = 0
        for i, ponto_grupo in enumerate(pontos_grupo):
            erro += calcula_distancia(X[i], Y[i], centroides[ponto_grupo][0], centroides[ponto_grupo][1]) ** 2
        E.append(erro / (2 * len(X)))
    
    global iteracao_acumulada
    iteracao_acumulada += iteracao
    print(f"\t   K: {k} - Ciclos: {iteracao} ({iteracao_acumulada})\n")
    
    return pontos_grupo, centroides, iteracao


def main():
    X, Y = [], []
    
    read_data(X, Y)
    
    print("\n" + "-"*85, end="\n")
    print("[+] Centroides Iniciais:")
    pontos_grupo, centroides, iteracoes = calcula_k(X, Y)
    plot_spread_graph(X, Y, pontos_grupo, centroides)
    
    
    print("[+] Pontos e seus grupos:")
    print(f"\t=> Centróides: {len(centroides)}")
    print(f"\t=> Iterações: {iteracoes}\n")
    print("-"*85, end="\n\n")
    _ = [print(f"\t{X[i], Y[i]}\t\t\t[{grupos[pontos_grupo[i] % len(grupos)]}]") for i in range(len(pontos_grupo))]
    
    
if __name__ == "__main__":
    main()
    