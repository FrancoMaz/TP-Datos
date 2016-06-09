import csv
import random
import matplotlib.pyplot as plt
import math

NUM_PIXELES = 784
NUM_CLASES = 10
VALORMAXIMO = 255
VALORMINIMO = 0
FACTORAPRENDIZAJE = 0.5
NEURONASCAPAOCULTA = 100
UMBRAL = 0.5

wInicialEntrada = range(0,NUM_PIXELES + 1)
wInicialSalida = range(0,NEURONASCAPAOCULTA + 1)
vectorW1 = range(0,NEURONASCAPAOCULTA)
vectorW2 = range(0,NUM_CLASES)
matriz = []

for i in range(0,NEURONASCAPAOCULTA):
	wInicialEntrada[i] = []
	for j in range(0,NUM_PIXELES + 1):
		wInicialEntrada[i].append(random.random())

for i in range(0,NUM_CLASES):
	wInicialSalida[i] = []
	for j in range(0,NEURONASCAPAOCULTA):
		wInicialSalida[i].append(random.random())

for i in range(0,NUM_CLASES):
	vectorW1[i] = wInicialEntrada
	vectorW2[i] = wInicialSalida

def sigmoide(valor):
	return (float(1/(1+math.exp(-valor))))

def productoInterno(x,w):
	producto = 0
	for i in range(0,len(x)):
		producto += float(x[i])*w[i]
	return producto
	
def suma(x,w,error):
	vectorTemp = vectorConElUno(x)[:]
	vectorSuma = range(NUM_PIXELES+1)
	for i in range(0,NUM_PIXELES+1):
		vectorSuma[i] = int(vectorTemp[i])*error + int(w[i])
	return vectorSuma

def calcularNuevoW(vector,solucionIdeal,solucionPerceptron):
	errorCuadratico = (1/2)*(solucionIdeal - solucionPerceptron)**2
	wNuevo = suma(vector,vectorw[int(vector[0])],error)
	vectorw[int(vector[0])] = wNuevo
	return wNuevo

def vectorConElUno(vector):
	vectorADevolver = vector[:]
	vectorADevolver[0] = 1
	return vectorADevolver

def perceptron(posicionFila,matriz,numeroDeClase,solucionPerceptron,solucionIdeal):
	fila = matriz[posicionFila]
	wNuevo = calcularNuevoW(fila,solucionIdeal,solucionPerceptron)
	contadorPosiciones = 0
	contadorDeControl = 0
	while (contadorPosiciones < posicionFila)and(contadorDeControl<= 2000):
		filaAClasificar = matriz[contadorPosiciones]
		vectorTemp = vectorconElUno(filaAClasificar)
		clasificador = funcionDeActivacion(productoInterno(vectorTemp,wNuevo))
		if (int(filaAClasificar[0]) == numeroDeClase):
			if clasificador < UMBRAL:
				wNuevo = calcularNuevoW(filaAClasificar,1,clasificador)
				contadorPosiciones = -1				
		elif(clasificador >= UMBRAL):
				wNuevo = calcularNuevoW(filaAClasificar,0,clasificador)
				contadorPosiciones = -1
		contadorDeControl += 1
		contadorPosiciones += 1		
			
def escalamiento(valor):
	return (valor - VALORMINIMO)/(VALORMAXIMO - VALORMINIMO)
	
def salidaNeurona(entrada,pesos):
	return (sigmoide(productoInterno(entrada,pesos)))

def recorrerMatriz(matriz,numeroDeClase):
	tamanio = len(matriz)	
	for i in range(0, tamanio):
		capaDeEntrada = []
		capaDeSalida = []
		salidasReales = []
		salidasCapaOculta = []
		for i in range(0,NUM_CLASES):
			capaDeSalida.append(0)
		capaDeSalida[int(matriz[i][0])] = 1
		for pixel in range(1,NUM_PIXELES):
			capaDeEntrada.append(escalamiento(int(matriz[i][pixel])))
		for neurona in range(0,NEURONASCAPAOCULTA):
			salidasCapaOculta.append(salidaNeurona([1]+capaDeEntrada,vectorW1[int(matriz[i][0])][neurona]))
		for salidas in range(0,NUM_CLASES):
			salidasReales.append(salidaNeurona(salidasCapaOculta,vectorW2[int(matriz[i][0])][salidas]))
		print salidasReales
		"""clasificador = funcionDeActivacion(productoInterno([1]+capaDeEntrada,vectorw[int(matriz[i][0])]))
		if(int(matriz[i][0]) == numeroDeClase):
			capaDeSalida[numeroDeClase] = 1
			if (clasificador < UMBRAL):
				perceptron(i,matriz,numeroDeClase,clasificador,1)
		elif(clasificador >= UMBRAL):
			perceptron(i,matriz,numeroDeClase,clasificador,0) 	"""

train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next()

for label in archivo_csv:
	matriz.append(label)
train.close()		

for clase in range(0,NUM_CLASES):
	recorrerMatriz(matriz,clase)
	
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
