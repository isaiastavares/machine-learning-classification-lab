from collections import Counter
import pandas as pd

# teste inicial : home, busca, logado => comprou
# home, busca
# home, logado
# busca, logado
# busca: 85.71% (7 testes)

#df = data frame
df = pd.read_csv('situacao_do_cliente.csv')

X_df = df[['recencia', 'frequencia', 'semanas_de_inscricao']]
Y_df = df['situacao']

#ira transformar a coluna busca em binario
Xdummies_df = pd.get_dummies(X_df)
Ydummies_df = Y_df

# transforma em array
X = Xdummies_df.values
Y = Ydummies_df.values

# 80% para treino e 10% para teste e 10% para validacao
porcentagem_de_treino = 0.8
porcentagem_de_teste = 0.1

tamanho_de_treino = int(porcentagem_de_treino * len(Y))
tamanho_de_teste = int(porcentagem_de_teste * len(Y))
tamanho_de_validacao = int(len(Y) - tamanho_de_treino - tamanho_de_teste)

treino_dados = X[0:tamanho_de_treino]
treino_marcacoes = Y[0:tamanho_de_treino]

fim_de_teste = tamanho_de_treino + tamanho_de_teste
teste_dados = X[tamanho_de_treino:fim_de_teste]
teste_marcacoes = Y[tamanho_de_treino:fim_de_teste]

validacao_dados = X[fim_de_teste:]
validacao_marcacoes = Y[fim_de_teste:]

def fit_and_predict(nome, modelo, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes):
	modelo.fit(treino_dados, treino_marcacoes)

	resultado = modelo.predict(teste_dados)
	acertos = (resultado == teste_marcacoes)

	total_de_acertos = sum(acertos)
	total_de_elementos = len(teste_dados)
	taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

	msg = "Taxa de acerto do {0}: {1}".format(nome, taxa_de_acerto)
	print(msg)
	return taxa_de_acerto

resultados = {}

# 0 => 0 1 => 1, 2 LinearSVC 0 ou do resto (38%, resto 62%)
# 0 => 0, 2 1 => 1 LinearSVC 1 ou do resto (44%, resto 56%)
# 0 => 0, 1 2 => 2 LinearSVC 2 ou do resto (20%, resto 80%)
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
modeloOneVsRest = OneVsRestClassifier(LinearSVC(random_state = 0))
resultadoOneVsRest = fit_and_predict("OneVsRest", modeloOneVsRest, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes)
resultados[resultadoOneVsRest] = modeloOneVsRest

from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
modeloOneVsOne = OneVsOneClassifier(LinearSVC(random_state = 0))
resultadoOneVsOne = fit_and_predict("OneVsOne", modeloOneVsOne, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes)
resultados[resultadoOneVsOne] = modeloOneVsOne

from sklearn.naive_bayes import MultinomialNB
modeloMultinomial = MultinomialNB()
resultadoMultinomial = fit_and_predict("MultinomialNB", modeloMultinomial, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes)
resultados[resultadoMultinomial] = modeloMultinomial

from sklearn.ensemble import AdaBoostClassifier
modeloAdaBoost = AdaBoostClassifier()
resultadoAdaBoost = fit_and_predict("AdaBoostClassifier", modeloAdaBoost, treino_dados, treino_marcacoes, teste_dados, teste_marcacoes)
resultados[resultadoAdaBoost] = modeloAdaBoost

maximo = max(resultados)
vencedor = resultados[maximo]
print("Vencedor")
print(vencedor)

resultado = vencedor.predict(validacao_dados)
acertos = (resultado == validacao_marcacoes)

total_de_acertos = sum(acertos)
total_de_elementos = len(validacao_marcacoes)
taxa_de_acerto = 100.0 * total_de_acertos / total_de_elementos

msg = "Taxa de acerto do vencedor entre os dois algoritmos no mundo real: {0}".format(taxa_de_acerto)
print(msg)

# a eficacia do algoritmo que chuta tudo um unico valor
#acerto_de_um = len(Y[Y=='sim'])
#acerto_de_zero = len(Y[Y=='nao'])

#acerto_de_um = list(Y).count('sim')
#acerto_de_zero = list(Y).count('nao')

acerto_base = max(Counter(validacao_marcacoes).itervalues())
taxa_de_acerto_base = 100.0 * acerto_base / len(validacao_marcacoes)

print("Taxa de acerto base: %.2f" % taxa_de_acerto_base)
print("Total de testes: %d" % len(validacao_dados))