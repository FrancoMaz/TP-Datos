import csv
import matplotlib.pyplot as plt
from decimal import *

train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next() 

frecuenciaNumeros = {}
numeros = {}
vectorNumeros = range(0,10)
probabilidadTotal = 0

for i in range(0,10):
	vectorPixels = range(0,785)
	vectorNumeros[i] = vectorPixels

for label in archivo_csv:
	if label[0] not in frecuenciaNumeros:
			frecuenciaNumeros[label[0]] = 0
	frecuenciaNumeros[label[0]] += 1
	if label[0] not in numeros:
		pixels = range(0,784)
		for col in range(0,784):
			fila = range(0,257)
			for i in range(0,257):
				fila[i] = 0	
			pixels[col] = fila
		numeros[label[0]] = pixels	
	
	for numpixel in range(0,784):
		pixels = numeros[label[0]]
		indice = int(label[numpixel+1])
		if indice <> 0:
			pixels[numpixel][indice] += 1
			pixels[numpixel][256] += 1
		
train.close()	

#Se calcula el P(X) que es constante para todo
for i in range(0,10):
	listaPixels = numeros[str(i)]
	sumaProductoria = 0
	for j in range(0,784):
		productoria = 1
		for valor in range(0,256):
			valorPixel = listaPixels[j][valor]
			
			if valorPixel <>0: 
				probablidadDelPixel = float(valorPixel)/float(listaPixels[j][256])
				productoria = float(productoria * probablidadDelPixel)
		
		vectorNumeros[i][j] = float(productoria)
		sumaProductoria += float(productoria)
	probabilidadTotal += float(sumaProductoria * frecuenciaNumeros[str(i)]/42000)
	
#lo uso para dejar a cada valor posible entre 0 a 255 para cada pixel de cada clase de numero su probabilidad

for i in range(0,10):
	listaPixels = numeros[str(i)]
	for j in range(0,784):
		for valor in range(0,256):
			valorPixel = listaPixels[j][valor]
			if valorPixel == 0: valorPixel = 1
			listaPixels[j][valor]= float(valorPixel)/float(listaPixels[j][256])
			

#Empecemos a predecir que esto se va a descontrolar
test = open('test.csv')
test_csv = csv.reader(test, delimiter=",")
test_csv.next()
 
archivoPrediccion = open ("resultadoDeLaPrediccionDeNumeros.csv","w")
prediccion_csv = csv.writer(archivoPrediccion)
registros = []
registros.append(("NumerosPredecido","Probabilidad"))

for label in test_csv:
	tuplaX = label
	probabilidadBayesinaMayor = -1
	for i in range(0,10):
		listaPixels = numeros[str(i)]
		sumaDeProbabilidadDeLosPixels = 0
		for j in range(0,784):
			sumaDeProbabilidadDeLosPixels += float(listaPixels[j][int(tuplaX[j])])
		probabilidadBayesiana = float((sumaDeProbabilidadDeLosPixels*frecuenciaNumeros[str(i)]/42000)/probabilidadTotal)
		if(probabilidadBayesiana > probabilidadBayesinaMayor):
			claseNumero = i;
			probabilidadBayesinaMayor = probabilidadBayesiana
			print probabilidadBayesinaMayor
			print claseNumero
	tuplaNumero=(claseNumero,probabilidadBayesinaMayor)
	registros.append(tuplaNumero)				
prediccion_csv.writerows(registros)		
test.close()
archivoPrediccion.close()



archivo = open ("resultadoClases.csv","w")
archivo_csv = csv.writer(archivo)
registros = []
registros.append(("Numeros","Cantidad"))
	
for clave in frecuenciaNumeros:
		tupla = (clave,frecuenciaNumeros[clave[0]])
		registros.append(tupla)
archivo_csv.writerows(registros)

archivo.close()
