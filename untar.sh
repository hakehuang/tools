#!/bin/bash -x
cd /rootfs/wb/util/Graphics
for i in $(ls .)
do
  if [ -d $i ]; then
   cd $i
   mkdir test
   for j in $(ls *.gz)
   do
    tar xzvf $j -C test
    echo $j
   done
   cd ..
  fi
done
