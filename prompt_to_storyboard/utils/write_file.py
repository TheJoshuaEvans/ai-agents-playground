def write_file(location: str, contents: str) -> None:
    """
    Write a file to the specified location.

    Args:
        location: The location of the file to write.
        contents: The contents to write to the file.
    """
    with open(location, 'w') as file:
        file.write(contents.strip())
