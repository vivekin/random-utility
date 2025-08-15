#!/bin/bash

# Usage: ./list_file_types.sh /path/to/directory

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

dir="$1"

echo "📂 File types in: $dir"
echo "-----------------------------------"

# Find files, extract extensions, lowercase, unique
find "$dir" -type f \
    | sed -n 's/.*\.//p' \
    | tr '[:upper:]' '[:lower:]' \
    | sort -u

