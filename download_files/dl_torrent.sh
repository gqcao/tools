#!/bin/bash

DL_PATH=$HOME/Downloads
URL=""

nohup transmission-cli -u 1 -w $DL_PATH $URL 1> 00torr.out 2> 00torr.err &
