import csv
import matplotlib.pyplot as plt

train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next() 

claseNumeros = {}

for label in archivo_csv:
	if label[0] not in claseNumeros:
			claseNumeros[label[0]] = 0
	claseNumeros[label[0]] += 1
		
train.close()

archivo = open ("resultadoClases.csv","w")
archivo_csv = csv.writer(archivo)
registros = []
registros.append(("Numeros","Cantidad"))
	
for clave in claseNumeros:
		tupla = (clave,claseNumeros[clave[0]])
		registros.append(tupla)
archivo_csv.writerows(registros)

archivo.close()
