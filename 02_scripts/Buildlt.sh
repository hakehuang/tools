#!/bin/sh
#
# Freescale MAD Linux SCM weekly build script
# For VTE test suit
# Author: Hake Huang <b20222>
# 2008-10-21

# Note:
#      the script should be put into $SCRIPT_PATH
#      defined in the script


HEAD_LINE="Linux Test Suite: VTE build"
VIEW_PATH=/vobs/fsl_mad_tt_lnx
VTE_PATH=${VIEW_PATH}/vte
TEMP_PATH=/home/temp
PKG="vte"
SCRIPT_PATH=/home/utils

echo $HEAD_LINE

cd $VIEW_PATH

mkdir -p $TEMP_PATH

if [ ! -e $TEMP_PATH ]
then
echo "temp path not exist. quit!"
exit 1
fi

if [ -z $1 ]
then
 echo "need specify the build week number like WK42"
 exit 1
fi

if [ ! -e $TEMP_PATH ]
then
mkdir -p $TEMP_PATH
fi

LBTYPE=VTE_$1

cleartool mklbtype -c "auto build" $LBTYPE@${VIEW_PATH}
cleartool lock -nusers b18293 lbtype:$LBTYPE@${VIEW_PATH}
cleartool mklabel -replace $LBTYPE .
cd ${VTE_PATH}
cleartool mklabel -replace -recurse $LBTYPE .

tar -zcvf $PKG.tar.gz vte >> ${TEMP_PATH}/log.txt 2>&1
rm -rf ${TEMP_PATH}/
mv $PKG.tar.gz ${TEMP_PATH}/ >> ${TEMP_PATH}/log.txt 2>&1
${SCRIPT_PATH}/vte.sh ${TEMP_PATH}
