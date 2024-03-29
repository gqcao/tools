#!/bin/bash

YT_URL=https://www.youtube.com/watch?v=8dcJ-U1dUx0

nohup youtube-dl --extract-audio --audio-format mp3 $YT_URL 1> 00dl_mp3.out 2> 00dl_mp3.err &
#nohup youtube-dl $YT_URL 1> 00dl_mp3.out 2> 00dl_mp3.err &
