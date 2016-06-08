import csv
import random
import matplotlib.pyplot as plt
import math

NUM_PIXELES = 784
NUM_CLASES = 10
UMBRAL = 0.5
VALORMAXIMO = 50979600
FACTORAPRENDIZAJE = 0.5

wInicial = range(0,NUM_PIXELES + 1)
vectorw = range(0,NUM_CLASES)
contador = 0

for i in range(0,NUM_PIXELES + 1):
	wInicial[i] = random.random()

for i in range(0,NUM_CLASES):
	vectorw[i] = wInicial
def funcionDeActivacion(valor):
	return valor/VALORMAXIMO

def productoInterno(x,w):
	vectorTemp = x[:]
	vectorTemp[0] = 1
	producto = 0
	for i in range(0,NUM_PIXELES + 1):
		producto += float(vectorTemp[i])*w[i]
	return producto
	
def suma(x,w,error):
	vectorTemp = x[:]
	vectorTemp[0] = 1
	vectorSuma = range(NUM_PIXELES+1)
	for i in range(0,NUM_PIXELES+1):
		vectorSuma[i] = int(vectorTemp[i])*error + int(w[i])
	return vectorSuma

def calcularNuevoW(vector,solucionIdeal):
	error = abs(solucionIdeal-funcionDeActivacion(productoInterno(vector,vectorw[int(vector[0])])))
	print error
	wNuevo = suma(vector,vectorw[int(vector[0])],error)
	vectorw[int(vector[0])] = wNuevo
	return wNuevo

def perceptron(posicionFila,matriz,numeroDeClase,solucionIdeal):
	fila = matriz[posicionFila]
	wNuevo = calcularNuevoW(fila,solucionIdeal)
	contadorPosiciones = 0
	contadorDeControl = 0
	while (contadorPosiciones < posicionFila)and(contadorDeControl<= 2000):
		filaAClasificar = matriz[contadorPosiciones]
		#print "posicionDeFila: "+ str(posicionFila)
		#print "claseAClasificar: "+filaAClasificar[0]
		#print "NumeroDeClase: " + str(numeroDeClase)
		#print" "
		clasificador = funcionDeActivacion(productoInterno(filaAClasificar,wNuevo))
		if (int(filaAClasificar[0]) == numeroDeClase):
			if clasificador < UMBRAL:
				wNuevo = calcularNuevoW(filaAClasificar,1)
				contadorPosiciones = -1
			#else: print clasificador					
		elif(clasificador >= UMBRAL):
				wNuevo = calcularNuevoW(filaAClasificar,0)
				contadorPosiciones = -1
				#print"entro"
		contadorDeControl += 1
		contadorPosiciones += 1		
			
#cumuloDeClases = range(0,NUM_CLASES)
cumuloDeClases= []
#for i in range(0,NUM_CLASES):
	#cumuloDeClases[i] = []

def recorrerMatriz(matriz,numeroDeClase):
	tamanio = len(matriz)
	for i in range(0, tamanio):
		#print matriz[i][0]
		clasificador = funcionDeActivacion(productoInterno(matriz[i],vectorw[int(matriz[i][0])]))
		if(int(matriz[i][0]) == numeroDeClase):
			if (clasificador < UMBRAL):
				perceptron(i, matriz,numeroDeClase,1)
		elif(clasificador >= UMBRAL):
			   perceptron(i,matriz,numeroDeClase,0) 	

train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next()

for label in archivo_csv:
	cumuloDeClases.append(label)
train.close()		

for clase in range(0,NUM_CLASES):
	recorrerMatriz(cumuloDeClases,clase)
	
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
