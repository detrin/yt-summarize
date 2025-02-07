#!/bin/bash

video_url=$1
uuid_dir=$(uuidgen)
mkdir $uuid_dir
cd $uuid_dir
yt-dlp --write-auto-subs --sub-lang en --convert-subs srt --skip-download $video_url
yt-dlp --write-subs --sub-lang en --convert-subs srt --skip-download $video_url
cd ..
echo $uuid_dir
