import sys
from enum import Enum
import glob
import os
import hashlib
import shutil

class FileType(Enum):
    SOURCE_CODE = "source-code"
    HTML = "html"
    IMAGES = "images"
    DOCUMENTS = "documents"
    OTHERS = "others"

# Mapping of file types to their extensions
FILE_TYPE_EXTENSIONS = {
    FileType.SOURCE_CODE: ['*.py', '*.java', '*.cpp', '*.js'],
    FileType.HTML: ['*.html', '*.htm'],
    FileType.IMAGES: ['*.jpg', '*.jpeg', '*.png', '*.gif'],
    FileType.DOCUMENTS: ['*.txt', '*.pdf', '*.docx'],
    FileType.OTHERS: []  # This can be tailored based on requirements
}

def count_files(file_type):
    file_count = 0
    extensions = FILE_TYPE_EXTENSIONS[file_type]

    if file_type == FileType.OTHERS:
        # Count files that are not in any of the defined categories
        all_files = glob.glob('*')
        categorized_files = [item for sublist in FILE_TYPE_EXTENSIONS.values() for item in sublist]
        file_count = len([file for file in all_files if not any(file.endswith(ext) for ext in categorized_files)])
    else:
        for ext in extensions:
            file_count += len(glob.glob(ext))

    return f"Counted {file_count} files of type: {file_type.value}"

def calculate_sha1(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            sha1_hash = hashlib.sha1(file_data).hexdigest()
            return f"SHA1 for {file_path}: {sha1_hash}"
    except FileNotFoundError:
        return f"File not found: {file_path}"

def verify_sha1(file_path, expected_hash):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            sha1_hash = hashlib.sha1(file_data).hexdigest()
            if sha1_hash == expected_hash:
                return f"SHA1 hash matches for {file_path}"
            else:
                return f"Mismatch: Expected {expected_hash}, found {sha1_hash}"
    except FileNotFoundError:
        return f"File not found: {file_path}"
        
def show_free_space():
    total, used, free = shutil.disk_usage("/")
    total_gb = total // (2**30)
    used_gb = used // (2**30)
    free_gb = free // (2**30)
    return f"Disk space - Total: {total_gb} GB, Used: {used_gb} GB, Free: {free_gb} GB"

def process_command(args):
    match args:
        case ["count", (FileType.SOURCE_CODE.value | FileType.HTML.value | FileType.IMAGES.value | FileType.DOCUMENTS.value | FileType.OTHERS.value) as file_type]:
            return count_files(FileType(file_type))
        
        case ["count", _, *_]:
            return "Error: 'count' command requires exactly one file type argument"

        case ["sha1", "verify"] | ["sha1", "verify", _, _, _, *_]:
            return "Error: 'verify-sha1' command requires exactly two arguments (file path and expected hash)"
        
        case ["sha1", "verify", file_path, expected_hash]:
            return verify_sha1(file_path, expected_hash)

        case ["sha1", *file_paths] if file_paths:
            return [calculate_sha1(path) for path in file_paths]        
        
        case ["sha1"]:
            return "Error: 'sha1' command requires at least one file path"

        case ["free-space"]:
            return show_free_space()
        
        case ["free-space", *_]:
            return "Error: 'free-space' command does not require any additional arguments"

        case _:
            return "Unknown command"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command_output = process_command(sys.argv[1:])
        print(command_output)
    else:
        print("No command provided. Use 'help' for command list.")
