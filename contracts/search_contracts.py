import os
import pandas as pd
import hashlib

def search_files(directory, extensions):
    matches = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in extensions):
                matches.append(os.path.join(root, filename))
    return matches

def file_hash(filepath):
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

def update_files_uniques(files):
    unique_files = {}
    for file in files:
        base_name = os.path.basename(file)
        file_hash_value = file_hash(file)
        if base_name in unique_files:
            if unique_files[base_name] == file_hash_value:
                continue
        unique_files[base_name] = file_hash_value

    files = [file for file in files if os.path.basename(file) in unique_files and unique_files.pop(os.path.basename(file), None) is not None]
    return files

if __name__ == "__main__":
    # directory = input("Enter the directory to search: ")
    directory = r"C:\JYN\2024-08-06"
    extensions = ['.xlsx', '.xls', '.pdf']
    files = search_files(directory, extensions)

    unique_files = update_files_uniques(files)
    
    # Create a DataFrame from the list of files
    df = pd.DataFrame(unique_files, columns=['file_path'])

    # Split the file path to get the file name
    df['file_name'] = df['file_path'].apply(lambda x: os.path.basename(x))

    # Save the DataFrame to an Excel file
    output_file = r"C:\JYN\unique_files.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Data has been written to {output_file}")