#!/usr/bin/env python
# -*- coding: latin-1 -*-
#
# Este script en Python espera procesar un archivo XML que contiene la 
# informacion arrojada por el comando 'condor_history -xml'
#
# Asi mismo, la informacion tomada del archivo XML es guardada en un archivo 
# formato CSV. Los encabezados de dicho archivo estan dados por las palabras en
# la variable 'tags'.
#
# Developer: Edier Zapata - edalzap@gmail.com
# Maintainer: John Sanabria - john.sanabria@correounivalle.edu.co
# Date: Diciembre 9, 2017
#
# Links de referencia
# - http://boscoh.com/programming/reading-xml-serially.html
# - http://stackoverflow.com/questions/7171140/using-python-iterparse-for-large-xml-files
# - http://www.diveintopython3.net/xml.html
# - http://chimera.labs.oreilly.com/books/1230000000393/ch06.html#_parsing_huge_xml_files_incrementally
from xml.etree.ElementTree import iterparse
import csv

# Tags a recolectar
tags=[
"User",
"ClusterId",
"ProcId",
"CompletionDate", # Finish date
"JobCurrentStartDate", # Last run start
"BytesSent",
"BytesRecvd",
"DiskUsage_RAW", # KB
"JobStatus",
"LastJobStatus",
"DiskUsage" # KB
]

doc=iterparse('./history.xml',('start','end'))
csvfile = open('./history.csv',"w")
writer = csv.DictWriter(csvfile, fieldnames = tags)
writer.writeheader()
# evita el primer encabezado
next(doc)
# Totales
numTasks = 0
totalBytesSent = 0
totalBytesRecv = 0
totalElapsedTime = 0
diskUsed = 0
# Parciales por tarea
user=""
completionDate = 0
jobCurrentStartDate = 0
clusterId = 0
procId = 0
bytesSent = 0
bytesRecv = 0
diskUsage = 0
diskUsageRaw = 0
jobStatus = 0
lastJobStatus = 0
errorCount = 0
ignoredTasks = 0
#
# Se recorreran cada una de las lineas del archivo XML arrojado por el comando
# condor_history -xml
#
# El archivo contiene algo similar lo que contiene el archivo 'otro.xml'.
# Se asume que condor_history hace bien su trabajo y arroja un XML bien 
# formado.
#
# Ahora, cada nueva tarea en el XML se define con la marca <c> y su 
# terminacion se indica con la marca </c>.
#
# Los atributos de la tarea se definen con la marca <a> y cada atributo tien
# asociado un valor que puede ser booleano (<b></b>), entero (<i></i>),
# real (<r>,</r>) o cadena de caracteres (<s></s>).
#
# Ahora, cada vez que se alcanza una marca <a/> se valida si es un atributo
# de nuestro interes. Los atributos de interes estan definidos en el arreglo
# 'tags'. 
#
# Dependiendo del atributo encontrado se guardara su valor en la 
# correspondiente variable.
#
# Una vez se encuentra un marcador de finalizacion de tarea </c> se procede
# a consolidar la informacion de la tarea bajo observacion. Los valores que
# correspondan seran guardados en unas variables globales o totales.
#
# Puede suceder dentro del procesamiento aparezca un error para tomar el dato,
# ejemplo se quiere convertir una cadena de caracteres a un valor que el 
# lenguaje no puede hacer. En ese caso, cualquier analisis sobre los datos
# se invalida y solo se pueden volver a considerar valores una vez se termine
# de procesar la tarea que causo el problema. Esto se logra cuando se llega
# a una marca de finalizacion de tarea </c>.
#
flagOK = True
for event,elem in doc:
  if event == 'start' and elem.tag == 'a': # se encontro un atributo
    if flagOK: # No ha habido problemas hasta el momento
      if tags.count(elem.get('n')) > 0: # Se encuentra alguno de los tags
        if elem.get('n') == 'User':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          user = elem.text
        if elem.get('n') == 'CompletionDate':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            completionDate = int(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR completionDate %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
        if elem.get('n') == 'JobCurrentStartDate':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            jobCurrentStartDate = int(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR jobCurrentStartDate %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
        if elem.get('n') == 'ClusterId':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            clusterId = int(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR clusterId %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
        if elem.get('n') == 'ProcId':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            procId = int(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR ProcId %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
        if elem.get('n') == 'BytesSent':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            bytesSent = float(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR bytesSent %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
        if elem.get('n') == 'BytesRecvd':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            bytesRecv = float(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR bytesRecvd %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
        if elem.get('n') == 'DiskUsage':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            diskUsage = int(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR DiskUsage %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
        if elem.get('n') == 'JobStatus':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            jobStatus = int(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR jobStatus %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
        if elem.get('n') == 'LastJobStatus':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            lastJobStatus = int(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR lastJobStatus %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
        if elem.get('n') == 'DiskUsage_RAW':
          (event, elem) = next(doc)
          # Al leer el proximo elemento se tiene algo como <i>...</i>
          try: 
            diskUsageRaw = int(elem.text)
          except TypeError:
            flagOK = False
            errorCount = errorCount + 1
            print("[%s - %s] ERROR diskUsageRaw %s.%s %s"%(errorCount,numTasks,clusterId,procId,elem.text))
            pass
  # Una marca de fin de tarea
  elif event == 'end' and elem.tag == 'c':
    if flagOK: # La tarea no presento errores
      numTasks = numTasks + 1
      totalBytesSent = totalBytesSent + bytesSent
      totalBytesRecv = totalBytesRecv + bytesRecv
      if (completionDate > jobCurrentStartDate):
        totalElapsedTime = totalElapsedTime + (completionDate - jobCurrentStartDate)
      if (diskUsageRaw < diskUsage):
        diskUsed = diskUsed + diskUsageRaw
      #ClusterID ProcessId User ElapsedTime BytesS BytesR DUR DiskUNUsed
      #print("%s %s %s %s %s %s %s %s"%(clusterId, procId, user, str(completionDate - jobCurrentStartDate), bytesSent, bytesRecv, diskUsageRaw, str(diskUsage - diskUsageRaw)))
      writer.writerow({'User': user, 'ClusterId': clusterId, \
              'ProcId': procId, 'CompletionDate': completionDate, \
              'JobCurrentStartDate': jobCurrentStartDate, \
              'BytesSent': bytesSent, 'BytesRecvd': bytesRecv, \
              'DiskUsage_RAW': diskUsageRaw, 'JobStatus': jobStatus, \
              'LastJobStatus': lastJobStatus, 'DiskUsage': diskUsage})
    else: # La tarea presento errores y es ignorada, se limpian todas las vars
      ignoredTasks = ignoredTasks + 1
      flagOK = True
    # reset variables
    user=""
    completionDate = 0
    jobCurrentStartDate = 0
    clusterId = 0
    procId = 0
    bytesSent = 0
    bytesRecv = 0
    diskUsage = 0
    jobStatus = 0
    lastJobStatus = 0
    diskUsageRaw = 0
  elem.clear()

print("Numero de tareas %s BytesSent %s BytesRecv %s DiskUsed %s ElapsedTime %s"%(str(numTasks), str(totalBytesSent), str(totalBytesRecv), str(diskUsed), str(totalElapsedTime)))
print("Tareas ignoradas %s errores %s"%(ignoredTasks,errorCount))
