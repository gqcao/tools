#!/bin/bash

URL="https://download.library.lol/main/1298000/74def197eccb1a52d9694f2b7a88bebd/Donald%20E.%20Knuth%20-%20The%20Art%20of%20Computer%20Programming%2C%20Volume%201_%20Fundamental%20Algorithms%20%283rd%20Edition%29.%201-Addison-Wesley%20Professional%20%281997%29.epub"

nohup wget $URL --no-check-certificate 1> 00dl.out 2> 00dl.err &
