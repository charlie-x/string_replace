import sys
from pathlib import Path

def replace_string_in_file(file_path, search_string, replacement_string):
    # encode strings as bytes
    search_bytes = search_string.encode()
    
    # encoding of the replacement string
    replacement_bytes = replacement_string.encode()

    # check if the replacement string is longer than the search string
    if len(replacement_bytes) + 1 > len(search_bytes):  # +1 for null terminator
        print(f"Error: The replacement string '{replacement_string}' (with null terminator) is longer than the search string '{search_string}'.")
        return False

    # pad the replacement string with null bytes if it's shorter than the search string
    # ensure the total length matches the search string length, accounting for the null terminator
    if len(replacement_bytes) < len(search_bytes):
        padding_length = len(search_bytes) - len(replacement_bytes) - 1  # -1 to account for the null terminator
        replacement_bytes += b'\0' + b'\0' * padding_length
    else:
        # add only one null terminator if lengths are equal or padding isn't needed
        replacement_bytes += b'\0'

    # read the original binary data
    with open(file_path, "rb") as file:
        binary_data = file.read()

    # check if the search string exists in the binary data
    if search_bytes not in binary_data:
        print(f"Error: The string '{search_string}' was not found in {file_path}.")
        return False

    # replace the search bytes with replacement bytes in the binary data
    modified_data = binary_data.replace(search_bytes, replacement_bytes, 1)  # limit to one replacement

    # if no replacement occurred, return False
    if modified_data == binary_data:
        print(f"Error: No replacements made for '{search_string}' in {file_path}.")
        return False

    # write the modified binary data back to the file
    with open(file_path, "wb") as file:
        file.write(modified_data)

    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python modify_binary.py <file_path> <search_string> <replacement_string>")
        sys.exit(1)

    file_path = sys.argv[1]
    search_string = sys.argv[2]
    replacement_string = sys.argv[3]

    # validate that the file exists
    if not Path(file_path).is_file():
        print(f"Error: The file {file_path} does not exist.")
        sys.exit(1)

    # perform the replacement
    if not replace_string_in_file(file_path, search_string, replacement_string):
        sys.exit(1)  # exit with an error code
