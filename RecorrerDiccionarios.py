import csv
import matplotlib.pyplot as plt

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
		pixels = range(0,785)
		for col in range(0,785):
			fila = range(0,257)
			for i in range(0,256):
				fila[i] = 0
			pixels[col] = fila
		numeros[label[0]] = pixels	
	
	for numpixel in range(0,784):
		pixels = numeros[label[0]]
		indice = int(label[numpixel+1])
		pixels[numpixel][indice] += 1
		pixels[numpixel][256] += 1
		
	for i in range(0,10):
		listaPixels = numeros[str(i)]
		sumaProductoria = 0
		for j in range(0,785):
			productoria = 1
			for valor in range(0,256):
				valorPixel = listaPixels[j][valor]
				if valorPixel == 0: valorPixel = 1
				productoria = productoria * valorPixel
			productoria = productoria/listaPixels[j][valor]
			vectorNumeros[i][j] = productoria
			sumaProductoria += productoria
		probabilidadTotal += sumaProductoria * frecuenciaNumeros[str(i)]

train.close()

archivo = open ("resultadoClases.csv","w")
archivo_csv = csv.writer(archivo)
registros = []
registros.append(("Numeros","Cantidad"))
	
for clave in frecuenciaNumeros:
		tupla = (clave,frecuenciaNumeros[clave[0]])
		registros.append(tupla)
archivo_csv.writerows(registros)

archivo.close()
