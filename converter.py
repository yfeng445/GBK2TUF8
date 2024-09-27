import os

def check_encoding(data, encoding):
    """Check if the data can be decoded using a specific encoding."""
    try:
        data.decode(encoding)
        return True
    except UnicodeDecodeError:
        return False

def detect_and_convert_file_encoding(file_path):
    """Detects if a file is GBK encoded and converts it to UTF-8 if necessary."""
    
    # Open the file as binary to check encoding
    with open(file_path, 'rb') as f:
        data = f.read()

    # Check if the content is in GBK encoding
    is_gbk = check_encoding(data, 'gbk')

    if is_gbk:
        print(f"File content '{file_path}' is GBK encoded. Converting to UTF-8...")
        # Convert the content from GBK to UTF-8
        content = data.decode('gbk')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"File content '{file_path}' has been converted to UTF-8.")
    else:
        print(f"File content '{file_path}' is not GBK encoded.")

def rename_if_gbk_encoded(filename):
    """Detect if the filename itself is GBK encoded and rename to UTF-8."""
    try:
        # Try decoding the filename as UTF-8; if it fails, it could be GBK
        filename.encode('utf-8')
    except UnicodeEncodeError:
        # If it's not valid UTF-8, it might be GBK, so attempt to decode it
        try:
            # Decode filename from GBK and re-encode it as UTF-8
            new_filename = filename.encode('latin1').decode('gbk')
            print(f"Renaming file from '{filename}' to '{new_filename}'...")
            os.rename(filename, new_filename)
            return new_filename
        except (UnicodeDecodeError, UnicodeEncodeError):
            print(f"Filename '{filename}' is not in GBK.")
            return filename

    return filename

def process_files_in_folder(folder_path):
    """Detect and convert all GBK files and filenames in a folder."""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                # Rename file if the filename is GBK encoded
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, rename_if_gbk_encoded(file))
                
                # Convert file content if needed
                detect_and_convert_file_encoding(new_file_path)

# Usage example
folder_path = './.'  # Replace with your folder path
process_files_in_folder(folder_path)
input("\nConversion complete.")
