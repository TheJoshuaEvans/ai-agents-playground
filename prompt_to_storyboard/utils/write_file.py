"""
Write a file to the specified location.

Args:
    location (str): The location of the file to write.
    contents (str): The contents to write to the file.
"""
def write_file(location: str, contents: str) -> None:
    with open(location, 'w') as file:
        file.write(contents.strip())
