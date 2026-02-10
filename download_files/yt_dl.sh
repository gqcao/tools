#!/bin/bash

YT_TOOL=yt-dlp  # yt-dlp, or youtube-dl
YT_URL=

nohup $YT_TOOL --extract-audio --audio-format mp3 $YT_URL 1> 00dl_mp3.out 2> 00dl_mp3.err &
#nohup $YT_TOOL $YT_URL 1> 00dl_mp3.out 2> 00dl_mp3.err &
