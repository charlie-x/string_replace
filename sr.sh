#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 strings_file original_hex_file string_to_replace"
    exit 1
fi

stringsFile=$1
originalHexFile=$2
stringToReplace=$3

# check if the strings file exists
if [ ! -f "$stringsFile" ]; then
    echo "Strings file does not exist."
    exit 1
fi

# check if the original hex file exists
if [ ! -f "$originalHexFile" ]; then
    echo "Original hex file does not exist."
    exit 1
fi

# ensure the output directory exists
outputDir="./out"
mkdir -p "$outputDir"

# convert hex to bin, modify bin, and convert back to hex
process_hex_file() {
    local originalHex=$1
    local string=$2

    # convert hex to bin
    local tempBin=$(mktemp --suffix=.bin)
    objcopy -I ihex -O binary "$originalHex" "$tempBin"

    # modify the bin file with the string (terminated by a null character in the modification process)
    python modify_binary.py "$tempBin" "$stringToReplace" "$line"

    # Check the exit status of the Python script
    if [ $? -ne 0 ]; then
        echo "Modification failed for $line. Skipping."
        continue  # Skip the rest of the loop for this iteration
    fi

    # convert the modified bin back to hex
    local baseName=$(basename "$originalHex")
    local modifiedHex="${outputDir}/${baseName%.hex}_${string}.hex"
    objcopy -I binary -O ihex "$tempBin" "$modifiedHex"

    echo "generated new hex file: $modifiedHex"
}

# read each line from the strings file and process the hex file
while IFS= read -r line
do
    # skip blank lines
    [[ -z "$line" ]] && continue
    
    # process the hex file with the current line (without adding a null character to the command)
    process_hex_file "$originalHexFile" "$line"
done < "$stringsFile"
