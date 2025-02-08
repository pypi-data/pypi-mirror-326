import re


def eirify(string: str) -> str:
    """Corrects Irish names.

    Args:
        string: A name.

    Returns:
        A corrected name.

    Examples:
        >>> eirify("o'brian")
        "O'Brian"
        >>> eirify("o'Brian")
        "O'Brian"
        >>> eirify("O'brian")
        "O'Brian"
        >>> eirify("o' brian")
        "O'Brian"

    """
    return (
        re.sub(r"(o\s*')(\s*)", r"o' ", string, flags=re.IGNORECASE)
        .title()
        .replace("O' ", "O'")
    )


def scotify(string: str) -> str:
    """Corrects Scottish names.

    Args:
        string: A name.

    Returns:
        A corrected name.

    Examples:
        >>> scotify("mcgregor")
        "McGregor"
        >>> scotify("macgregor")
        "MacGregor"
        >>> scotify("mc gregor")
        "McGregor"
        >>> scotify("mac gregor")
        "MacGregor"

    """
    return (
        re.sub(r"(m(?:a*)c)(\s*)", r"\1 ", string, flags=re.IGNORECASE)
        .title()
        .replace("Mac ", "Mac")
        .replace("Mc ", "Mc")
    )
