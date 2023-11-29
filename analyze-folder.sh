#!/bin/bash

# Usage : bash script-analyze.sh TA/2019

echo "Analyse of year $1"
echo "Number of files"
ls -1 $1 |wc -l
echo "Files that don't mention digitalization"
pdfgrep -L --with-filename --color always 'digitalization' $1/*.pdf | wc -l

echo "Files that don't mention artificial intelligence"
pdfgrep -L --with-filename --color always 'artificial intelligence' $1/*.pdf | wc -l

pdfgrep -iHnr --with-filename --color always 'digitaliz'  

