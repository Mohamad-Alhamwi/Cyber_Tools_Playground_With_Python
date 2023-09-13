#!/usr/bin/python3

from readline import append_history_file
import requests 
import sys

# A function to print out errors.
def throw_error(error_num, further_info=None): 

    # TODO: Senitize the value of further_info.

    error_message = {
        1: "[\033[35mError\033[0m] Usage: ./script.py http(s)://example.com [DIRECTORY_LIST]",
        2: f"[\033[35mError\033[0m] No such file: {further_info}",
        3: f"[\033[35mError\033[0m] Incomplete URL: \033[35m{further_info}\033[0m, you need to supply \033[35mhttp://\033[0m or \033[35mhttps://\033[0m to the URL",
        4: f"[\033[35mError\033[0m] Problem establishing a network connection to \033[35m{further_info}\033[0m",
    }

    print (error_message[error_num])

# A function to append a string to other string. 
def append_string(str1, str2):
    return str1 + str2

# A function to make requests.
def make_request(url):

    try:
        # Sending get request and saving the response as response object.
        response = requests.get(url, timeout=5)

        status_code = response.status_code

        if 404 == status_code:
            print(f"[\033[31mNot Found\033[0m] {status_code} {url}")
        else:
            print(f"[\033[32mFound\033[0m] {status_code} {url}")
    
    except requests.exceptions.MissingSchema:
        throw_error(3, url)
        sys.exit(1)

    except requests.ConnectionError:
        throw_error(4, url)

    # TODO Handle other exceptions as needed.

# The main block of code goes here.
def main():
    # Check the arguments number.
    if len(sys.argv) < 3:
        throw_error(1)
        sys.exit(1)

    # Path to the directory list.
    list_path = sys.argv[2]

    try:
        with open(list_path, "r") as file:
            # The directory list content.
            directory_list = file.read()

    except FileNotFoundError:
        throw_error(2, list_path)
        sys.exit(1)

    # All the Directories in the file.
    directories = directory_list.splitlines()

    url = sys.argv[1]
    if url[-1] != '/':
        url = append_string(url, '/')

    # Iterete through all the directories.
    for directory in directories:
        
        # Construct a full url.
        full_url = append_string(url, directory)

        full_url = append_string(full_url, ".html")
        
        # Make a request.
        make_request(full_url)

if __name__ == "__main__":
    main()