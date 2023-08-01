#!/usr/bin/env python

import subprocess
import os
import pdf2txt
from py_dotenv import read_dotenv
from algoliasearch.search_client import SearchClient

file_counter = 0

def next_obj_id():
    global file_counter
    file_counter = file_counter + 1
    return file_counter

def publish_file(f):
    command = ["docker-compose", "exec", "-it", "ipfs", "ipfs", "add", "-r", "/export/" + f]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error executing command: {result.stderr}")
    else:
        return result.stdout.split(' ')[1]

def ocr_file(file_name):
    try:
        doc = pdf2txt.PdfDocument('./data/export/' + file_name)
        return ''.join(doc.paragraphs)
    except:
        pass

def index_file(index, file_name, ipfs_hash, text_content):
    if not file_name:
        return
    if not ipfs_hash:
        return
    if not text_content:
        return

    print(ipfs_hash)

    index.save_object({
        'file_name': file_name,
        'ipfs_hash': ipfs_hash,
        'text_content': text_content[:999],
        'objectID': next_obj_id()
        }
    )

def list_files(directory_path, search_index):
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist")
        return

    # Ensure the path is a directory
    if not os.path.isdir(directory_path):
        print(f"The path {directory_path} is not a directory")
        return

    # Loop over all files in the directory
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)

        # Only print the path if it's a file
        if os.path.isfile(file_path):
            ipfs_hash = publish_file(file_name)
            text_content = ocr_file(file_name)
            index_file(search_index, file_name, ipfs_hash, text_content)

def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    read_dotenv(dotenv_path)

    client = SearchClient.create(os.getenv('ALGOLIA_CLIENT_ID'), os.getenv('ALGOLIA_CLIENT_SECRET'))
    index = client.init_index('pdf')

    list_files("./data/export", index)

if __name__ == "__main__":
    main()
