import csv
import random
import matplotlib.pyplot as plt
import math

NUM_PIXELES = 784
NUM_CLASES = 10
VALORMAXIMO = 255
VALORMINIMO = 0
FACTORAPRENDIZAJE = 0.5
NEURONASCAPAOCULTA1 = 100
NEURONASCAPAOCULTA2 = 100
CANTIDADCAPAS = 4
UMBRALINICIAL = 0.5
CRITERIODECORTE = 0.01

wPesoCapa1 = range(0,NEURONASCAPAOCULTA1)
wPesoCapa2 = range(0,NEURONASCAPAOCULTA2)
wPesoCapaFinal = range(0,NUM_CLASES)
setDeDatos = []
entradasCapaInicial = range(0,NUM_PIXELES)
salidasCapaOculta1 = range(0,NEURONASCAPAOCULTA1)
salidasCapaOculta2 = range(0,NEURONASCAPAOCULTA2)
salidasCapaFinal = range(0,NUM_CLASES)
salidasDeseadas = []
factoresDeCambio = []


#Inicializacion de vectores de pesos-------------------

def inicializacionPesos(listaPesos,entrada,salida):
	for i in range(0,salida):
		listaPesos[i] = []
		for j in range(0,entrada):
			listaPesos[i].append(random.random())
		listaPesos[i].append(UMBRALINICIAL)
	
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
	
def backpropagation(salidasDeseadas,salidasCapaFinal,salidasCapaOculta1,salidasCapaOculta2,wPesoCapa1,wPesoCapa2,wPesoCapaFinal,entradasCapaInicial):
	for i in range(0,NUM_CLASES):
		factoresDeCambio[CANTIDADCAPAS-1][i] = factorDeCambioCapaFinal(salidasDeseadas[i],salidasCapaFinal[i])
		for j in range(0,NEURONASCAPAOCULTA2):
			wPesoCapaFinal[i][j] = descensoDelGradiente(wPesoCapaFinal[i][j],factoresDeCambio[CANTIDADCAPAS-1][i],salidasCapaOculta2[j])
	recalcularPesos(salidasCapaOculta2,factoresDeCambio, wPesoCapa2,salidasCapaOculta1,NEURONASCAPAOCULTA2, NEURONASCAPAOCULTA1, CANTIDADCAPAS-2)
	recalcularPesos(salidasCapaOculta1,factoresDeCambio, wPesoCapa1,entradasCapaInicial,NEURONASCAPAOCULTA1, NUM_PIXELES, 0)
	
#Reajuste de pesos
def descensoDelGradiente(pesoAnterior,factorDeCambioAnterior,entradaAnterior):
	return(pesoAnterior + FACTORAPRENDIZAJE*factorDeCambioAnterior*entradaAnterior)
	
def recalcularPesos(salidasCapaActual,factorDeCambio, pesos, entradasCapaActual, cantidadNeuronasCapaActual, cantidadNeuronasCapaAnterior, capaActual):
	for i in range(0,cantidadNeuronasCapaActual):
		factoresDeCambio[capaActual][i] = factorDeCambioCapasOcultas(salidas,factoresDeCambio[capaActual+1]+[0],pesos[i])
		for j in range(0,cantidadNeuronasCapaAnterior):
			pesos[i][j] = descensoDelGradiente(pesos[i][j],factoresDeCambio[capaActual][i],entradasCapaActual[j])

#Definicion del error para el criterio de corte
def error(salidaDeseada,salidaFinal):
	suma = 0
	for i in range(0,NUM_CLASES):
		suma += (salidaDeseada[i] - salidaFinal[i])**2
	return math.sqrt(suma)
	
#Funciones auxiliares---------------------------------------------
def sigmoide(valor):
	return (float(1/(1+math.exp(-valor))))

def productoInterno(x,w):
	producto = 0
	for i in range(0,len(x)):
		producto += float(x[i])*w[i]
	return producto
	
def escalamiento(valor):
	return (valor - VALORMINIMO)/(VALORMAXIMO - VALORMINIMO)
	
def funcionDeActivacion(entrada,pesos):
	return (sigmoide(productoInterno(entrada,pesos)))
	
def derivadaSalida(salida):
	return (salida*(1-salida))
	
def calcularSalidasDeCapa(cantidadNeuronas,salidas,entradas,pesos):
	for i in range(0,cantidadNeuronas):
		print len(entradas)
		print len(pesos[i])
		salidas[i] = float(funcionDeActivacion(entradas,pesos[i]))
		
def modificarVector(vector,inicioVector,tamanio):	
	vectorADevolver = vector[:]
	for i in range(inicioVector,tamanio+1):
		vectorADevolver[i-1] = (escalamiento(int(vector[i])))
	return (vectorADevolver + [1])
#---------------------------------------------------------------
#Funcion de entrenamiento
def entrenamiento(setDeDatos):
	for i in range(0,len(setDeDatos)):
		fila = setDeDatos[i]
		for j in range(0,NUM_CLASES):
			salidasDeseadas.append(0)
		salidasDeseadas[int(setDeDatos[i][0])] = 1
		#calcularSalidasDeCapa(cantidadNeuronasCapaActual,salidasCapaActual,salidasCapaAnterior,pesosCapaActual)
		#se calcula la salida de la capa oculta 1
		calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(fila,1,NUM_PIXELES),wPesoCapa1)
		#se calcula la salida de la capa oculta 2
		calcularSalidasDeCapa(NEURONASCAPAOCULTA2,salidasCapaOculta2,salidasCapaOculta1+[1],wPesoCapa2)
		#se calcula la salida de la capa final
		calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta2+[1],wPesoCapaFinal)
		contadorPosiciones = 0
		if (error(salidasDeseadas,salidasCapaFinal) > CRITERIODECORTE):	
			while (contadorPosiciones <= i):		
				#recalculamos todos los pesos de la red
				backpropagation(salidasDeseadas,salidasCapaFinal,salidasCapaOculta1,salidasCapaOculta2,wPesoCapa1,wPesoCapa2,wPesoCapaFinal,entradasCapaInicial)
				#calculamos otras vez las salidas de todas las capas
				fila = setDeDatos[contadorDePosiciones]
				for j in range(0,NUM_CLASES):
					salidasDeseadas.append(0)
				salidasDeseadas[int(setDeDatos[i][0])] = 1
				calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(fila,1,NUM_PIXELES),wPesoCapa1)
				calcularSalidasDeCapa(NEURONASCAPAOCULTA2,salidasCapaOculta2,salidasCapaOculta1+[1],wPesoCapa2)
				calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta2+[1],wPesoCapaFinal)
				if (error(salidasDeseadas,salidasCapaFinal) > CRITERIODECORTE):
					contadorPosiciones =-1	
				contadorPosiciones +=1
				salidasDeseadas.clear()
				entradasCapaInicial.clear()	
			
	
#Inicializacion de pesos
inicializacionPesos(wPesoCapa1,NUM_PIXELES,NEURONASCAPAOCULTA1)
inicializacionPesos(wPesoCapa2,NEURONASCAPAOCULTA1,NEURONASCAPAOCULTA2)
inicializacionPesos(wPesoCapaFinal,NEURONASCAPAOCULTA2,NUM_CLASES)

#Inicializacion de factores de cambio		
inicializacionFactorDeCambio(factoresDeCambio,NEURONASCAPAOCULTA1)
inicializacionFactorDeCambio(factoresDeCambio,NEURONASCAPAOCULTA2)
inicializacionFactorDeCambio(factoresDeCambio,NUM_CLASES)

#Empieza el entrenamiento :)
train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next()

for label in archivo_csv:
	setDeDatos.append(label)
train.close()		

#for clase in range(0,NUM_CLASES):
entrenamiento(setDeDatos)
		
