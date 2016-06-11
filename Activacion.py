import csv
import random
import matplotlib.pyplot as plt
import math

#crea archivos para comprobar la valides--------------------------


archivoPrediccion = open ("resultadoDeLaPrediccionDeNumeros.csv","w")
prediccion_csv = csv.writer(archivoPrediccion)
registros = []
registros.append(("ImageId","Label"))
contador = -1
for i in range(0,32001):
	clase =5
	contador = 0
	tuplaNumero=(contador,clase)
	registros.append(tuplaNumero)
	contador += 1
prediccion_csv.writerows(registros)	
archivoPrediccion.close()

#-----------------------------------------------------------------------------------------------------#
predicciones = open('resultadoDeLaPrediccionDeNumeros.csv')
predicciones_csv = csv.reader(predicciones, delimiter=",")
predicciones_csv.next()

matrizPredicciones=[]
for label in predicciones_csv:
	matrizPredicciones.append(label)
predicciones.close()

archivoMiniTest = open('archivoValidacion.csv') 
miniTest_csv = csv.reader(archivoMiniTest, delimiter=",")
miniTest_csv.next()
matrizValidacion=[]
for label in miniTest_csv:
	matrizValidacion.append(label)
archivoMiniTest.close()

cantidadDeNumerosPrueba = range(0,10)
for i in range(0,10):
	cantidadDeNumerosPrueba[i]=0
	
for i in range(0,len(matrizValidacion)):
	cantidadDeNumerosPrueba[int(matrizValidacion[i][0])]=cantidadDeNumerosPrueba[int(matrizValidacion[i][0])] + 1

vectorDeClasesClasificasMal = range(0,10)
for i in range(0,10):
	vectorDeClasesClasificasMal[i]=0

archivoDeFallos = open ("digitosQueFallaron.csv","w")
archivoDeFallos_csv = csv.writer(archivoDeFallos)
registrosDeFallos = []
registrosDeFallos.append("Label")

clasesCalificadasMal=0
totalNumerosAclasificar=0
for i in range(0,len(matrizValidacion)):
	totalNumerosAclasificar+=1
	fila=matrizValidacion[i]
	claseCorrecta=int(fila[0])
	prediccionDeClase=int(matrizPredicciones[i][1])
	"""print "-----------------------------------------------------------"
	print "numero de la posicion: "+str(i)
	print "clase correcta: "+str(claseCorrecta)
	print "prediccion: "+str(prediccionDeClase)
	if (claseCorrecta==prediccionDeClase):
		print "clase correcta"""
	if (claseCorrecta != prediccionDeClase):
		#print "no correcta"
		clasesCalificadasMal= clasesCalificadasMal + 1
		vectorDeClasesClasificasMal[int(claseCorrecta)]= vectorDeClasesClasificasMal[int(claseCorrecta)] + 1
		registrosDeFallos.append(fila)
archivoDeFallos_csv.writerows(registrosDeFallos)		
archivoDeFallos.close()
print "========================================================================="
for i in range(0,10):
	print "para la clase: "+ str(i) + " clasifico mal : "+str(vectorDeClasesClasificasMal[i])+ " de un total de: "+str(cantidadDeNumerosPrueba[i])
print "total de clasificaciones mal: "+str(clasesCalificadasMal)
print "total de numeros a clasificar: "+str(totalNumerosAclasificar)
#---------------------------------------------------------------------------------------------"""
