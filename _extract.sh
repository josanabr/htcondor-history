#!/bin/bash
if [ ! ${#} -eq 2 ]; then
	echo "Se esperan dos argumentos, el archivo XML y el CSV destino"
	exit -1
fi
if [ ! -f ${1} ]; then
	echo "No se encontro archivo [${1}]"
	exit -1
fi

time python _extract.py ${1} ${2}
exit 0
