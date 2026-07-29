def decode_insta_text(text: str) -> str:
    """
    Instagram export JSONs encode UTF-8 characters as Latin-1 strings.
    This function converts double-encoded latin-1 back to proper UTF-8 strings.
    """
    if not isinstance(text, str) or not text:
        return ""
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text

def decode_obj(obj):
    """Recursively decode string values in dicts and lists."""
    if isinstance(obj, str):
        return decode_insta_text(obj)
    elif isinstance(obj, list):
        return [decode_obj(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: decode_obj(val) for key, val in obj.items()}
    return obj
