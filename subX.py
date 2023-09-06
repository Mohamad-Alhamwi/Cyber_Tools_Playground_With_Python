#!/usr/bin/python3

import requests 
import sys
import time

# A function to print out errors.
def throw_error(error_num, further_info=None,  additional_info=None): 

    # TODO: Senitize the value of further_info.

    error_message = {
        1: "[\033[35mError\033[0m] Usage: ./script.py [SUBDOMAINS_LIST_PATH] [TARGET_URL].",
        2: f"[\033[35mError\033[0m] No such file: {further_info}.",
        3: "[\033[35mError\033[0m] You need to type in the full URL like: http(s)://example.com.",
        4: f"[\033[35mError\033[0m] Problem establishing a network connection to {further_info}.",
        5: f"[\033[34mInformational\033[0m] The server being accessed ({further_info}) is slow to respond.\n\033[34m...............\033[0m Timed out after waiting for \033[34m{additional_info}\033[0m seconds.",
    }

    print (error_message[error_num])

# A function to find a substring of a given string and insert some string after it.
def insert_after(source, target, insert_string):
    index = source.find(target)
    
    if index != -1:
        new_string = source[:index + len(target)] + insert_string + '.' + source[index + len(target):]
        return new_string
    
    else:
        throw_error(3)
        sys.exit(1)

# A function to make requests.
def make_request(url, initial_timeout, max_retries):
    retries = 0
    
    while retries < max_retries:
        try:
            # Sending get request and saving the response as response object.
            response = requests.get(url, timeout=initial_timeout)

            status_code = response.status_code

            status_code_message = {
                200: "[\033[32mSuccessful\033[0m]",
                300: "[\033[33mRedirection\033[0m]",
                400: "[\033[30mClient Error\033[0m]",
                500: "[\033[31mServer Error\033[0m]",
            }

            if 200 <= status_code < 300:
                print(f"{status_code_message[200]} {status_code} {url}")
            elif 300 <= status_code < 400:
                print(f"{status_code_message[300]} {status_code} {url}")
            elif 400 <= status_code < 500:
                print(f"{status_code_message[400]} {status_code} {url}")
            elif 500 <= status_code < 600:
                print(f"{status_code_message[500]} {status_code} {url} \033[31m TCP connection to the web server could not be established. It could get blocked which is an indicator of a firewall in place.\033[0m")
            
            # Request was successful, exit the loop.
            return

        except requests.ConnectionError:
            throw_error(4, url)
            # Exit the loop on a ConnectionError.
            return

        except requests.Timeout:
            throw_error(5, url, initial_timeout)

            # Increment the retries counter.
            retries += 1

            # Increment the timeout.
            initial_timeout += 5
            
            # Add a small delay before retrying.
            time.sleep(1)

        # TODO Handle other exceptions as needed.

    # If we reach this point, max_retries were reached without success.
    print(f"\033[34m...............\033[0m Reached maximum retry attempts \033[34m({max_retries})\033[0m for {url}.")

# The main block of code goes here.
def main():
    # Check the arguments number.
    if len(sys.argv) < 3:
        throw_error(1)
        sys.exit(1)

    # Path to the subdomains list.
    list_path = sys.argv[1]

    try:
        with open(list_path, "r") as file:
            # The subdomains list content.
            subdomain_list = file.read()

    except FileNotFoundError:
        throw_error(2, list_path)
        sys.exit(1)

    # All the subdomains in the file.
    subdomins = subdomain_list.splitlines()

    # Iterete through all the subdomains.
    for subdomain in subdomins:
        # Construct a full url.
        full_url = insert_after(sys.argv[2], "://", subdomain)
            
        # Initialize with a short timeout.
        initial_timeout = 5
        # Maximum number of retries
        max_retries = 5

        # Make a request.
        make_request(full_url, initial_timeout, max_retries)

if __name__ == "__main__":
    main()