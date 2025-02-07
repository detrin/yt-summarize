#!/bin/bash

# https://www.youtube.com/watch?v=-v6M_MEbkbI
video_url=$1
uuid_dir=$(uuidgen)
yt-dlp --write-auto-subs --sub-lang en --convert-subs srt --skip-download -P "home:$uuid_dir" $video_url
yt-dlp --write-subs --sub-lang en --convert-subs srt --skip-download -P "home:$uuid_dir" $video_url
echo $uuid_dir
