#!/bin/sh -x

IMAGE_LIST="uImage system.img recovery.img"

IMG_PATH=

usage()
{
 cat <<EOF
 usage:
 format_SD.sh [-p <path to images>] -d <SD device node ie. /dev/sdb> \
 [-u] [-b <path to the u-boot-no-padding.bin>]
 -p path to images to be burn
 -d SD device node, not partition
 -u make uImage from zImage 
 -b burn u-boot
EOF
}
#this format has below assumptions
#10M taks 11 cylinders
#30M takes 32 cylinders
# if only we can use /dev/sdb5 resovled
#those dependency will ease.
#poor FSL RD
boot_fdisk_cmd()
{
  if [ -e .SD_PARTITION ]; then
     mv .SD_PARTITION .SD_PARTITION_bk
  fi
  touch .SD_PARTITION
  cat >.SD_PARTITION <<EOF

d
1
d
2
d
3
d
4
d
5
d
6

n
p
1

+1024M

n
p
2

+500M

n
e
3

+280M

n
l

+250M

n
l



n
p
4


d
1

n
p
SHIFT


w
EOF
}

check_size()
{
 SZ=$(fdisk -l $DEVNODE | grep "Units =" | awk '{print $9}')
 SHIFT=$(echo "((10*1024*1024*10)/${SZ}+9)/10" | bc)
 SHIFT=$(expr $SHIFT + 1)
}


mk_uImage()
{
RC=0
if [ ! -e ${IMG_PATH}/uImage ]; then
if [ -e ${IMG_PATH}/zImage ]; then
$(pwd)/tools/mkimage -A arm -O linux -T kernel -C none \
-a 0x90008000 -e 0x90008000 -n "Android Linux Kernel" \
-d ${IMG_PATH}/zImage ${IMG_PATH}/uImage || RC=1
fi
fi
if [ ! -e ${IMG_PATH}/uramdisk.img ]; then
if [ -e ${IMG_PATH}/ramdisk.img ]; then
$(pwd)/tools/mkimage -A arm -O linux -T ramdisk -C none \
-a 0x90308000 -n "Android Root Filesystem" \
-d ${IMG_PATH}/ramdisk.img ${IMG_PATH}/uramdisk.img || RC=1
fi
fi
return $RC
}

umount_SD()
{
mounted=$(mount | grep $DEVNODE | awk '{print $1}' |wc -l)
if [ $mounted -gt 0 ]; then
todo=$(mount | grep $DEVNODE | awk '{print $1}')
for i in $todo
do
umount $DEVNODE
done
fi
}

check_image()
{
if [ -z $IMG_PATH ]; then
IMG_PATH=$(pwd)
fi

for i in $IMAGE_LIST
do
FILE=${IMG_PATH}/$i
if [ ! -e $FILE ];then
echo "error $i not exist"
return 1
fi
done
return 0
}

MU=
RC=
BL=
SHIFT=0
STREAM_PATH=

while getopts hp:d:ub:m: arg
do
    case $arg in
    h) usage ; exit ;;
    p) IMG_PATH=$OPTARG ;;
    d) DEVNODE=$OPTARG ;;
    u) MU=1 ;;
    b) BL=$OPTARG ;;
    m) STREAM_PATH=$OPTARG ;;
    \?)
    usage
    exit 1 ;;
    esac
done


if [ -z $DEVNODE ]; then
echo "need provide the SD device node"
usage
exit 1
fi
mk_uImage || exit 1

check_image || exit 1
boot_fdisk_cmd
umount_SD
check_size
sleep 5

if [ $SHIFT -eg 0  ]; then
echo "Fail to auto get the 10M shift please input: "
SHIFT=12
fdisk -l $DEVNODE
read -p ">" SHIFT
fi

sed -i "s/SHIFT/${SHIFT}/g" ./.SD_PARTITION

fdisk $DEVNODE < ./.SD_PARTITION
sleep 5

if [ ! -z $BL ]; then
dd if=$BL of=$DEVNODE bs=1024 seek=1 || RC="$RC 8"
fi

dd if=${IMG_PATH}/uImage of=$DEVNODE bs=1M seek=1  || RC="$RC 2"
dd if=${IMG_PATH}/uramdisk.img of=$DEVNODE bs=4M seek=1 || RC="$RC 3"

mkfs.vfat ${DEVNODE}1
mkfs.ext3 ${DEVNODE}2
mkfs.ext3 ${DEVNODE}4
mkfs.ext3 ${DEVNODE}5
mkfs.ext3 ${DEVNODE}6

dd if=${IMG_PATH}/system.img of=${DEVNODE}2 || RC="$RC 4"
dd if=${IMG_PATH}/recovery.img of=${DEVNODE}4 || RC="$RC 5"
#dd if=${IMG_PATH}/userdata.img of=${DEVNODE}5 || RC="$RC 6"

if [ $STREAM_PATH ]; then
mkdir -p /mnt/tmpfs
mount -t vfat ${DEVNODE}1 /mnt/tmpfs
cp -a ${STREAM_PATH}/CaiHong.mp3  /mnt/tmpfs
cp -a ${STREAM_PATH}/clip1_15fps.MP4 /mnt/tmpfs
cp -a ${STREAM_PATH}/zly.jpg /mnt/tmpfs
umount /mnt/tmpfs
fi
sync

if [ "$RC" != "0" ]; then
echo "$RC error"
exit 1
fi



 
