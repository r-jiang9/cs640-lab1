#!/bin/bash

# Check if the directory path is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_test_file_directory>"
    exit 1
fi

# Set the directory path from the argument
test_dir="$1"

# Check if the provided directory exists
if [ ! -d "$test_dir" ]; then
    echo "Directory $test_dir does not exist."
    echo "Current working directory: $PWD"
    exit 1
fi

# Delete all sender directories (sender1, sender2, ..., sender[i])
for dir in sender*; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "Deleted directory: $dir"
    fi
done

cp "requester.py" "./requester"
# Copy tracker.txt to the ./requester directory
if [ -f "$test_dir/tracker.txt" ]; then
    cp "$test_dir/tracker.txt" "./requester/"
    echo "Copied tracker.txt to ./requester"
else
    echo "tracker.txt not found in $test_dir."
    exit 1
fi

# Initialize a counter for the split files
i=1

# Copy split[i].txt files to the corresponding sender[i] directories
while true; do
    split_file="$test_dir/split${i}.txt"
    if [ ! -f "$split_file" ]; then
        break
    fi

    # Create the sender[i] directory
    sender_dir="sender${i}"
    mkdir "$sender_dir"

    # Copy the split file to the sender[i] directory
    cp "$split_file" "$sender_dir/"
    echo "Copied $split_file to $sender_dir/"

    # Copy sender.py to the sender[i] directory
    cp "./sender.py" "$sender_dir/"
    echo "Copied sender.py to $sender_dir/"

    # Increment the counter
    ((i++))
done

echo "Setup completed."