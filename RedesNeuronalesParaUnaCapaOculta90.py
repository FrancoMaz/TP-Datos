import csv
import random
import matplotlib.pyplot as plt
import math
import numpy as np

NUM_PIXELES = 784
NUM_CLASES = 10
VALORMAXIMO = 255
VALORMINIMO = 0
FACTORAPRENDIZAJE = 0.4
NEURONASCAPAOCULTA1 = 100
CANTIDADCAPAS = 3
CRITERIODECORTE = 0.5
MAXFILA = 42000
ERRORDEEPOCA = 20
ERRORMINIMO = 20
CANTIDADEPOCAS = 7
TAMANIOMINIBATCH = 100
CANTIDADITERACIONES = 100

wPesoCapa1 = range(0,NEURONASCAPAOCULTA1)
wPesoCapaFinal = range(0,NUM_CLASES)
setDeDatos = []
entradasCapaInicial = range(0,NUM_PIXELES)
salidasCapaOculta1 = range(0,NEURONASCAPAOCULTA1)
salidasCapaFinal = range(0,NUM_CLASES)
salidasDeseadas = range(0,NUM_CLASES)
factoresDeCambio = []
ejemplosQueFallan = []
salidasCalculadasActuales = range(0,MAXFILA)
salidasCalculadasAnteriores = range(0,MAXFILA)

#Inicializacion de vectores de pesos-------------------

def inicializacionPesos(listaPesos,entrada,salida):
	for i in range(0,salida):
		listaPesos[i] = []
		for j in range(0,entrada+1):
			listaPesos[i].append(random.uniform(-1.0,1.0))

def inicializacionSalidasDeseadas(salidasDeseadas):
	for i in range(0,len(salidasDeseadas)):
		salidasDeseadas[i] = range(0,NUM_CLASES)
		for j in range(0,len(salidasDeseadas[i])):
			salidasDeseadas[i][j] = 0
			if (i == j):
				salidasDeseadas[i][j] = 1
	
#Inicializacion de vector de factores de cambio------------
def inicializacionFactorDeCambio(factoresDeCambio,cantidadNeuronas):
	factoresDeCambio.append(range(0,cantidadNeuronas))
#-----------------------------------------------------
#Funciones para el entrenamiento

#Backpropagation
def factorDeCambioCapaFinal(salidaDeseada,salidaFinal):
	return (salidaDeseada - salidaFinal)*derivadaSalida(salidaFinal)
	
def factorDeCambioCapasOcultas(salidaCapaActual,factorDeCambioSiguiente,peso):
	return(derivadaSalida(salidaCapaActual)*productoInterno(factorDeCambioSiguiente,peso))
	
def backpropagation(salidasDeseadas,salidasCapaFinal,salidasCapaOculta1,wPesoCapa1,wPesoCapaFinal,entradasCapaInicial):
	for i in range(0,NUM_CLASES):
		factoresDeCambio[CANTIDADCAPAS-2][i] = float(factorDeCambioCapaFinal(salidasDeseadas[i],salidasCapaFinal[i]))
		for j in range(0,NEURONASCAPAOCULTA1):
			wPesoCapaFinal[i][j] = (descensoDelGradiente(wPesoCapaFinal[i][j],factoresDeCambio[CANTIDADCAPAS-2][i],salidasCapaOculta1[j]))
	recalcularPesos(salidasCapaOculta1,factoresDeCambio, wPesoCapa1,entradasCapaInicial,NEURONASCAPAOCULTA1, NUM_PIXELES, 0)
	
#Reajuste de pesos
def descensoDelGradiente(pesoAnterior,factorDeCambioAnterior,entradaAnterior):
	return(pesoAnterior - FACTORAPRENDIZAJE*factorDeCambioAnterior*entradaAnterior)
	
def recalcularPesos(salidasCapaActual,factorDeCambio, pesos, entradasCapaActual, cantidadNeuronasCapaActual, cantidadNeuronasCapaAnterior, capaActual):
	for i in range(0,cantidadNeuronasCapaActual):
		factoresDeCambio[capaActual][i] = factorDeCambioCapasOcultas(salidasCapaActual[i],factoresDeCambio[capaActual+1],pesos[i])
		for j in range(0,cantidadNeuronasCapaAnterior):
			pesos[i][j] = descensoDelGradiente(pesos[i][j],factoresDeCambio[capaActual][i],entradasCapaActual[j])

#Definicion del error para el criterio de corte
def error(salidaDeseada,salidaFinal):
	suma = float(0)
	for i in range(0,NUM_CLASES):
		suma += (salidaDeseada[i] - salidaFinal[i])**2
	return float(math.sqrt(suma))
	
#Funciones auxiliares---------------------------------------------
def sigmoide(valor):
	return float(1/(1+math.exp(-valor)))

def productoInterno(x,w):
	producto = 0
	for i in range(0,len(x)):
		producto += float(x[i])*w[i]
	return producto
	
def escalamiento(valor):
	return (float(valor - VALORMINIMO)/(VALORMAXIMO - VALORMINIMO))
	
def funcionDeActivacion(entrada,pesos):
	return (sigmoide(productoInterno(entrada,pesos)))
	
def derivadaSalida(salida):
	return (-(salida*(1-salida)))
	
def calcularSalidasDeCapa(cantidadNeuronas,salidas,entradas,pesos):
	for i in range(0,cantidadNeuronas):
		salidas[i] = float(funcionDeActivacion(entradas,pesos[i]))

def modificarVector(vector,tamanio):	
	vectorADevolver = range(0,tamanio-1)
	for i in range(1,tamanio):
		vectorADevolver[i-1] = escalamiento(int(vector[i]))
	return (vectorADevolver + [-1])
	
def crearArchivoPesos(nombre,vectorPesos):
	archivoPesos = open(nombre,"w")
	pesos_csv = csv.writer(archivoPesos)
	registros = []
	registros.append("Label")
	for i in range(0,len(vectorPesos)):
		tupla = vectorPesos[i]
		registros.append(tupla)
	pesos_csv.writerows(registros)
	archivoPesos.close()

def calcularEfectividad(correctos, total):
	return float((correctos * 100)/total)
	
def redondeo(valor):
	if (valor >= 0.5):
		valorADevolver = 1
	else:
		valorADevolver = 0
	return valorADevolver

def cumpleConCondicionDeCorte(salidasDeseadas,salidasFinales):
	cumple = True
	for i in range(0, len(salidasFinales)):
		if (redondeo(salidasFinales[i]) != salidasDeseadas[i]):
			cumple = False
	return cumple
			
#---------------------------------------------------------------
#Funcion de entrenamiento
def entrenamiento(setDeDatos):
	contadorEpocas = 0
	for i in range(0,CANTIDADEPOCAS):
		#minibatches = []
		contadorEpocas += 1
		print "Epoca " + str(contadorEpocas)
		"""random.shuffle(setDeDatos)
		contadorMinibatches = 0
		for j in range(0,len(minibatches)):
			minibatches.append([])
			for k in range(0,TAMANIOMINIBATCH):
				minibatches[j].append(setDeDatos[contadorMinibatches])
				contadorMinibatches += 1
		for minibatch in minibatches:
			contadorMinibatch = 0
			print "Minibatch "+str(contadorMinibatch)
			contadorMinibatch += 1"""
		contadorCorrectos = 0
		for fila in range(0,len(setDeDatos)):
			filaActual = setDeDatos[fila]
			print fila
			#calcularSalidasDeCapa(cantidadNeuronasCapaActual,salidasCapaActual,salidasCapaAnterior,pesosCapaActual)
			#se calcula la salida de la capa oculta 1
			calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(filaActual,len(filaActual)),wPesoCapa1)
			#se calcula la salida de la capa final
			calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta1+[-1],wPesoCapaFinal)
			contadorDeControl = 0
			errorCometido =  error(salidasDeseadas[int(filaActual[0])],salidasCapaFinal)
			while (errorCometido > CRITERIODECORTE) and (contadorDeControl <= CANTIDADITERACIONES):
				backpropagation(salidasDeseadas[int(filaActual[0])],salidasCapaFinal,salidasCapaOculta1,wPesoCapa1,wPesoCapaFinal,modificarVector(filaActual,len(filaActual)))
				calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(filaActual,len(filaActual)),wPesoCapa1)
				calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta1+[-1],wPesoCapaFinal)
				errorCometido = error(salidasDeseadas[int(filaActual[0])],salidasCapaFinal)
				contadorDeControl +=1
			if (np.argmax(salidasCapaFinal) == int(filaActual[0])):
				contadorCorrectos += 1
		print "Efectividad de la epoca " + str(contadorEpocas) + ": " + str(calcularEfectividad(contadorCorrectos,len(setDeDatos))) + "%"
				#salidasCalculadasActuales[i]= errorCometido	

def copiarSalidasActuales():
	for i in range(0,MAXFILA):
		salidasCalculadasAnteriores[i] = salidasCalculadasActuales[i]

"""def calcularPrecisionDelEntrenamiento():
	contadorBuenos = 0
	for i in range(0,MAXFILA):
		diferencia = float(salidasCalculadasAnteriores[i]-salidasCalculadasActuales[i])
		#print "diferencia :"+ str(diferencia)				
		if int(diferencia) <= 0:
		   if ((diferencia*100)/salidasCalculadasActuales[i]) < ERRORMINIMO:
			   contadorBuenos += 1
		else:
		 if ((diferencia*100)/salidasCalculadasAnteriores[i]) < ERRORMINIMO:
			   contadorBuenos += 1
	return float(contadorBuenos * 100/MAXFILA)"""
    	
#Inicializacion de pesos
inicializacionPesos(wPesoCapa1,NUM_PIXELES,NEURONASCAPAOCULTA1)
inicializacionPesos(wPesoCapaFinal,NEURONASCAPAOCULTA1,NUM_CLASES)
inicializacionSalidasDeseadas(salidasDeseadas)

#Inicializacion de factores de cambio		
inicializacionFactorDeCambio(factoresDeCambio,NEURONASCAPAOCULTA1)
inicializacionFactorDeCambio(factoresDeCambio,NUM_CLASES)

#Empieza el entrenamiento :)
train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next()


#division de datos y de validacion---------------------------
for label in archivo_csv:
	setDeDatos.append(label)
train.close()

"""print "Empezo la division de datos-------------------------------"
matrizDeValidacion=[]
contador=0
print "Empezo la division de datos-------------------------------"
for label in archivo_csv:
	#if contador >= 2000:
		#break 	
	if (contador < MAXFILA):
		setDeDatos.append(label)
	else:
		matrizDeValidacion.append(label)
	contador +=1	
train.close()
print "Termino la division de datos------------------------------" 

archivoValidacion = open ("archivoValidacion.csv","w")
archivoValidacion_csv = csv.writer(archivoValidacion)
registroValidacion = []
registroValidacion.append("Label")
for i in range(0,len(matrizDeValidacion)):
	registroValidacion.append(matrizDeValidacion[i])
archivoValidacion_csv.writerows(registroValidacion)		
archivoValidacion.close()
#fin de division-----------------------------"""


print "Empezo el entrenamiento-----------------------------------------------------"

entrenamiento(setDeDatos)
"""if(epocaActual > 1):	
	precisionActual = calcularPrecisionDelEntrenamiento()
	print "Epoca:"+str(epocaActual)+" ---presicion: " + str(precisionActual)+"%"		
	epocaActual += 1
	copiarSalidasActuales()"""
print "Termino el entrenamiento------------------------------------------------------"

"""print "Empezo la prediccion de la validacion-----------------------------------------"
validacion = open('archivoValidacion.csv')
validacion_csv = csv.reader(validacion, delimiter=",")
validacion_csv.next()

archivoPrediccion = open ("prediccionValidacion.csv","w")
prediccion_csv = csv.writer(archivoPrediccion)
registros = []
registros.append(("ImageId","Label"))
contador = 0
contadorAciertos = 0
for label in validacion_csv:
	contador += 1
	print contador
	tuplaX = label
	calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(tuplaX,len(tuplaX)),wPesoCapa1)
	calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta1+[-1],wPesoCapaFinal)
	clase = np.argmax(salidasCapaFinal)
	if (clase == int(label[0])):
		contadorAciertos += 1
	else:
		ejemplosQueFallan.append(tuplaX)
	tuplaNumero=(contador,clase)
	registros.append(tuplaNumero)
print ("Aciertos: " + str(contadorAciertos) + " de " + str(contador) + " datos totales")		
prediccion_csv.writerows(registros)		
validacion.close()
archivoPrediccion.close()
print "Termino la prediccion de la validacion-------------------------------------------" 

print "Ejemplos que fallan-------------------------------------------------------------"
#for i in range(0,len(ejemplosQueFallan)):
entrenamiento(ejemplosQueFallan)
print "Termino ejemplos que fallan-----------------------------------------------------""" 

crearArchivoPesos("pesosCapaOcultaConUnaCapaOculta.csv",wPesoCapa1)
crearArchivoPesos("pesosCapaFinalConUnaCapaOculta.csv",wPesoCapaFinal)

print "Empezo la verdadera prediccion apartir del TEST---------------------------------"
#Test a predecir-------------------------------------------------------------------------------------------------
test = open('test.csv')
test_csv = csv.reader(test, delimiter=",")
test.next()

archivoPrediccion = open ("prediccionTest.csv","w")
prediccion_csv = csv.writer(archivoPrediccion)
registros = []
registros.append(("ImageId","Label"))
contador = 0
for label in test_csv:
	contador += 1
	print contador
	tuplaX = label
	calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(tuplaX,len(tuplaX)),wPesoCapa1)
	calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta1+[-1],wPesoCapaFinal)
	clase = np.argmax(salidasCapaFinal)
	tuplaNumero=(contador,clase)
	registros.append(tuplaNumero)
prediccion_csv.writerows(registros)		
test.close()
archivoPrediccion.close()

print"Termino todo bien por suerte------------------------------------------------------"
