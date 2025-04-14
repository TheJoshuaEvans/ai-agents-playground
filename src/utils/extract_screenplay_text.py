def extract_screenplay_text(text):
    start_marker = "==="
    end_marker = "==="

    # Find the start and end indices
    start_index = text.find(start_marker)
    end_index = text.rfind(end_marker)

    # Extract the screenplay text if both markers are found
    if start_index != -1 and end_index != -1 and start_index < end_index:
        return text[start_index + len(start_marker):end_index].strip()

    return ""
