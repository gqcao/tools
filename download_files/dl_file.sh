#!/bin/bash

URL=""

nohup wget $URL --no-check-certificate 1> 00dl.out 2> 00dl.err &
