from re import Pattern

def match_any(regex_list: list[Pattern], string: str) -> bool:
    """
    Match any regex pattern in a list.

    Args:
        regex_list (list[Pattern]): List of compiled regex patterns.
        string (str): String to match against the regex patterns.
    """
    return any(regex.match(string) for regex in regex_list)