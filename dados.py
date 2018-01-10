import csv

def carregar_acessos():

    #X sao as caracteristicas que eu sei
    X = []
    #Y as marcacoes (que eu nao sei) eh o que eu quero prever
    Y = []

    arquivo = open('acessos.csv', 'rb')
    leitor = csv.reader(arquivo)

    leitor.next()

    for home, como_funciona, contato, comprou in leitor:

        dado = [int(home), int(como_funciona), int(contato)]
        X.append(dado)
        Y.append(int(comprou))

    return X, Y

def carregar_buscas():

    X = []
    Y = []

    arquivo = open('buscas.csv', 'rb')
    leitor = csv.reader(arquivo)

    leitor.next()

    for home, busca, logado, comprou in leitor:

        dado = [int(home), busca, int(logado)]
        X.append(dado)
        Y.append(int(comprou))

    return X, Y
