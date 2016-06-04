import csv

import matplotlib.pyplot as plt
NUM_PIXELES = 784
NUM_CLASES = 10

wInicial = range(0,NUM_PIXELES + 1)
vectorw = range(0,NUM_CLASES)
contador = 0

for i in range(0,NUM_PIXELES + 1):
	wInicial[i] = -1

for i in range(0,NUM_CLASES):
	vectorw[i] = wInicial

def productoInterno(x,w):
	vectorTemp = x[:]
	vectorTemp[0] = 1
	producto = 0
	for i in range(0,NUM_PIXELES + 1):
		producto += int(vectorTemp[i])*w[i]
	return producto
	
def suma(x,w):
	vectorTemp = x[:]
	vectorTemp[0] = 1
	vectorSuma = range(NUM_PIXELES+1)
	for i in range(0,NUM_PIXELES+1):
		vectorSuma[i] = int(vectorTemp[i]) + int(w[i])
	return vectorSuma

def calcularNuevoW(vector):
	wNuevo = suma(vector,vectorw[int(vector[0])])
	vectorw[int(vector[0])] = wNuevo
	return wNuevo

def perceptron(posicionFila,lista):
	fila = lista[posicionFila]
	wNuevo = calcularNuevoW(fila)
	contadorPosiciones = 0
	while (contadorPosiciones < posicionFila):
		filaAClasificar = lista[contadorPosiciones]
		clasificador = productoInterno(filaAClasificar,wNuevo)
		if clasificador < 0:
			wNuevo = calcularNuevoW(filaAClasificar)
			contadorPosiciones = -1
		contadorPosiciones += 1
			
cumuloDeClases = range(0,NUM_CLASES)
for i in range(0,NUM_CLASES):
	cumuloDeClases[i] = []

def recorrerMatriz(matriz):
	tamanio = len(matriz)
	for i in range(0, tamanio):
		
		clasificador = productoInterno(matriz[i],vectorw[int(matriz[i][0])])
		if (clasificador < 0):
			perceptron(i, matriz)

train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next() 
for label in archivo_csv:
	cumuloDeClases[int(label[0])].append(label)
train.close()		

for clase in range(0,NUM_CLASES):
	recorrerMatriz(cumuloDeClases[clase])
	
for i in range(0,NUM_CLASES):
	print vectorw[i]
	print (" ")
	
	test = open('test.csv')
test_csv = csv.reader(test, delimiter=",")
test_csv.next()
 
archivoPrediccion = open ("resultadoDeLaPrediccionDeNumeros.csv","w")
prediccion_csv = csv.writer(archivoPrediccion)
registros = []
registros.append(("ImageId","Label"))
contador = 0
for label in test_csv:
	contador += 1
	tuplaX = label
	mayor = -1
	for i in range(0,NUM_CLASES):
		producto = productoInterno([1]+label,vectorw[i])
		if (producto > mayor):
			mayor = producto
			clase = i
	tuplaNumero=(contador,clase)
	registros.append(tuplaNumero)				
prediccion_csv.writerows(registros)		
test.close()
archivoPrediccion.close()
