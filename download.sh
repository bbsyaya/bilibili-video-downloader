#!/bin/bash

# wget下载视频
FS="#"
for line in `cat out/【旧版】游戏王DM（高清片源）.txt`
do
    url=`echo $line | awk -F $FS {'print $1'}`
    out=`echo $line | awk -F $FS {'print $2'}`
    wget --no-clobber $url -O $out
done
