#!/bin/bash

# touch tree.sh
# sudo chmod 777 tree.sh
# vi tree.sh

# Check if path and depth are provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <directory_path> <max_depth>"
    exit 1
fi

DIR="$1"
MAX_DEPTH="$2"

# Function to print the tree
print_tree() {
    local dir="$1"
    local prefix="$2"
    local depth="$3"

    # Stop if current depth exceeds max depth
    if [ "$depth" -gt "$MAX_DEPTH" ]; then
        return
    fi

    local entries=("$dir"/*)
    local count=${#entries[@]}
    local i=1

    for entry in "${entries[@]}"; do
        local name="$(basename "$entry")"
        if [ -d "$entry" ]; then
            if [ $i -eq $count ]; then
                echo "${prefix}└── $name"
                print_tree "$entry" "${prefix}    " $((depth + 1))
            else
                echo "${prefix}├── $name"
                print_tree "$entry" "${prefix}│   " $((depth + 1))
            fi
        fi
        ((i++))
    done
}

echo "$DIR"
print_tree "$DIR" "" 1
