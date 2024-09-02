import os

'''
    Used when using assistance from generative AI.
'''

# Define the directories to exclude and the file extensions to include
excluded_dirs = {'.venv', 'venv', 'structure_print', '__pycache__', '.git', 'git'}
included_extensions = {'.py', '.txt', '.html', '.js', '.json', '.yml', '.yaml'}

# The name of the output file
output_filename = 'directory_structure_and_contents.txt'

excluded_files = [output_filename, "LICENSE", "requirements.txt", ".gitignore", ".gitattributes"]

# Set to track processed files
processed_files = set()

def is_included_file(file_name):
    # Check if the file has one of the allowed extensions and is not in excluded_files
    return file_name not in excluded_files and any(file_name.endswith(ext) for ext in included_extensions)

def write_file_content(file_path, output_file):
    # Write the name and content of the file to the output file
    output_file.write(f"\nFile: {file_path}\n")
    output_file.write(f"{'-'*len(f'File: {file_path}')}\n")
    with open(file_path, 'r', encoding='utf-8') as f:
        output_file.write(f.read() + '\n\n')

def traverse_directory(directory, output_file):
    # Traverse the directory structure
    for root, dirs, files in os.walk(directory):
        # Skip the excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        # Write the directory path as a heading
        output_file.write(f"\nDirectory: {root}\n")
        output_file.write(f"{'='*len(f'Directory: {root}')}\n")
        
        for file in files:
            file_path = os.path.join(root, file)
            # Check if the file is in excluded_files
            if file in excluded_files:
                # Write only the file name
                output_file.write(f"\nFile: {file_path}\n")
                output_file.write(f"{'-'*len(f'File: {file_path}')}\n\n")
            elif is_included_file(file):
                # Check if the file has already been processed
                if file_path not in processed_files:
                    write_file_content(file_path, output_file)
                    # Mark the file as processed
                    processed_files.add(file_path)

# Run the script
with open(output_filename, 'w', encoding='utf-8') as output_file:
    traverse_directory('.', output_file)

print(f"Directory structure and contents have been saved to '{output_filename}'.")