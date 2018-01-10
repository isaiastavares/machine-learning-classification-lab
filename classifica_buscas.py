from collections import Counter
import pandas as pd

#df = data frame
df = pd.read_csv('buscas.csv')

X_df = df[['home', 'busca', 'logado']]
Y_df = df['comprou']

#ira transformar a coluna busca em binario
Xdummies_df = pd.get_dummies(X_df)
Ydummies_df = Y_df

# transforma em array
X = Xdummies_df.values
Y = Ydummies_df.values

# 90% para treino e 10% para teste
porcentagem_de_treino = 0.9
tamanho_de_treino = int(porcentagem_de_treino * len(Y))
tamanho_de_teste = len(Y) - tamanho_de_treino

treino_dados = X[:tamanho_de_treino]
treino_marcacoes = Y[:tamanho_de_treino]

teste_dados = X[-tamanho_de_teste:]
teste_marcacoes = Y[-tamanho_de_teste:]

from sklearn.naive_bayes import MultinomialNB
modelo = MultinomialNB()
modelo.fit(treino_dados, treino_marcacoes)

resultado = modelo.predict(teste_dados)
acertos = (resultado == teste_marcacoes)

total_de_acertos = sum(acertos)
total_de_elementos = len(teste_dados)
taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

print("Taxa de acerto do algoritmo: %.2f" % taxa_de_acerto)
print(total_de_elementos)

# a eficacia do algoritmo que chuta tudo um unico valor
#acerto_de_um = len(Y[Y=='sim'])
#acerto_de_zero = len(Y[Y=='nao'])

#acerto_de_um = list(Y).count('sim')
#acerto_de_zero = list(Y).count('nao')

acerto_base = max(Counter(teste_marcacoes).itervalues())
taxa_de_acerto_base = 100.0 * acerto_base / len(teste_marcacoes)

print("Taxa de acerto base: %.2f" % taxa_de_acerto_base)
