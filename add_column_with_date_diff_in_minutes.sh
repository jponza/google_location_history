#!/bin/bash
read line < input
echo -n $line; echo ",No_Of_Hours";
sed '1d' input| 
    while IFS=,
        read a b c d e f g;
    do 
        #echo -n "${g} - ${f}: "
        #echo (`date +%s -d $g` - `date +%s -d $f`)/86400;

        # get DIFF in seconds
        let DIFF=$[ (`date +%s -d $g` - `date +%s -d $f`)/60 ];


        #echo "${DIFF} minutes"
        echo $a,$b,$c,$d,$e,$f,$g,$DIFF
        
    done  

