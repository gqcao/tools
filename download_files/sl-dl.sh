#!/bin/bash
#-----------------------------------------------
# Modify 4/08/2018 by giudinvx
# Email  giudinvx[at]gmail[dot]com 
#-----------------------------------------------

# Author: Andrea Lazzarotto
# http://andrealazzarotto.com
# andrea.lazzarotto@gmail.com

# Slideshare Downloader
# This script takes a slideshare presentation URL as an argument and
# carves all the slides in flash format, then they are converted to
# and finally merged as a PDF

# License:
# Copyright 2010-2011 Andrea Lazzarotto
# This script is licensed under the Gnu General Public License v3.0.
# You can obtain a copy of this license here: http://www.gnu.org/licenses/gpl.html

# Usage:
# slideshare-downloader.sh URL -s [NUMBER OF SLIDES TO DOWNLOAD] -q [QUALTY OF IMAGES 320,1024]
check_dependencies() {
	# Verifies if all binaries are present
	DEP="wget sed seq convert"
	ERROR="0"
	for i in $DEP; do
		WHICH="`which $i`"
		if [[ "x$WHICH" == "x" ]];
			then
				echo "Error: $i not found."
				ERROR="1"
		fi
	done
	if [ "$ERROR" -eq "1" ];
		then
			echo "You need to install some packages."
			echo "Remember: this script requires Wget and Convert."
			exit 1
	fi
}

validate_input() {
	# Performs a very basic check to see if the url is in the correct form
	URL=`echo "$1" | cut -d "#" -f 1 | cut -d "/" -f 3`
	q=638
	DOMAIN=`echo "$URL" | cut -d "/" -f 3`
	CORRECT='www.slideshare.net'
	myArray=("$@")

	if [ "$DOMAIN" != "$CORRECT" ]
		then
			echo "Provided URL is not valid." >&2
			exit 1
	fi

	for i in "$@"
		do
			l=$((l + 1))
			case $i in
				-s)
					s=${myArray[$l]}
					;;
				-q)
					q=${myArray[$l]}
					;;
				-h)
					echo "Use -s (total number of slides) | -q (quality of slides, default is 638px) [320,1024,728]" >&2
					exit 1
					;;
		esac
	done

	#check if the number of slides is setted
	if echo -n "$s" | grep "^[0-9]*$">/dev/null
		then SIZE=$s
	else
		SIZE=10
			echo "Size of total nomber of slides not defined... trying to extracting it, or defaulting is 10." 
	fi
	#check if the quality of slides to download is setted
	if [ $q -eq 320 ] || [ $q -eq 1024 ] || [ $q -eq 728 ]
		then QUALITY=$q
	else
		QUALITY=638
			echo "Quality of images not defined... defaulting to 638." 
	fi
}

build_params() {
	# Gathers required information
	DOCSHORT=`echo "$1" | cut -d "/" -f 5`
	echo "Download of $DOCSHORT started."
	echo "Fetching information..."
	INFOPAGE=`wget -q -O - "$1"`
	#trying to capture the url of the first slide .jpg
	IMGURL=`echo "$INFOPAGE" | grep "data-normal" | head -n 1 | grep -oP "(?<=data-normal=\")[^\"]+(?=\")" | cut -d "?" -f1`
	#try to extract the total number of slides
	#SIZE=`echo "$INFOPAGE" | grep "totalSlides" | head -n 1 | sed -s "s/.*total-slides//g" | sed s/[^0-9]//g`
	#if [[ "$SIZE" =~ ([0-9]+)$ ]]
	#	then
	#		echo "Number of slide found - $SIZE"
	#fi
}

create_env() {
	# Finds a suitable name for the destination directory and creates it
	DIR=$DOCSHORT
	if [ -e "$DIR" ];
		then
			I="-1"
			OLD=$DIR
			while [ -e "$DIR" ]
			do
				I=$(( $I + 1 ))
				DIR="$OLD.$I"
			done
	fi
	mkdir "$DIR"
}

fetch_slides() {
	#clean the string from the dynamic param
	NURL=`echo $IMGURL | sed "s/[0-9]-[0-9]*\.jpg$//g"`
	#download all slides in jpg format
	for i in $( seq 1 $SIZE ); do
		echo "Downloading slide $i"
		echo $NURL`echo $i`-`echo $QUALITY`.jpg
		wget "$NURL`echo $i`-`echo $QUALITY`.jpg" -q -O "$DIR/slide-`echo $i`.jpg"
	done
	echo "All slides downloaded."
}

build_pdf() {
	IMAGES=`ls $DIR/*.jpg | sort -V`
	echo "Generating PDF..."
	convert $IMAGES $DIR/$DOCSHORT.pdf
	echo "The PDF has been generated."
	echo "Find your presentation in: \"`pwd`/$DIR/$DOCSHORT.pdf\""
}

clean() {
	rm -rf $DIR/slide-*.jpg
}

check_dependencies
validate_input $@
build_params $@
create_env
fetch_slides
build_pdf
clean
