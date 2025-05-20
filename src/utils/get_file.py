"""
Retrieves the contents of a file from a given location.

Args:
    location (str): The location of the file to retrieve.

Returns:
    str: The contents of the file.
"""
def get_file(location: str) -> str:
    with open(location, 'r') as file:
        return file.read().strip()
