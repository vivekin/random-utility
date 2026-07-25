#!/bin/bash

# Usage: ./tree_count.sh /path/to/directory

print_tree() {
    local dir="$1"
    local prefix="$2"

    # Count files directly inside this directory (not recursive)
    local file_count
    file_count=$(find "$dir" -maxdepth 1 -type f | wc -l)

    # Print directory name and file count
    echo "${prefix}📂 $(basename "$dir") ($file_count files)"

    # Iterate over subdirectories
    local subdir
    for subdir in "$dir"/*/; do
        if [ -d "$subdir" ]; then
            print_tree "$subdir" "    $prefix"
        fi
    done
}

# Check if directory is given
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

print_tree "$1" ""

