#!/bin/bash
#
# Developed by Fred Weinhaus 6/9/2009 .......... revised 12/18/2017
#
# ------------------------------------------------------------------------------
# 
# Licensing:
# 
# Copyright © Fred Weinhaus
# 
# My scripts are available free of charge for non-commercial use, ONLY.
# 
# For use of my scripts in commercial (for-profit) environments or 
# non-free applications, please contact me (Fred Weinhaus) for 
# licensing arrangements. My email address is fmw at alink dot net.
# 
# If you: 1) redistribute, 2) incorporate any of these scripts into other 
# free applications or 3) reprogram them in another scripting language, 
# then you must contact me for permission, especially if the result might 
# be used in a commercial or for-profit environment.
# 
# My scripts are also subject, in a subordinate manner, to the ImageMagick 
# license, which can be found at: http://www.imagemagick.org/script/license.php
# 
# ------------------------------------------------------------------------------
# 
####
#
# USAGE: textcleaner [-r rotate] [-l layout] [-c cropoff] [-g] [-e enhance ] 
# [-f filtersize] [-o offset] [-u]  [-t threshold] [-s sharpamt] [-s saturation] 
# [-a adaptblur] [-T] [-p padamt] [-b bgcolor] [-F fuzzval] [-i invert] infile outfile
# USAGE: textcleaner [-help]
#
# OPTIONS:
#
# -r	  rotate			rotate image 90 degrees in direction specified if 
#                           aspect ratio does not match layout; options are cw 
#                           (or clockwise), ccw (or counterclockwise) and n 
#                           (or none); default=none or no rotation
# -l      layout            desired layout; options are p (or portrait) or 
#                           l (or landscape); default=portrait
# -c      cropoff			image cropping offsets after potential rotate 90; 
#                           choices: one, two or four non-negative integer comma 
#                           separated values; one value will crop all around; 
#                           two values will crop at left/right,top/bottom; 
#                           four values will crop left,top,right,bottom
# -g                        convert document to grayscale before enhancing
# -e      enhance           enhance image brightness before cleaning;
#                           choices are: none, stretch or normalize; 
#                           default=stretch
# -f      filtersize        size of filter used to clean background;
#                           integer>0; default=15
# -o      offset            offset of filter in percent used to reduce noise;
#                           integer>=0; default=5
# -u                        unrotate image; cannot unrotate more than 
#                           about 5 degrees
# -t      threshold			text smoothing threshold; 0<=threshold<=100; 
#                           nominal value is about 50; default is no smoothing
# -s      sharpamt          sharpening amount in pixels; float>=0; 
#                           nominal about 1; default=0
# -S      saturation        color saturation expressed as percent; integer>=0; 
#                           only applicable if -g not set; a value of 100 is 
#                           no change; default=200 (double saturation)
# -a      adaptblur         alternate text smoothing using adaptive blur; 
#                           floats>=0; default=0 (no smoothing)
# -T         				trim background around outer part of image 
# -p      padamt			border pad amount around outer part of image;
#                           integer>=0; default=0
# -b      bgcolor           desired color for background or "image"; default=white
# -F      fuzzval           fuzz value for determining bgcolor when bgcolor=image; 
#                           integer>=0; default=10
# -i      invert            invert colors; choices are: 1 or 2 for one-way or two-ways
#                           (input or input and output); default is no inversion
#
###
#
# NAME: TEXTCLEANER
# 
# PURPOSE: To process a scanned document of text to clean the text background.
# 
# DESCRIPTION: TEXTCLEANER processses a scanned document of text to clean
# the text background and enhance the text. The order of processing is:
# 1) optional 90 degree rotate if aspect does not match layout
# 2) optional crop, 
# 3) optional convert to grayscale, 
# 4) optional enhance, 
# 5) filter to clean background and optionally smooth/antialias, 
# 6) optional unrotate (limited to about 5 degrees or less), 
# 7) optional text smoothing,
# 8) optional sharpening, 
# 9) optional saturation change (if -g is not specified), 
# 10) optional alternate text smoothing via adaptive blur
# 11) optional auto trim of border (effective only if background well-cleaned),
# 12) optional pad of border
# 
# OPTIONS: 
# 
# -r rotate ... ROTATE image either clockwise or counterclockwise by 90 degrees,
# if image aspect ratio does not match the layout mode. Choices are: cc (or 
# clockwise), ccw (or counterclockwise) and n (or none). The default is no rotation.
# 
# -l layout ... LAYOUT for determining if rotation is to be applied. The choices 
# are p (or portrait) or l (or landscape). The image will be rotated if rotate is 
# specified and the aspect ratio of the image does not match the layout chosen. 
# The default is portrait.
#
# -c cropoffsets ... CROPOFFSETS are the image cropping offsets after potential 
# rotate 90. Choices: one, two or four non-negative integer comma separated 
# values. One value will crop all around. Two values will crop at 
# left/right,top/bottom. Four values will crop left,top,right,bottom.
# 
# -g ... Convert the document to grayscale.
# 
# -e enhance ... ENHANCE brightness of image. The choices are: none, stretch, 
# or normalize. The default=stretch.
# 
# -f filtersize ... FILTERSIZE is the size of the filter used to clean up the 
# background. Values are integers>0. The filtersize needs to be larger than 
# the thickness of the writing, but the smaller the better beyond this. Making it 
# larger will increase the processing time and may lose text. The default is 15. 
#
# -o offset ... OFFSET is the offset threshold in percent used by the filter  
# to eliminate noise. Values are integers>=0. Values too small will leave much 
# noise and artifacts in the result. Values too large will remove too much 
# text leaving gaps. The default is 5. 
# 
# -u ... UNROTATE the image. This is limited to about 5 degrees or less.
# 
# -t threshold ... THRESHOLD is the text smoothing threshold. Values are integers 
# between 0 and 100. Smaller values smooth/thicken the text more. Larger values 
# thin, but can result in gaps in the text. Nominal value is in the middle at 
# about 50. The default is to disable smoothing.
#
# -s sharpamt ... SHARPAMT is the amount of pixel sharpening to be applied to  
# the resulting text. Values are floats>=0. If used, it should be small 
# (suggested about 1). The default=0 (no sharpening). 
# 
# -S saturation ... SATURATION is the desired color saturation of the text 
# expressed as a percentage. Values are integers>=0. A value of 100 is no change. 
# Larger values will make the text colors more saturated. The default=200  
# indicates double saturation. Not applicable when -g option specified.
# 
# -a adaptblur ... ADAPTBLUR applies an alternate text smoothing using 
# an adaptive blur. The values are floats>=0. The default=0 indicates no 
# blurring.
# 
# -T ... TRIM the border around the image.
# 
# -p padamt ... PADAMT is the border pad amount in pixels. The default=0.
# 
# -b bgcolor ... BGCOLOR is the desired background color after it has been 
# cleaned up. Any valid IM color may be use. If bgcolor=image, then the color will 
# be computed from the top left corner pixel and a fuzzval. The final color will be 
# computed subsequently as an average over the whole image. The default is white.
#
# -F fuzzval ... FUZZVAL is the fuzz value for determining bgcolor when bgcolor=image. 
# Values are integers>=0. The default=10.
#
# -i invert ... INVERT colors for example to convert white text on black background to 
# black text on white background. The choices are: 1 or 2 for one-way or two-ways
# (input or input and output). The default is no inversion.
# 
# CAVEAT: No guarantee that this script will work on all platforms, 
# nor that trapping of inconsistent parameters is complete and 
# foolproof. Use At Your Own Risk. 
# 
######
#

# set default values
rotate="none"		# rotate 90 clockwise (cw) or counterclockwise (ccw)
layout="portrait"   # rotate 90 to match layout; portrait or landscape
cropoff=""			# crop amounts; comma separate list of 1, 2 or 4 integers
numcrops=0			# number of crops flag
gray="no"			# convert to grayscale flag
enhance="stretch"	# none, stretch, normalize
filtersize=15		# local area filter size
offset=5			# local area offset to remove "noise"; too small-get noise, too large-lose text
threshold=""        # smoothing threshold
sharpamt=0			# sharpen sigma
saturation=200		# color saturation percent; 100 is no change
adaptblur=0			# adaptive blur
unrotate="no"		# unrotate flag
trim="no"			# trim flag
padamt=0			# pad amount
bgcolor="white"		# color for output whiteboard background
fuzzval=10			# fuzz value for determining bgcolor from image
invert=""			# invert colors: 1 or 2

# set directory for temporary files
dir="."    # suggestions are dir="." or dir="/tmp"

# set up functions to report Usage and Usage with Description
PROGNAME=`type $0 | awk '{print $3}'`  # search for executable on path
PROGDIR=`dirname $PROGNAME`            # extract directory of program
PROGNAME=`basename $PROGNAME`          # base name of program
usage1() 
	{
	echo >&2 ""
	echo >&2 "$PROGNAME:" "$@"
	sed >&2 -e '1,/^####/d;  /^###/g;  /^#/!q;  s/^#//;  s/^ //;  4,$p' "$PROGDIR/$PROGNAME"
	}
usage2() 
	{
	echo >&2 ""
	echo >&2 "$PROGNAME:" "$@"
	sed >&2 -e '1,/^####/d;  /^######/g;  /^#/!q;  s/^#*//;  s/^ //;  4,$p' "$PROGDIR/$PROGNAME"
	}


# function to report error messages
errMsg()
	{
	echo ""
	echo $1
	echo ""
	usage1
	exit 1
	}


# function to test for minus at start of value of second part of option 1 or 2
checkMinus()
	{
	test=`echo "$1" | grep -c '^-.*$'`   # returns 1 if match; 0 otherwise
    [ $test -eq 1 ] && errMsg "$errorMsg"
	}

# test for correct number of arguments and get values
if [ $# -eq 0 ]
	then
	# help information
   echo ""
   usage2
   exit 0
elif [ $# -gt 31 ]
	then
	errMsg "--- TOO MANY ARGUMENTS WERE PROVIDED ---"
else
	while [ $# -gt 0 ]
		do
			# get parameter values
			case "$1" in
		  -h|-help)    # help information
					   echo ""
					   usage2
					   exit 0
					   ;;
			   	-r)    # rotate
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID ROTATE SPECIFICATION ---"
					   checkMinus "$1"
					   rotate=`echo "$1" | tr "[:upper:]" "[:lower:]"`
					   case "$rotate" in
					   		none|n) rotate="none" ;;
					   		clockwise|cw) rotate="cw" ;;
					   		counterclockwise|ccw) rotate="ccw" ;;
					   		*) errMsg "--- ROTATE=$rotate IS NOT A VALID CHOICE ---" ;;
					   esac
					   ;;
			   	-l)    # layout
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID LAYOUT SPECIFICATION ---"
					   checkMinus "$1"
					   layout=`echo "$1" | tr "[:upper:]" "[:lower:]"`
					   case "$layout" in
					   		portrait|p) layout="portrait" ;;
					   		landscape|l) layout="landscape" ;;
					   		*) errMsg "--- LAYOUT=$layout IS NOT A VALID CHOICE ---" ;;
					   esac
					   ;;
				-c)    # get cropoffsets
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID CROPOFFSETS SPECIFICATION ---"
					   checkMinus "$1"
					   cropoff="$1"
					   cropoff="${cropoff},"
					   cropoff=`expr "$cropoff" : '\([,0-9]*\)'`
					   numcrops=`echo "$cropoff" | tr "," " " | wc -w` 
					   [ "$cropoff" = "" ] && errMsg "--- ONE OR TWO OR FOUR OFFSETS MUST BE PROVIDED ---"
					   [ $numcrops -ne 1 -a $numcrops -ne 2 -a $numcrops -ne 4 ] && errMsg "--- ONE OR TWO OR FOUR OFFSETS MUST BE PROVIDED ---"
					   crop1=`echo "$cropoff" | cut -d, -f1`
					   crop2=`echo "$cropoff" | cut -d, -f2`
					   crop3=`echo "$cropoff" | cut -d, -f3`
					   crop4=`echo "$cropoff" | cut -d, -f4`
					   ;;
			   	-g)    # set grayscale
					   gray="yes"
					   ;;
			   	-e)    # get enhance
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID ENHANCE SPECIFICATION ---"
					   checkMinus "$1"
					   enhance="$1"
					   case "$1" in
					   		none) ;;
					   		stretch) ;;
					   		normalize) ;;
					   		*) errMsg "--- ENHANCE=$enhance IS NOT A VALID CHOICE ---" ;;
					   esac
					   ;;
				-f)    # get filtersize
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID FILTERSIZE SPECIFICATION ---"
					   checkMinus "$1"
					   filtersize=`expr "$1" : '\([0-9]*\)'`
					   [ "$filtersize" = "" ] && errMsg "--- FILTERSIZE=$filtersize MUST BE A NON-NEGATIVE INTEGER ---"
					   filtersizetest=`echo "$filtersize < 1" | bc`
					   [ $filtersizetest -eq 1 ] && errMsg "--- FILTERSIZE=$filtersize MUST BE AN INTEGER GREATER THAN 0 ---"
					   ;;
				-o)    # get offset
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID OFFSET SPECIFICATION ---"
					   checkMinus "$1"
					   offset=`expr "$1" : '\([0-9]*\)'`
					   [ "$offset" = "" ] && errMsg "--- OFFSET=$offset MUST BE A NON-NEGATIVE INTEGER ---"
					   ;;
				-t)    # get threshold
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID THRESHOLD SPECIFICATION ---"
					   checkMinus "$1"
					   threshold=`expr "$1" : '\([0-9]*\)'`
					   [ "$threshold" = "" ] && errMsg "--- THRESHOLD=$threshold MUST BE A NON-NEGATIVE INTEGER ---"
					   thresholdtestA=`echo "$threshold < 0" | bc`
					   thresholdtestB=`echo "$threshold > 100" | bc`
					   [ $thresholdtestA -eq 1 -o $thresholdtestB -eq 1 ] && errMsg "--- THRESHOLD=$threshold MUST BE AN INTEGER GREATER BETWEEN 0 AND 100 ---"
					   ;;
				-s)    # get sharpamt
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID SHARPAMT SPECIFICATION ---"
					   checkMinus "$1"
					   sharpamt=`expr "$1" : '\([.0-9]*\)'`
					   [ "$sharpamt" = "" ] && errMsg "--- SHARPAMT=$sharpamt MUST BE A NON-NEGATIVE FLOAT ---"
					   ;;
				-S)    # get saturation
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID SATURATION SPECIFICATION ---"
					   checkMinus "$1"
					   saturation=`expr "$1" : '\([0-9]*\)'`
					   [ "$saturation" = "" ] && errMsg "--- SATURATION=$saturation MUST BE A NON-NEGATIVE INTEGER ---"
					   ;;
				-a)    # get adaptblur
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID ADAPTBLUR SPECIFICATION ---"
					   checkMinus "$1"
					   adaptblur=`expr "$1" : '\([.0-9]*\)'`
					   [ "$adaptblur" = "" ] && errMsg "--- ADAPTBLUR=$adaptblur MUST BE A NON-NEGATIVE FLOAT ---"
					   ;;
			   	-u)    # set unrotate
					   unrotate="yes"
					   ;;
			   	-T)    # set trim
					   trim="yes"
					   ;;
				-p)    # get padamt
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID PADAMT SPECIFICATION ---"
					   checkMinus "$1"
					   padamt=`expr "$1" : '\([0-9]*\)'`
					   [ "$padamt" = "" ] && errMsg "--- PADAMT=$padamt MUST BE A NON-NEGATIVE INTEGER ---"
					   ;;
			   	-b)    # get bgcolor
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID BACKGROUND COLOR SPECIFICATION ---"
					   checkMinus "$1"
					   bgcolor="$1"
					   ;;
				-F)    # get fuzzval
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID FUZZVAL SPECIFICATION ---"
					   checkMinus "$1"
					   fuzzval=`expr "$1" : '\([0-9]*\)'`
					   [ "$fuzzval" = "" ] && errMsg "--- FUZZVAL=$fuzzval MUST BE A NON-NEGATIVE INTEGER ---"
					   ;;
				-i)    # get invert
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID INVERT SPECIFICATION ---"
					   checkMinus "$1"
					   invert=`expr "$1" : '\([0-9]*\)'`
					   [ "$invert" = "" ] && errMsg "--- INVERT=$invert MUST BE A NON-NEGATIVE INTEGER ---"
					   testA=`echo "$invert < 1" | bc`
					   testB=`echo "$invert > 2" | bc`
					   [ $testA -eq 1 -o $testB -eq 1 ] && errMsg "--- INVERT=$invert MUST BE AN INTEGER VALUE OF 1 OR 2 ---"
					   ;;
				 -)    # STDIN and end of arguments
					   break
					   ;;
				-*)    # any other - argument
					   errMsg "--- UNKNOWN OPTION ---"
					   ;;
		     	 *)    # end of arguments
					   break
					   ;;
			esac
			shift   # next option
	done
	#
	# get infile and outfile
	infile="$1"
	outfile="$2"
fi

# test that infile provided
[ "$infile" = "" ] && errMsg "NO INPUT FILE SPECIFIED"

# test that outfile provided
[ "$outfile" = "" ] && errMsg "NO OUTPUT FILE SPECIFIED"

# get im version
im_version=`convert -list configure | \
sed '/^LIB_VERSION_NUMBER /!d;  s//,/;  s/,/,0/g;  s/,0*\([0-9][0-9]\)/\1/g' | head -n 1`

tmpA1="$dir/textcleaner_1_$$.mpc"
tmpA2="$dir/textcleaner_1_$$.cache"
trap "rm -f $tmpA1 $tmpA2 exit 0;" 0
trap "rm -f $tmpA1 $tmpA2; exit 1" 1 2 3 15
#trap "rm -f $tmpA1 $tmpA2; exit 1" ERR


# test for hdri enabled
# NOTE: must put grep before trap using ERR in case it does not find a match
if [ "$im_version" -ge "07000000" ]; then
	hdri_on=`convert -version | grep "HDRI"`	
else
	hdri_on=`convert -list configure | grep "enable-hdri"`
fi


# colorspace RGB and sRGB swapped between 6.7.5.5 and 6.7.6.7 
# though probably not resolved until the latter
# then -colorspace gray changed to linear between 6.7.6.7 and 6.7.8.2 
# then -separate converted to linear gray channels between 6.7.6.7 and 6.7.8.2,
# though probably not resolved until the latter
# so -colorspace HSL/HSB -separate and -colorspace gray became linear
# but we need to use -set colorspace RGB before using them at appropriate times
# so that results stay as in original script
# The following was determined from various version tests using textcleaner
# with IM 6.7.4.10, 6.7.6.10, 6.7.9.0
if [ "$im_version" -lt "06070607" -o "$im_version" -gt "06070707" ]; then
	setcspace="-set colorspace RGB"
else
	setcspace=""
fi
# no need for setcspace for grayscale or channels after 6.8.5.4
if [ "$im_version" -gt "06080504" ]; then
	setcspace=""
fi

if [ "$invert" != "" ]; then
	inversion1="-negate"
else
	inversion1=""
fi	

# read the input image into the TMP cached image.
convert -quiet "$infile" +repage $inversion1 "$tmpA1" ||
	errMsg "--- FILE $infile NOT READABLE OR HAS ZERO SIZE ---"

# get image size
ww=`convert $tmpA1 -ping -format "%w" info:`
hh=`convert $tmpA1 -ping -format "%h" info:`

# get image h/w aspect ratio and determine if portrait=1 (h/w>1) or landscape=0 (h/w<1)
aspect=`convert xc: -format "%[fx:($hh/$ww)>=1?1:0]" info:`
 
#echo "ww=$ww; hh=$hh; aspect=$aspect"

# set up rotation
if [ "$layout" = "portrait" -a $aspect -eq 0 -a "$rotate" = "cw" ]; then
	rotation="-rotate 90"
elif [ "$layout" = "portrait" -a $aspect -eq 0 -a "$rotate" = "ccw" ]; then
	rotation="-rotate -90"
elif [ "$layout" = "landscape" -a $aspect -eq 1 -a "$rotate" = "cw" ]; then
	rotation="-rotate 90"
elif [ "$layout" = "landscape" -a $aspect -eq 1 -a "$rotate" = "ccw" ]; then
	rotation="-rotate -90"
else
	rotation=""
fi
	
# set up cropping
if [ "$cropoff" != "" -a $numcrops -eq 1 ]; then
	wwc=`convert xc: -format "%[fx:$ww-2*$crop1]" info:`
	hhc=`convert xc: -format "%[fx:$hh-2*$crop1]" info:`
	cropping="-crop ${wwc}x${hhc}+$crop1+$crop1 +repage"
elif [ "$cropoff" != "" -a $numcrops -eq 2 ]; then
	wwc=`convert xc: -format "%[fx:$ww-2*$crop1]" info:`
	hhc=`convert xc: -format "%[fx:$hh-2*$crop2]" info:`
	cropping="-crop ${wwc}x${hhc}+$crop1+$crop2 +repage"
elif [ "$cropoff" != "" -a $numcrops -eq 4 ]; then
	wwc=`convert xc: -format "%[fx:$ww-($crop1+$crop3)]" info:`
	hhc=`convert xc: -format "%[fx:$hh-($crop2+$crop4)]" info:`
	cropping="-crop ${wwc}x${hhc}+$crop1+$crop2 +repage"
else
	cropping=""
fi
#echo "cropoff=$cropoff; numcrops=$numcrops; cropping=$cropping"

# test if grayscale
grayscale=`convert $tmpA1 -format "%[colorspace]" info:`
typegray=`convert $tmpA1 -format '%r' info: | grep 'Gray'`
if [ "$gray" = "yes" -o "$grayscale" = "Gray" -o "$typegray" != "" ]; then 
	makegray="$setcspace -colorspace gray -type grayscale"
else
	makegray=""
fi
#echo "makegray=$makegray"

# set up enhance
if [ "$enhance" = "stretch" ]; then
	enhancing="$setcspace -contrast-stretch 0"
elif [ "$enhance" = "normalize" ]; then
	enhancing="$setcspace -normalize"
else
	enhancing=""
fi
#echo "enhancing=$enhancing"

# setup blurring
if [ "$threshold" = "" ]; then
	blurring=""
else
	# note: any 0<bluramt<=1, will be the same as using bluramt=1, since radius must be used as an integer
#	bluramt=`convert xc: -format "%[fx:$threshold/100]" info:`
#	blurring="-blur ${bluramt}x65535 -level ${threshold}x100%"
	blurring="-blur 1x65535 -level ${threshold}x100%"
fi
#echo "blurring=$blurring"

# get background color
bgcolor=`echo "$bgcolor" | tr "[:upper:]" "[:lower:]"`
if [ "$bgcolor" = "image" ]; then
	bgcolor=`convert $tmpA1 -format "%[pixel:u.p{0,0}]" info:`
	fuzzval=$((100-fuzzval))
	bgcolor=`convert $tmpA1 -fuzz $fuzzval% +transparent "$bgcolor" -scale 1x1! -alpha off -format "%[pixel:u.p{0,0}]" info:`
fi
#echo "$bgcolor"

# set up unrotate
if [ "$unrotate" = "yes" ]; then
	unrotating="-background $bgcolor -deskew 40%"
else
	unrotating=""
fi
#echo "unrotating=$unrotating"

# setup sharpening
if [ "$sharpamt" = "0" -o "$sharpamt" = "0.0" ]; then
	sharpening=""
else
	sharpening="-sharpen 0x${sharpamt}"
fi
#echo "sharpening=$sharpening"

# setup modulation
[ "$gray" = "yes" -o "$grayscale" = "Gray" -o "$typegray" != "" ] && saturation=100
if [ $saturation -eq 100 ]; then
	modulation=""
else
	modulation="-modulate 100,$saturation,100"
fi
#echo "modulation=$modulation"

# set up adaptiveblurring
if [ "$adaptblur" = "0" ]; then
	adaptiveblurring=""
else
	adaptiveblurring="-adaptive-blur $adaptblur"
fi

# set up trim
if [ "$trim" = "yes" -a "$hdri_on" != "" ]; then
	# hdri is enabled
	# need to round near white to pure white for trim to work
	trimming="-white-threshold 99.9% -trim +repage "
elif [ "$trim" = "yes" -a "$hdri_on" = "" ]; then
	# hdri is not enabled
	trimming="-trim +repage "
else
	trimming=""
fi
#echo "trimming=$trimming"

# set up pad
if [ $padamt -gt 0 ]; then
	# note must reset -compose from -compose copy_opacity as -border uses -compose
	padding="-compose over -bordercolor $bgcolor -border $padamt"
else
	padding=""
fi
#echo "padding=$padding"

if [ "$invert" = 2 ]; then
	inversion2="-negate"
else
	inversion2=""
fi	

# process image
convert -respect-parenthesis \( $tmpA1 $rotation $cropping $makegray $enhancing \) \
	\( -clone 0  $setcspace -colorspace gray -negate -lat ${filtersize}x${filtersize}+${offset}% -contrast-stretch 0 $blurring \) \
	-compose copy_opacity -composite -fill "$bgcolor" -opaque none -alpha off \
	$unrotating $sharpening $modulation $adaptiveblurring $trimming $padding $inversion2 \
	"$outfile"
exit 0
