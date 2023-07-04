import requests
import os
import re
import shutil

def remove_svg_and_png_tags(text):
    cleaned_text = re.sub(r'<svg.*?</svg>', '', text, flags=re.DOTALL)
    cleaned_text = re.sub(r'!\[.*?\.png\]\(.*?\)', '', cleaned_text, flags=re.DOTALL)
    return cleaned_text

def flatten_directory_structure(root_folder, output_folder):
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith('.txt'):
                old_filepath = os.path.join(foldername, filename)
                new_filepath = os.path.join(output_folder, filename)

                with open(old_filepath, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                cleaned_content = remove_svg_and_png_tags(file_content)

                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)

                if old_filepath != new_filepath:
                    os.remove(old_filepath)

def remove_empty_folders(root_folder):
    for foldername, subfolders, filenames in os.walk(root_folder, topdown=False):
        if not os.listdir(foldername) and foldername != root_folder:
            os.rmdir(foldername)

def fetch_files_from_directory(path, output_folder="../data"):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Send a request to the GitHub API
    response = requests.get(f'https://api.github.com/repos/rstudio/py-shiny-docs/contents/{path}')
    response.raise_for_status()  # ensure we notice bad responses

    for item in response.json():
        if item['type'] == 'file' and item['name'].endswith('.qmd'):
            # Download file
            file_content = requests.get(item['download_url']).text

            # Write file to disk
            filename = os.path.join(output_folder, item['name'].replace('.qmd', '.txt'))
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(file_content)


        elif item['type'] == 'dir':
            # Create new output folder for subdirectory
            new_output_folder = os.path.join(output_folder, item['name'])
            fetch_files_from_directory(item['path'], output_folder=new_output_folder)  # recursive call for directories

    # Clean and move files to main output folder
    flatten_directory_structure(output_folder, output_folder)

    # Remove empty folders
    remove_empty_folders(output_folder)

# Start fetching files
fetch_files_from_directory('docs')
