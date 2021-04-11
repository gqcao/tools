#!/bin/bash
ffmpeg -f concat -safe 0 -i mylist2.txt -c copy output.mp3
