import csv
import matplotlib.pyplot as plt
NUM_PIXELES = 784
NUM_CLASES = 10

wInicial = range(0,NUM_PIXELES + 1)
vectorw = range(0,NUM_CLASES + 1)
vectorPosiciones = range(0,NUM_CLASES + 1)
contador = 0

for i in range(0,NUM_PIXELES + 1):
	wInicial[i] = -1

for i in range(0,NUM_CLASES + 1):
	vectorw[i] = wInicial
	vectorPosiciones[i] = []

def productoInterno(x,w):
	x[0] = 1
	producto = 0
	for i in range(0,NUM_PIXELES + 1):
		producto += int(x[i])*w[i]
	return producto
	
def suma(x,w):
	vectorSuma = range(NUM_PIXELES + 1)
	for i in range(0,NUM_PIXELES + 1):
		vectorSuma[i] = int(x[i]) + int(w[i])
	return vectorSuma

def calcularNuevoW(vector):
	vector[0] = 1
	wNuevo = suma(vectorw[vector[0]], vector)

def perceptron(vector):
	resultado = productoInterno(vector, vectorw[int(vector[0])])
	vectorPosiciones[vector[0]].append(contador)
	if resultado < 0:
		calcularNuevoW(vector)
		for i in range(0,len(vectorPosiciones[vector[0]]) + 1):
			perceptron()
			
		

train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next() 

for label in archivo_csv:
	perceptron(label)
		
train.close()	
"""
#Se calcula el P(X) que es constante para todo
for i in range(0,10):
	listaPixels = numeros[str(i)]
	sumaProductoria = 0
	for j in range(0,784):
		productoria = 1
		for valor in range(0,256):
			valorPixel = listaPixels[j][valor]
			
			if valorPixel <>0:
				probablidadDelPixel = float(valorPixel)/float(frecuenciaNumeros[str(i)])
				productoria = float(productoria * probablidadDelPixel)
				listaPixels[j][valor] = probablidadDelPixel
		
		vectorNumeros[i][j] = float(productoria)
		sumaProductoria += float(productoria)
	probabilidadTotal += float(sumaProductoria * frecuenciaNumeros[str(i)]/42000)

#Empecemos a predecir que esto se va a descontrolar
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
	probabilidadBayesinaMayor = -1
	for i in range(0,10):
		listaPixels = numeros[str(i)]
		sumaDeProbabilidadDeLosPixels = 0
		for j in range(0,784):
			if int(tuplaX[j]) <> 0:
				sumaDeProbabilidadDeLosPixels += float(listaPixels[j][int(tuplaX[j])])
		probabilidadBayesiana = float((sumaDeProbabilidadDeLosPixels*frecuenciaNumeros[str(i)]/42000)/probabilidadTotal)
		if(probabilidadBayesiana > probabilidadBayesinaMayor):
			claseNumero = i;
			probabilidadBayesinaMayor = probabilidadBayesiana
	tuplaNumero=(contador,claseNumero)
	registros.append(tuplaNumero)				
prediccion_csv.writerows(registros)		
test.close()
archivoPrediccion.close()"""
