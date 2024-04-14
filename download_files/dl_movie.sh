#!/bin/bash

DL_PATH=$HOME/Downloads/videos
TORRENT_PATH=$HOME/Downloads
TORRENT_FILE=foo.torrent

nohup transmission-cli -u 1 -w $DL_PATH $TORRENT_PATH/$TORRENT_FILE 1> 00vid.out 2> 00vid.err &
