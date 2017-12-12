#!/bin/bash
if [ ! ${#} -eq 2 ]; then
	echo "Se esperan dos argumentos, el XML original y el XML destino"
	exit -1
fi
if [ ! -f ${1} ]; then
	echo "No se encontro archivo [${1}]"
	exit -1
fi
time ./flatCondorXML.sh ${1} ${2}
exit 0
