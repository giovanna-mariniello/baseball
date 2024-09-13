from model.model import Model

mymodel = Model()
#print(mymodel.get_all_anni())
mymodel.build_grafo(2015)

v0 = list(mymodel._grafo.nodes)[2]

path, score = mymodel.get_percorso(v0)
print(len(path))
print(score)
