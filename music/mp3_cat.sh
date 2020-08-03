#!/bin/bash
ffmpeg -f concat -i mylist2.txt -c copy output.mp3
