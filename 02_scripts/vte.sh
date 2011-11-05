#!/bin/bash
#/*================================================================================================= 

#    Copyright (C) 2004, Freescale Semiconductor, Inc. All Rights Reserved 
#    THIS SOURCE CODE IS CONFIDENTIAL AND PROPRIETARY AND MAY NOT 
#    BE USED OR DISTRIBUTED WITHOUT THE WRITTEN PERMISSION OF 
#    Freescale Semiconductor, Inc. 
#
#====================================================================================================
#Revision History:
#                            Modification     Tracking
#Author                          Date          Number    Description of Changes
#-------------------------   ------------    ----------  -------------------------------------------
#Hake Huang                   10/21/2008       n/a        initialization of vte_release.sh 
#====================================================================================================
#Portability:   gnu compiler
#==================================================================================================*/
#
#/*==================================================================================================
# Need user input the path which containers the vte.tar.gz file          
# ltib environment for each platform is build ok in $LTIB_PATH
#       
#=================================================================================================*/ 

PLATFORM="31 35 37 51 37_24"

#PLATFORM="51"

#PLATFORM="51"
#COMPILER=$(which arm-none-linux-gnueabi-gcc)
COMPILER=/opt/freescale/usr/local/gcc-4.1.2-glibc-2.5-nptl-3/arm-none-linux-gnueabi/bin/arm-none-linux-gnueabi-gcc
REMOTE_PATH=/rootfs/wb/temp
LTIB_PATH=/u/build/nightly_build/build/ltib_build/

#below are path definitions for each platform 
# mx31
MX31_KERNEL_CONFIG=imx31_3stack_defconfig
MX31_KERNEL_PATH=${LTIB_PATH}/imx31_3stack/ltib/rpm/BUILD/linux
MX31_ARCH_PLATFORM=imx31stack
MX31_CFLAGS="-DPROJECT_LPDK=1"
MX31_REMOTE_VTE_PATH=/rootfs/wb/vte_mx31
# mx35
MX35_KERNEL_CONFIG=imx35_3stack_defconfig
MX35_KERNEL_PATH=${LTIB_PATH}/imx35_3stack/ltib/rpm/BUILD/linux
MX35_ARCH_PLATFORM=imx35stack
MX35_REMOTE_VTE_PATH=/rootfs/wb/vte_mx35
MX35_CFLAGS="-DPROJECT_RINGO=1"
# mx37
MX37_KERNEL_CONFIG=imx37_3stack_defconfig
MX37_KERNEL_PATH=${LTIB_PATH}/imx37_3stack/ltib/rpm/BUILD/linux
MX37_ARCH_PLATFORM=imx37stack
MX37_REMOTE_VTE_PATH=/rootfs/wb/vte_mx37
MX37_CFLAGS="-DPROJECT_MARLEY=1"
# mx37-24
MX37_24_KERNEL_CONFIG=imx37_3stack_defconfig
MX37_24_KERNEL_PATH=/u/build/mx37_2.4.2/ltib/rpm/BUILD/linux
MX37_24_ARCH_PLATFORM=imx37stack
MX37_24_REMOTE_VTE_PATH=/rootfs/wb/vte_mx37_24
MX37_24_CFLAGS="-DPROJECT_MARLEY=1"
# mx51
MX51_KERNEL_CONFIG=imx51_3stack_defconfig
MX51_KERNEL_PATH=${LTIB_PATH}/imx51_3stack/ltib/rpm/BUILD/linux
MX51_ARCH_PLATFORM=imx51stack
MX51_REMOTE_VTE_PATH=/rootfs/wb/vte_mx51
MX51_CFLAGS="-DPROJECT_ELVIS=1"

if [ -z $COMPILER ]
then
 echo "cross compiler does not listed in env"
 exit 1
fi


if [ ! -e $1 ]
then
echo "vte does no exist"
exit 1
fi

VTE_PPATH=$1
VTE_PATH=${VTE_PPATH}/vte

#cp the vte source to test server
if [ ! -e ${VTE_PPATH}/vte.tar.gz ]
then
echo "vte package not exit! quit"
exit 2
fi

#prepare local vte
prepare_vte()
{ 
 echo "prepare vte"
 cd ${VTE_PPATH}
 tar xzvf vte.tar.gz >/dev/null
 chmod -R 777 vte
}

#clean old version remote
vte_transfer()
{
  echo "vte transfer"
  ssh root@10.192.225.222 rm -f ${REMOTE_PATH}/vte.tar.gz
  ssh root@10.192.225.222 rm -rf ${REMOTE_PATH}/vte
  scp ${VTE_PPATH}/vte.tar.gz root@10.192.225.222:${REMOTE_PATH}/
  ssh root@10.192.225.222 tar xzvf ${REMOTE_PATH}/vte.tar.gz -C ${REMOTE_PATH}
  ssh root@10.192.225.222 chmod -R 755 ${REMOTE_PATH}/vte
  ssh root@10.192.225.222 cp -a ${REMOTE_PATH}/vte/* ${MX31_REMOTE_VTE_PATH}
  ssh root@10.192.225.222 cp -a ${REMOTE_PATH}/vte/* ${MX35_REMOTE_VTE_PATH}
  ssh root@10.192.225.222 cp -a ${REMOTE_PATH}/vte/* ${MX37_REMOTE_VTE_PATH}
  ssh root@10.192.225.222 cp -a ${REMOTE_PATH}/vte/* ${MX37_24_REMOTE_VTE_PATH}
  ssh root@10.192.225.222 cp -a ${REMOTE_PATH}/vte/* ${MX51_REMOTE_VTE_PATH}
  ssh root@10.192.225.222 mkdir -p ${MX31_REMOTE_VTE_PATH}/testcases/bin
  ssh root@10.192.225.222 mkdir -p ${MX35_REMOTE_VTE_PATH}/testcases/bin
  ssh root@10.192.225.222 mkdir -p ${MX37_REMOTE_VTE_PATH}/testcases/bin
  ssh root@10.192.225.222 mkdir -p ${MX37_24_REMOTE_VTE_PATH}/testcases/bin
  ssh root@10.192.225.222 mkdir -p ${MX51_REMOTE_VTE_PATH}/testcases/bin
  ssh root@10.192.225.222 chmod -R 755 ${MX31_REMOTE_VTE_PATH}
  ssh root@10.192.225.222 chmod -R 755 ${MX35_REMOTE_VTE_PATH}
  ssh root@10.192.225.222 chmod -R 755 ${MX37_REMOTE_VTE_PATH}
  ssh root@10.192.225.222 chmod -R 755 ${MX37_24_REMOTE_VTE_PATH}
  ssh root@10.192.225.222 chmod -R 755 ${MX51_REMOTE_VTE_PATH}
}

export PATH=$PATH:$(dirname ${COMPILER})
export ARCH=arm
export CROSS_COMPILER=arm-none-linux-gnueabi-
export CROSS_COMPILE=arm-none-linux-gnueabi-
#export CROSS_COMPILER=$(dirname ${COMPILER})/arm-none-linux-gnueabi-
export ARCH_CPU=arm

setup_31()
{
 export ARCH_PLATFORM=${MX31_ARCH_PLATFORM}
 export CFLAGS=${MX31_CFLAGS}
 TODIR=${MX31_REMOTE_VTE_PATH}
 KERNEL_PATH=$MX31_KERNEL_PATH
}

setup_35()
{
 export ARCH_PLATFORM=${MX35_ARCH_PLATFORM}
 export CFLAGS=${MX35_CFLAGS}
 TODIR=${MX35_REMOTE_VTE_PATH}
 KERNEL_PATH=$MX35_KERNEL_PATH
}
setup_37()
{
 export ARCH_PLATFORM=${MX37_ARCH_PLATFORM}
 export CFLAGS=${MX37_CFLAGS}
 TODIR=${MX37_REMOTE_VTE_PATH}
 KERNEL_PATH=$MX37_KERNEL_PATH
}
setup_37_24()
{
 export ARCH_PLATFORM=${MX37_24_ARCH_PLATFORM}
 export CFLAGS=${MX37_24_CFLAGS}
 TODIR=${MX37_24_REMOTE_VTE_PATH}
 KERNEL_PATH=$MX37_24_KERNEL_PATH
}
setup_51()
{
 export ARCH_PLATFORM=${MX51_ARCH_PLATFORM}
 export CFLAGS=${MX51_CFLAGS}
 export TODIR=${MX51_REMOTE_VTE_PATH}
 KERNEL_PATH=$MX51_KERNEL_PATH
}

#main function

echo "vte running"
prepare_vte
vte_transfer

for i in $PLATFORM
do

setup_$i

export KLINUX_SRCDIR=${KERNEL_PATH}
export KLINUX_BLTDIR=${KERNEL_PATH}

#compile kernel
#not necessary
#==========================
#CMD=$(echo MX${i}_KERNEL_CONFIG)
#cd ${KERNEL_PATH}
#make distclean
#make $CMD 
#make
#==========================

#compile vte
cd ${VTE_PATH}
make clean
#make ltp
#make vte -k  
make vte -k >MX${i}_vte_build_log_$(date +"%y%m%d") 2>&1 
if [ $? -ne 0 ]
then
echo "Build vte $i fail" | mutt -s "build result for VTE at `date`, do not reply this email! Thanks." -a MX${i}_vte_build_log_$(date +"%y%m%d") spring.zhang@freescale.com -c b20222@freescale.com Victor.Cui@freescale.com Blake.liu@freescale.com Ada.lu@freescale.com lily.li@freescale.com &
else
echo "Build vte $i success" | mutt -s "weekly build result for VTE at `date`, do not reply this email! Thanks."  b20222@freescale.com &
fi

#move vte code to test server
scp -r -C ${VTE_PATH}/testcases/bin root@10.192.225.222:${TODIR}/testcases
scp MX${i}_vte_build_log_$(date +"%y%m%d") root@10.192.225.222:${TODIR}/ 
rm -rf MX${i}_vte_build_log_$(date +"%y%m%d")

if [ $? != 0 ]
then
echo "mx${i} vte build failed"
fi

done

echo "vte SCM build Finished"



