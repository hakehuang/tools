TARGET_ROOTFS_BASE="/mnt/nfs_root/"
BUILD=y
TOOLS_PATH=/home/ltibs/tools
ROOTDIR=$(pwd)

export PATH=$PATH:/opt/freescale/usr/local/gcc-4.4.4-glibc-2.11.1-multilib-1.0/arm-fsl-linux-gnueabi/bin

RC=0

platfm_rootfs="imx50_rootfs"  "imx53_rootfs" "ubuntu_10.10"
#below is the matrix for gpu applications
declare -a apps;
declare -a apps_configs;
declare -a apps_dir;
declare -a target_rootfs;
declare -a platfm_rootfs_config;
platfm_rootfs_config=("FB" "FB" "XGL");
apps_cnt=4
apps=("3DMarkMobile.git" "bbPinball.git" "openGLES.git" "openVG.git");
apps_configs_FB=("fsl_imx_linux" "master" "FB" "framebuffer_crosscompile");
apps_configs_XGL=("fsl_egl_x" "xwindow" "master" "egl_x_crosscompile");
apps_dir_FB=("configuration/fsl_imx_linux" "mak" "." ".");
apps_dir_XGL=("configuration/iMX51_pdk" "mak" "." ".");

iplat_cnt=0
export CROSS_COMPILE=arm-none-linux-gnueabi-

for k in $platfm_rootfs
do
  TARGET_ROOTFS=${TARGET_ROOTFS_BASE}/$k
  icnt=0
  if [ $BUILD = 'y' ]; then
    while [ $icnt -lt $apps_cnt ]; do
      CUR_CONFIG=${platfm_rootfs_config[${$iplat_cnt}]}
      cd $ROOTDIR
      apps_name=${apps[${icnt}]}
      apps_config=${apps_configs_${CUR_CONFIG}[${icnt}]}
      cdir=$(echo $apps_name | cut -d"." -f 1) 
      if [ ! -e $cdir ]; then
       git clone git://10.192.225.222/Graphics/$apps_name
      fi
      cd $cdir
      git checkout -b temp || git checkout temp
      if [ -nz $? ]; then
       git add .
       git commit -s -m"reset"
       git reset --hard HEAD~1
       git checkout -b temp || git checkout temp
      fi
      git branch -D build_${apps_config}
      git fetch origin +${apps_config}:build_${apps_config} && git checkout build_${apps_config} || exit -3
      cd ${apps_dir_${CUR_CONFIG}[${icnt}]}
      make ROOTFS=${TARGET_ROOTFS} || exit -5
      make clean
      cd $ROOTDIR/$cdir
      git add .
      git commit -s -m"make result"
      icnt=$(expr $icnt + 1)
    done
  fi
done

echo "gpu apps build" | mutt -s "gpu build OK" \
b20222@shlx12.ap.freescale.net 

