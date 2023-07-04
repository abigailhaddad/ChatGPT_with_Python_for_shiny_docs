import requests
import os
import re
import time

def load_github_token(path):
    with open(path, "r") as token_file:
        return token_file.read().strip()

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

def fetch_files_from_directory(repositories, output_folder="../data"):
    # Ensure output folder exists
    github_token = load_github_token("../key/github_token.txt")
    headers = {'Authorization': f'token {github_token}'}
    os.makedirs(output_folder, exist_ok=True)

    for repo in repositories:
        # Send a request to the GitHub API
        response = requests.get(f'https://api.github.com/repos/{repo}/contents', headers=headers)
        response.raise_for_status()  # ensure we notice bad responses

        for item in response.json():
            if item['type'] == 'file' and (item['name'].endswith('.qmd') or item['name'].endswith('.py')):
                # Download file
                file_content = requests.get(item['download_url']).text

                # Write file to disk
                filename = os.path.join(output_folder, item['name'].replace('.qmd', '.txt').replace('.py', '.txt'))
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(file_content)

            elif item['type'] == 'dir':
                # Recursively call for directories
                fetch_files_from_directory_in_subfolder(item['path'], output_folder, repo)

        # Clean and move files to main output folder
        flatten_directory_structure(output_folder, output_folder)

        # Remove empty folders
        remove_empty_folders(output_folder)

def fetch_files_from_directory_in_subfolder(path, output_folder, repo):
    github_token = load_github_token("../key/github_token.txt")
    headers = {'Authorization': f'token {github_token}'}
    # Send a request to the GitHub API
    response = requests.get(f'https://api.github.com/repos/{repo}/contents/{path}', headers=headers)
    response.raise_for_status()  # ensure we notice bad responses

    for item in response.json():
        if item['type'] == 'file' and (item['name'].endswith('.qmd') or item['name'].endswith('.py')):
            # Download file
            file_content = requests.get(item['download_url']).text

            # Write file to disk
            filename = os.path.join(output_folder, item['name'].replace('.qmd', '.txt').replace('.py', '.txt'))
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(file_content)

        elif item['type'] == 'dir':
            # Recursively call for directories
            fetch_files_from_directory_in_subfolder(item['path'], output_folder, repo)

# Start fetching files

# List of GitHub repositories to pull from (recursive - gets subfolders)
repositories = ['rstudio/py-shiny-docs', 'rstudio/py-shiny']
fetch_files_from_directory(repositories)
