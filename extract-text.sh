
#!/bin/bash
# Usage:
#  bash extract-text.sh > output/extracts.md
# Loops through folders

word="digital"

for folder in ./TA/*; do
  if [ -d "$folder" ]; then
    echo "## $folder ($(ls -1 $folder |wc -l) reports):"
    # Loop through files within each folder
    for file in "$folder"/*; do
      if [ -f "$file" ]; then
        # echo "Processing file: $file"
				# i ignore case, H print filename, n page number
        pdfgrep -in $word $file && echo "[From $(pdfinfo $file | head -n 1)]"
        # pdfgrep -iHn --with-filename --color always 'digitaliz' $file && pdfinfo $file | head -n 1
        
      fi
    done
    
  fi
done
