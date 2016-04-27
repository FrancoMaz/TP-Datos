import csv
import matplotlib.pyplot as plt


train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next()

pixelsCeros = range(0,784)

for i in range(0,784):
	pixelsCeros[i] = [i, 0]

for label in archivo_csv:
	for i in range (1,785):
		if label[i] == '0':
			pixelsCeros[i-1][1] += 1
			
train.close()

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
	columnasEliminadas = 0
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
		if pixelsCeros[numpixel][1] <= 41900:	
			columnasEliminadas += 1	
			pixels = numeros[label[0]]
			indice = int(label[numpixel+1])
			#if indice <> 0:
			pixels[numpixel][indice] += 1
			pixels[numpixel][256] += 1	
	print (784 - columnasEliminadas)
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
archivoPrediccion.close()
