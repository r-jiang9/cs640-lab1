import random

def split_file_random_points(input_file, num_parts):
    # Read the content of the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Strip newline characters from each line
    lines = [line.rstrip('\n') for line in lines]

    # Get the total number of lines
    total_lines = len(lines)

    # Generate random split points (excluding the first and last line)
    split_points = sorted(random.sample(range(1, total_lines), num_parts - 1))
    
    # Add the start (0) and end (total_lines) to the split points
    split_points = [0] + split_points + [total_lines]

    # Split and write the content into different files
    for i in range(1, num_parts + 1):
        start = split_points[i - 1]
        end = split_points[i]
        
        output_file = f'large{i}.txt'
        with open(output_file, 'w') as outfile:
            # Write lines without adding extra newlines
            outfile.write('\n'.join(lines[start:end]))  # Ensure the last line has a newline

# Call the function
split_file_random_points('original.txt', 10)