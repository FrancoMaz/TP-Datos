import csv
import random
import matplotlib.pyplot as plt
import math

NUM_PIXELES = 784
NUM_CLASES = 10
VALORMAXIMO = 255
VALORMINIMO = 0
FACTORAPRENDIZAJE = 0.1
NEURONASCAPAOCULTA1 = 100
NEURONASCAPAOCULTA2 = 100
CANTIDADCAPAS = 4
CRITERIODECORTE = 0.5

wPesoCapa1 = range(0,NEURONASCAPAOCULTA1)
wPesoCapa2 = range(0,NEURONASCAPAOCULTA2)
wPesoCapaFinal = range(0,NUM_CLASES)
setDeDatos = []
entradasCapaInicial = range(0,NUM_PIXELES)
salidasCapaOculta1 = range(0,NEURONASCAPAOCULTA1)
salidasCapaOculta2 = range(0,NEURONASCAPAOCULTA2)
salidasCapaFinal = range(0,NUM_CLASES)
salidasDeseadas = range(0,NUM_CLASES)
factoresDeCambio = []
ejemplosQueFallan = []


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
	
def backpropagation(salidasDeseadas,salidasCapaFinal,salidasCapaOculta1,salidasCapaOculta2,wPesoCapa1,wPesoCapa2,wPesoCapaFinal,entradasCapaInicial):
	for i in range(0,NUM_CLASES):
		factoresDeCambio[CANTIDADCAPAS-2][i] = float(factorDeCambioCapaFinal(salidasDeseadas[i],salidasCapaFinal[i]))
		for j in range(0,NEURONASCAPAOCULTA2):
			wPesoCapaFinal[i][j] = (descensoDelGradiente(wPesoCapaFinal[i][j],factoresDeCambio[CANTIDADCAPAS-2][i],salidasCapaOculta2[j]))
	recalcularPesos(salidasCapaOculta2,factoresDeCambio, wPesoCapa2,salidasCapaOculta1,NEURONASCAPAOCULTA2, NEURONASCAPAOCULTA1, CANTIDADCAPAS-3)
	recalcularPesos(salidasCapaOculta1,factoresDeCambio, wPesoCapa1,entradasCapaInicial,NEURONASCAPAOCULTA1, NUM_PIXELES, 0)
	
#Reajuste de pesos
def descensoDelGradiente(pesoAnterior,factorDeCambioAnterior,entradaAnterior):
	return(pesoAnterior + FACTORAPRENDIZAJE*factorDeCambioAnterior*entradaAnterior)
	
def recalcularPesos(salidasCapaActual,factorDeCambio, pesos, entradasCapaActual, cantidadNeuronasCapaActual, cantidadNeuronasCapaAnterior, capaActual):
	for i in range(0,cantidadNeuronasCapaActual):
		factoresDeCambio[capaActual][i] = factorDeCambioCapasOcultas(salidasCapaActual[i],factoresDeCambio[capaActual+1],pesos[i])
		for j in range(0,cantidadNeuronasCapaAnterior):
			pesos[i][j] = descensoDelGradiente(pesos[i][j],factoresDeCambio[capaActual][i],entradasCapaActual[j])

#Definicion del error para el criterio de corte
def error(salidaDeseada,salidaFinal):
	suma = 0
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
	return (salida*(1-salida))
	
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
#---------------------------------------------------------------
#Funcion de entrenamiento
def entrenamiento(fila):
	#calcularSalidasDeCapa(cantidadNeuronasCapaActual,salidasCapaActual,salidasCapaAnterior,pesosCapaActual)
	#se calcula la salida de la capa oculta 1
	calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(fila,len(fila)),wPesoCapa1)
	#se calcula la salida de la capa oculta 2
	calcularSalidasDeCapa(NEURONASCAPAOCULTA2,salidasCapaOculta2,salidasCapaOculta1+[-1],wPesoCapa2)
	#se calcula la salida de la capa final
	calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta2+[-1],wPesoCapaFinal)
	print i
	contadorDeControl = 0
	while (error(salidasDeseadas[int(fila[0])],salidasCapaFinal) > CRITERIODECORTE) and (contadorDeControl < 100):
			
		#while ((contadorPosiciones <= i) or (contadorDeControl <= 1000)):	
			#recalculamos todos los pesos de la red
		backpropagation(salidasDeseadas[int(fila[0])],salidasCapaFinal,salidasCapaOculta1,salidasCapaOculta2,wPesoCapa1,wPesoCapa2,wPesoCapaFinal,modificarVector(fila,len(setDeDatos[i])))
		calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(fila,len(fila)),wPesoCapa1)
		calcularSalidasDeCapa(NEURONASCAPAOCULTA2,salidasCapaOculta2,salidasCapaOculta1+[-1],wPesoCapa2)
		calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta2+[-1],wPesoCapaFinal)
		contadorDeControl +=1
			
				#calculamos otras vez las salidas de todas las capas
				
"""fila = setDeDatos[contadorPosiciones]
				calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(fila,len(fila)),wPesoCapa1)
				calcularSalidasDeCapa(NEURONASCAPAOCULTA2,salidasCapaOculta2,salidasCapaOculta1+[-1],wPesoCapa2)
				calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta2+[-1],wPesoCapaFinal)
				print error(salidasDeseadas,salidasCapaFinal)
				if (error(salidasDeseadas,salidasCapaFinal) > CRITERIODECORTE):
					contadorPosiciones =-1	
				for x in salidasDeseadas[:]:
					salidasDeseadas.remove(x)
				contadorPosiciones +=1
				contadorDeControl +=1
				for j in range(0,NUM_CLASES):
					salidasDeseadas.append(0)
				salidasDeseadas[int(fila[0])] = 1"""
			
			
	
#Inicializacion de pesos
inicializacionPesos(wPesoCapa1,NUM_PIXELES,NEURONASCAPAOCULTA1)
inicializacionPesos(wPesoCapa2,NEURONASCAPAOCULTA1,NEURONASCAPAOCULTA2)
inicializacionPesos(wPesoCapaFinal,NEURONASCAPAOCULTA2,NUM_CLASES)
inicializacionSalidasDeseadas(salidasDeseadas)

#Inicializacion de factores de cambio		
inicializacionFactorDeCambio(factoresDeCambio,NEURONASCAPAOCULTA1)
inicializacionFactorDeCambio(factoresDeCambio,NEURONASCAPAOCULTA2)
inicializacionFactorDeCambio(factoresDeCambio,NUM_CLASES)

#Empieza el entrenamiento :)
train = open('train.csv')
archivo_csv = csv.reader(train, delimiter=",")
archivo_csv.next()


#division de datos y de validacion---------------------------
matrizDeValidacion=[]
contador=0
for label in archivo_csv:
	if (contador <= 30000):
		setDeDatos.append(label)
	else:
		matrizDeValidacion.append(label)
	contador +=1	
train.close()

archivoValidacion = open ("archivoValidacion.csv","w")
archivoValidacion_csv = csv.writer(archivoValidacion)
registroValidacion = []
registroValidacion.append("Label")
for i in range(0,len(matrizDeValidacion)):
	registroValidacion.append(matrizDeValidacion[i])
archivoValidacion_csv.writerows(registroValidacion)		
archivoValidacion.close()
#fin de division-----------------------------

for i in range(0,len(setDeDatos)):
	entrenamiento(setDeDatos[i])

crearArchivoPesos("pesosCapa1.csv",wPesoCapa1)
crearArchivoPesos("pesosCapa2.csv",wPesoCapa2)
crearArchivoPesos("pesosCapaFinal.csv",wPesoCapaFinal)

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
	calcularSalidasDeCapa(NEURONASCAPAOCULTA2,salidasCapaOculta2,salidasCapaOculta1+[-1],wPesoCapa2)
	calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta2+[-1],wPesoCapaFinal)
	menorError = 100
	for i in range(0,NUM_CLASES):
		if (error(salidasDeseadas[i],salidasCapaFinal) < menorError):
			menorError = error(salidasDeseadas[i],salidasCapaFinal)
			clase = i
	if (i == int(label[0])):
		contadorAciertos += 1
	else:
		ejemplosQueFallan.append(tuplaX)
	tuplaNumero=(contador,clase)
	registros.append(tuplaNumero)
print ("Aciertos: " + str(contadorAciertos) + " de " + str(contador) + " datos totales")		
prediccion_csv.writerows(registros)		
validacion.close()
archivoPrediccion.close()

for i in range(0,len(ejemplosQueFallan)):
	entrenamiento(ejemplosQueFallan[i])

crearArchivoPesos("pesosCapa1.csv",wPesoCapa1)
crearArchivoPesos("pesosCapa2.csv",wPesoCapa2)
crearArchivoPesos("pesosCapaFinal.csv",wPesoCapaFinal)

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
	calcularSalidasDeCapa(NEURONASCAPAOCULTA2,salidasCapaOculta2,salidasCapaOculta1+[-1],wPesoCapa2)
	calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta2+[-1],wPesoCapaFinal)
	menorError = 100
	for i in range(0,NUM_CLASES):
		if (error(salidasDeseadas[i],salidasCapaFinal) < menorError):
			menorError = error(salidasDeseadas[i],salidasCapaFinal)
			clase = i
	tuplaNumero=(contador,clase)
	registros.append(tuplaNumero)
prediccion_csv.writerows(registros)		
test.close()
archivoPrediccion.close()
