def get_file(location: str) -> str:
    """
    Retrieves the contents of a file from a given location.

    Args:
        location: The location of the file to retrieve.

    Returns:
        The contents of the file.
    """
    with open(location, 'r') as file:
        return file.read().strip()
