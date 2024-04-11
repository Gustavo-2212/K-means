# Projeto de Aprendizado de Máquina com Clusterização de Dados (K-means) 🧠
---
### Autor
- **Nome:** Gustavo Alves de Oliveira
- **Matrícula:** 12311ECP026
- **Disciplina:** Aprendizagem de Máquina
- **Faculdade:** Universidade Federal de Uberlândia


🤖📊🔍

> Este projeto faz uso de uma base de dados simples para o teste de um algoritmo K-means++, variação do k-means convencional, com uma otimização na inicialização das centróides.



### K-means:

>O K-means é um algoritmo de clusterização amplamente utilizado em aprendizado de máquina não supervisionado. Ele foi proposto por James MacQueen em 1967, embora a versão mais conhecida tenha sido publicada por Stuart Lloyd em 1957 como um método para quantização vetorial em comunicação de dados.

#### Funcionamento:

O algoritmo K-means funciona da seguinte maneira:

1. **Inicialização**: Começa com a escolha aleatória de *k* centróides iniciais, onde *k* é o número de clusters desejados.

2. **Atribuição de pontos aos clusters**: Cada ponto de dado é atribuído ao centróide mais próximo com base em alguma medida de distância, geralmente a distância euclidiana.

3. **Atualização dos centróides**: Os centróides são recalculados como a média de todos os pontos atribuídos a cada cluster.

4. **Repetição**: Os passos 2 e 3 são repetidos até que os centróides não mudem significativamente ou até que um critério de parada seja atingido.

5. **Convergência**: Quando os centróides não mudam mais, o algoritmo converge e os clusters finais são determinados.

### K-means++:

>O K-means++ é uma extensão do K-means que melhora a inicialização dos centróides. Foi proposto por David Arthur e Sergei Vassilvitskii em 2007.

#### Inicialização dos centróides no K-means++:

1. **Escolha do primeiro centróide**: É escolhido aleatoriamente entre os pontos de dados.

2. **Escolha dos centróides subsequentes**: Os centróides restantes são escolhidos com base na distância ponderada dos centróides já escolhidos. Quanto maior a distância de um ponto a um centróide existente, maior a probabilidade de ser escolhido como um novo centróide.

3. **Repetição**: Os passos 1 e 2 são repetidos até que todos os centróides sejam escolhidos.

>O K-means++ ajuda a melhorar a convergência e a qualidade dos clusters finais, especialmente em conjuntos de dados de alta dimensionalidade.


### Estrutura do Projeto

O projeto está estruturado da seguinte forma:

- **./data**: Possui os dados para serem clusterizados;
- **./src**: Contém o código fonte;
- **./tmp**: Contém o arquivo **.html** com a representação gráfica do resultado do algoritmo K-means e a função de erro;

### Dependências do Projeto

Para executar o projeto, é necessário instalar a seguinte biblioteca Python:

- Bokeh: Biblioteca para criar visualizações interativas em navegadores da web.

```bash
pip install bokeh
```

### Como Executar o Projeto

1. Clone o repositório do projeto.
2. Instale as dependências listadas acima.
3. Execute, no diretório raiz do projeto, com o python3

### Conclusões

> Podemos ver que, ainda existe alguma aleatoriedade no sistema, portanto algumas vezes, ao executar o algoritmo mais centróides que o necessário é usada. No entanto, algumas vezes a convergência para 4 centróides é recorrente, que é a mais correta para essa base de dados.

```

🚀🔍💡

---
