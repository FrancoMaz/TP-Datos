import csv
import random
import matplotlib.pyplot as plt
import math
import numpy as np

NUM_CLASES = 10
NEURONASCAPAOCULTA1 = 30
NEURONASCAPAOCULTA2 = 100
NUM_PIXELES = 784
VALORMAXIMO = 255
VALORMINIMO = 0

wPesoCapa1 = range(0,NEURONASCAPAOCULTA1)
wPesoCapa2 = range(0,NEURONASCAPAOCULTA2)
wPesoCapaFinal = range(0,NUM_CLASES)
ejemplosQueFallan = []
salidasDeseadas = range(0,NUM_CLASES)
salidasCapaOculta1 = range(0,NEURONASCAPAOCULTA1)
salidasCapaOculta2 = range(0,NEURONASCAPAOCULTA2)
salidasCapaFinal = range(0,NUM_CLASES)

def modificarVector(vector,tamanio):	
	vectorADevolver = range(0,tamanio)
	for i in range(0,tamanio):
		vectorADevolver[i] = escalamiento(int(vector[i]))
	return (vectorADevolver + [-1])

def calcularSalidasDeCapa(cantidadNeuronas,salidas,entradas,pesos):
	for i in range(0,cantidadNeuronas):
		print pesos[i]
		salidas[i] = float(funcionDeActivacion(entradas,pesos[i]))
		
def funcionDeActivacion(entrada,pesos):
	return (sigmoide(productoInterno(entrada,pesos)))
	
def sigmoide(valor):
	return float(1/(1+math.exp(-valor)))
	
def productoInterno(x,w):
	producto = 0
	for i in range(0,len(x)):
		producto += float(x[i])*w[i]
	return producto

def error(salidaDeseada,salidaFinal):
	suma = 0
	for i in range(0,NUM_CLASES):
		suma += (salidaDeseada[i] - salidaFinal[i])**2
	return float(math.sqrt(suma))
	
def escalamiento(valor):
	return (float(valor - VALORMINIMO)/(VALORMAXIMO - VALORMINIMO))


pesosCapa1 = open('pesosCapaOcultaConUnaCapaOculta.csv')
pesosCapa1_csv = csv.reader(pesosCapa1,delimiter=',')
pesosCapa1.next()

for i in range(0,NEURONASCAPAOCULTA1):
	wPesoCapa1[i] = []
	for j in range(0,NUM_PIXELES+1):
		wPesoCapa1[i].append(0)
contador=0
for label in pesosCapa1:
	keywords = label.splitlines()
	keyword=label.split(",")
	for j in range (0,NUM_PIXELES+1):
		wPesoCapa1[contador][j]=float(keyword[j])
	contador +=1
pesosCapa1.close()

for i in range(0,NUM_CLASES):
	wPesoCapaFinal[i] = []
	for j in range(0,NEURONASCAPAOCULTA1+1):
		wPesoCapaFinal[i].append(0)
pesosCapaFinal = open('pesosCapaFinalConUnaCapaOculta.csv')
pesosCapaFinal_csv = csv.reader(pesosCapaFinal, delimiter=",")
pesosCapaFinal_csv.next()
contador=0
for label in pesosCapaFinal:
	keywords = label.splitlines()
	keyword=label.split(",")
	for j in range(0,NEURONASCAPAOCULTA1+1):
		wPesoCapaFinal[contador][j]=float(keyword[j])
	contador +=1
pesosCapaFinal.close()

for i in range(0,len(salidasDeseadas)):
	salidasDeseadas[i] = range(0,NUM_CLASES)
	for j in range(0,len(salidasDeseadas[i])):
		salidasDeseadas[i][j] = 0
		if (i == j):
			salidasDeseadas[i][j] = 1

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
	tuplaX = label
	calcularSalidasDeCapa(NEURONASCAPAOCULTA1,salidasCapaOculta1,modificarVector(tuplaX,len(tuplaX)),wPesoCapa1)
	calcularSalidasDeCapa(NUM_CLASES,salidasCapaFinal,salidasCapaOculta1+[-1],wPesoCapaFinal)
	clase = np.argmax(salidasCapaFinal)
	tuplaNumero=(contador,clase)
	registros.append(tuplaNumero)
prediccion_csv.writerows(registros)		
test.close()
archivoPrediccion.close()
