import glob
import os
import pathlib

found_ciphers = []


def find_tls_in_script(file, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    occurrences = 0
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file, 'r') as read_obj:
        # Read all lines in the file one by one

        for line in read_obj:
            # For each line, check if line contains the string

            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                text = line.rstrip()
                if format_text(text) not in found_ciphers:
                    occurrences = 1
                    found_ciphers.append((occurrences, format_text(text)))
                if format_text(text) in found_ciphers:
                    print("Already added")
            else:
                print("Nothing found")
                list_of_results.append((line_number, text))
    # Return list of tuples containing line numbers and lines where string is found


def format_text(text):
    first_a = text.replace(" ", "", 9)
    return first_a


os.chdir(pathlib.Path(__file__).parent.absolute())
for file in glob.glob("*.txt"):
    find_tls_in_script(file, 'TLS_')

for cipher in found_ciphers:
    print(cipher)
