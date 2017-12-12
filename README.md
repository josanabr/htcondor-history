# Procesamiento de archivos historicos en XML
HTCondor ofrece un comando llamado `condor_history` que permite extraer el histórico de todas las tareas que se ejecutan en un cluster de HTCondor.

La forma regular como se exportan estos archivos es via XML. 
Sin embargo, el XML si bien permite dar una estructura a la información, la realidad es que la estructura no es estandarizada sino que es libre y en este caso se ha hecho de acuerdo al albeldrío de los desarrolladores de HTCondor.

El objetivo pues de estas herramientas es crear una especie de *pipeline* en el cual se extrae la información del histórico en formato XML, se preprocesa (o se limpia) el archivo XML, se pasan a un formato estándar (e.g. CSV) y se pasan por herramientas que analicen grandes volúmenes de datos (e.g. pandas python).

A continuación se describirán las herramientas alrededor de las etapas definidas anteriormente.

## Generación de información

Para obtener la información histórica de procesos ejecutados en un cluster basado en HTCondor, se debe ejecutar lo siguiente:

```
$ condor_history -xml > salida.xml
```

Este comando almacena en `salida.xml` el histórico de todas las tareas que se ejecutaron en un cluster de HTCondor.

## Preprocesamiento

Un problema que se puede presentar con el XML generado en la etapa anterior es que el archivo de salida (`salida.xml`) realmente sea un archivo que contiene muchos archivos XML en su interior. 
Para convertir todos esos archivos en un solo archivo XML se crea el *script* `sFlatCondorXML.sh`. 
Para ejecutar este *script* se invoca de la siguiente manera:

```
$ ./sFlaCondorXML.sh salida.xml history.xml
```

Lo que hace este script es tomar el archivo `salida.xml`, que es un archivo con múltiples XML en su interior, y generar un nuevo archivo `history.xml` quien es realmente un solo archivo XML.

Para ejecutar este script en un cluster de HTCondor se utiliza el archivo `sFlatCondorXML.condor`. 

Los items **IMPORTANTES** de este archivo de HTCondor son:

* `arguments`: en este Ad se debe colocar, de acuerdo a nuestro ejemplo anterior, `salida.xml` y `history.xml`. 
* `transfer_input_files`: en este Ad se coloca cual es el archivo que se va a preprocesar, en este caso particular `salida.xml`. 
* `transfer_output_files`: en este Ad se coloca cual es el archivo que se desea se regrese al punto desde donde se ejecutó la tarea y este archivo será el insumo para la siguiente etapa, en este caso `history.xml`.

## Transformación

Teniendo ya el único archivo XML con  todo lo histórico, lo que se hace es convertirlo a un formato mas estandarizado como CSV.
Este formato es más relevante porque puede ser leido por diversas herramientas que analizan datos como: R y pandas Python.

Usted puede ejecutar la transformación sin necesidad de HTCondor y puede hacerlo ejecutando el comando

```
$ python _extract.py
```

Pero para lograr que efectivamente se tomen los archivos que se desean procesar es necesario modificar las líneas del archivo `_extract.py`:

```
doc=iterparse('./history.xml',('start','end'))
csvfile = open('./history.csv',"w")
```

Particularmente `history.xml` y `history.csv` por el archivo que usted quiere procesar (en este caso `history.xml`) y el archivo donde quiere que quede el contenido en formato CSV (en este caso `history.csv`).

Esta información esta altamente correlacionada con la información que está en el archivo `_extract.condor`, particularmente en las líneas:

```
transfer_input_files    = _extract.py,history.xml
transfer_output_files   = history.csv
```

Ya que se deben hacer los ajustes correspondientes en caso que usted modifique el código de `_extract.py` y cambie `history.xml` y `history.csv`.

# TAREAS POR HACER

Las siguientes son las listas de tareas que hay pendientes por hacer

* Permitir pasar por parámetros del archivo `_extract.py`: el nombre del archivo XML a ser procesado y el nombre del CSV que almacenará los datos procesados.
* Crear un archivo *DAG* que permita definir la ejecución del *pipeline*.
* Crear un *script* que permita generar los .condor y el .dag descritos anteriormente.
* Estudiar la librería pandas y validar que tipo de información se puede generar a partir de los datos
