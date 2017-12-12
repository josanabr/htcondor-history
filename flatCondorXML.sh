#!/bin/bash
#
# El comando 'condor_history -xml' entrega la salida en XML del historico de 
# ejecuciones de tareas en un cluster basado en HTCondor. Sin embargo, se ha 
# notado como esta salida puede tener varios XML en su interior en lugar de uno
# solo como es de esperarse.
#
# La estructura de este XML tiene algo como esto:
#
#<?xml version="1.0"?>
#<!DOCTYPE classads SYSTEM "classads.dtd">
#<classads>
#
#<c>
#    <a n="ExitBySignal"><b v="f"/></a>
#    <a n="JobLastStartDate"><i>1512668040</i></a>
#    <a n="MachineAttrSlotWeight0"><i>2</i></a>
#    <a n="LastRemoteHost"><s>slot1@uvcluster-02.cloud.univalle.edu.co</s></a>
#    <a n="BytesSent"><r>7.557460000000000E+05</r></a>
#
# Es decir, <?xml ...> <!DOCTYPE...> <classads> ... </classads> es lo que 
# delimita un archivo XML pero en la salida del comando 'condor_history' hay 
# muchas de estas estructuras entonces hay muchos archivos XML
#
# Este script lo que busca es aplanar y dejar un solo archivo XML que tenga la
# siguiente estructura:
# <classads>
#  <c>
#   <a>...
#  </c>
# ...
# </classads>
#
if [ ! ${#} -eq 2 ]; then
  echo "Indicar el nombre del archivo a procesar y el archivo de salida"
  exit -1
fi
archivoIn=${1}
archivoOut=${2}
if [ ! -f ${archivoIn} ]; then
  echo "No se encontro el archivo ${archivoIn}"
  exit -1
fi
if [ -f ${archivoOut} ]; then
  echo -n "${archivoOut} existe. Si desea sobre-escribirlo, " 
  echo "borrar primero antes de volver a correr este comando."
  exit -1
fi
tmpSalida="/tmp/${archivoOut}"
echo -n "Eliminando 'classads' de ${archivoIn}..."
grep -v classads ${archivoIn} > ${tmpSalida}
echo " hecho! Salida en ${tmpSalida}"
echo -n "Eliminando 'xml version' de ${tmpSalida}..."
grep -v "xml version" ${tmpSalida} > ${archivoOut}
echo " hecho! Salida en ${archivoOut}"
echo -n "Anteponiendo '<classads>' al archivo ${archivoOut}.."
echo "<classads>"|cat - ${archivoOut} > ${tmpSalida}
echo " hecho! Salida en ${tmpSalida}"
echo -n "Anadiendo '</classads>' a ${tmpSalida}... "
echo "</classads>" >> ${tmpSalida}
echo " hecho!"
echo -n "Moviendo/renombrando ${tmpSalida} a ${archivoOut}..."
mv ${tmpSalida} ${archivoOut}
echo " hecho!"
