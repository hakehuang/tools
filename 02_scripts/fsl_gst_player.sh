#!/bin/sh
#AACLC  Dec
gst-launch filesrc location=./AAC_ADTS_LC_44_173_2.aac ! mfw_aacdecoder ! alsasink
#gst-launch filesrc location=AAC_ADTS_LC_44_173_2.aac ! mfw_aacdecoder ! volume volume=10 ! alsasink	#For volume adjustment.

#AACPlus
gst-launch filesrc location=./AAC_HE_ADTS_22_64_VBR.aac ! mfw_aacplusdecoder ! alsasink

#MP3Dec
gst-launch filesrc location=./Mpeg1L3_44kHz_176kbps_s_VBR.mp3 ! mfw_mp3decoder ! alsasink

#WMADec
gst-launch filesrc location=./WMA_v91_2pVBR-Peak256kbps_Avg128kbps_48KHz_2_test2_L2.wma ! mfw_asfdemuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_wma10decoder ! alsasink

#WMAProDec
gst-launch filesrc location=./Classical_44_16_2_192000_1_1_M0.wma ! mfw_asfdemuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_wma10decoder ! alsasink

#WMALosslessDec
gst-launch filesrc location=./N1_44_2_16-allsynRTMoff2_Country1.wma ! mfw_asfdemuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_wma10decoder ! alsasink

#WAVLosslessDec
gst-launch filesrc location= ./PCM_44.1khz_1411kbps_2_16bit_zuoche.wav ! wavparse ! alsasink

#RA Playback
gst-launch filesrc location= ./cooker_21kbps_22.05khz_2_mc_sich_ra8_20.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink
gst-launch filesrc location= ./cooker_32kbps_22.05khz_2_Vetenskap_extramaterial_2005-10-31_142936.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink
gst-launch filesrc location= ./cooker_32kbps_22.05khz_2_Vetenskap_mosbricka_2005-03-02_105820.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink
gst-launch filesrc location= ./cooker_32kbps_44.1khz_2_FUN_RM_32.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink
gst-launch filesrc location= ./cooker_44kbps_44.1khz_2_mc_sich_ra8_44.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink
gst-launch filesrc location= ./cooker_64kbps_44.1khz_2_FUN_RM_64.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink
gst-launch filesrc location= ./cooker_64kbps_44.1khz_2_gg.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink
gst-launch filesrc location= ./cooker_96kbps_44.1khz_2_FUN_RM_96.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink
gst-launch filesrc location= ./cooker_131kbps_44.1hhz_6_multichannel.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink
gst-launch filesrc location= ./cooker_131kbps_44.1hhz_6_Surround.ra ! mfw_rmdemuxer ! mfw_radecoder ! alsasink


#VC1Dec
#MX37/51
gst-launch filesrc location=./wmv9_SP@ML_320x240_15fps_230_064Kbps_44kHz.wmv ! mfw_asfdemuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink tv-out=1 tv-mode=1 disp-width=720 disp-height=576 
gst-launch filesrc location=./wmv9_SP@ML_320x240_15fps_230_064Kbps_44kHz.wmv ! mfw_asfdemuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink
#MX31/MX35
gst-launch filesrc location=./wmv9_SP@ML_320x240_15fps_230_064Kbps_44kHz.wmv ! mfw_asfdemuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_wmv9mpdecoder ! mfw_v4lsink

#MPEG4Dec
#MX37/51
gst-launch filesrc location=./Mpeg4_SP1_320x240_15_579_aac_32_96_2_zads1-8.mp4 ! mfw_mp4demuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink tv-out=1 tv-mode=1 disp-width=720 disp-height=576 
gst-launch filesrc location=./Mpeg4_SP1_320x240_15_579_aac_32_96_2_zads1-8.mp4 ! mfw_mp4demuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink
#MX31/MX35
gst-launch filesrc location=./Mpeg4_SP1_320x240_15_579_aac_32_96_2_zads1-8.mp4 ! mfw_mp4demuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_mpeg4decoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_aacdecoder ! alsasink

#H.264Dec
#MX37/51
gst-launch filesrc location=./H264_BP13_320x240_20_701_AAC_44_128_Dont.mp4 ! mfw_mp4demuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink tv-out=1 tv-mode=1 disp-width=720 disp-height=576 
gst-launch filesrc location=./H264_BP13_320x240_20_701_AAC_44_128_Dont.mp4 ! mfw_mp4demuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink
#MX31/MX35
gst-launch filesrc location=./H264_BP13_320x240_20_701_AAC_44_128_Dont.mp4 ! mfw_mp4demuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_h264decoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_aacdecoder ! alsasink

#DivXDec
#MX37/51
gst-launch filesrc location=./a01_divx51b_640x304_870kbps_mp3_44khz_cbr128.avi ! mfw_avidemuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink tv-out=1 tv-mode=1 disp-width=720 disp-height=576 
gst-launch filesrc location=./a01_divx51b_640x304_870kbps_mp3_44khz_cbr128.avi ! mfw_avidemuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink
#MX31/MX35
gst-launch filesrc location=./a01_divx51b_640x304_870kbps_mp3_44khz_cbr128.avi ! mfw_avidemuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_divxdecoder  ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink

#MPEG2Dec
#MX37/51
gst-launch filesrc location=./Mpeg2PS_MP3_MPML_384x288_30fps_a_32khz_224bpsCBR_1_mouments_Super.MPG ! mfw_mpg2demuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink tv-out=1 tv-mode=1 disp-width=720 disp-height=576 
gst-launch filesrc location=./Mpeg2PS_MP3_MPML_384x288_30fps_a_32khz_224bpsCBR_1_mouments_Super.MPG ! mfw_mpg2demuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_vpudecoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink
#MX31/MX35
gst-launch filesrc location=./Mpeg2PS_MP3_MPML_384x288_30fps_a_32khz_224bpsCBR_1_mouments_Super.MPG ! mfw_mpg2demuxer name=demux demux. ! queue max-size-buffers=0 ! mfw_mpeg2decoder ! mfw_v4lsink demux. ! queue max-size-buffers=0 ! mfw_mp3decoder ! alsasink

#RVDec
gst-launch filesrc location= $file ! mfw_rmdemuxer name=dem dem. ! queue ! mfw_vpudecoder ! mfw_v4lsink dem. ! queue ! mfw_radecoder ! alsasink




