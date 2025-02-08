import re as regex
import time
import random


def encrypt_strings(code: str):
    """Encrypts strings in code"""

    # find all strings
    strings = regex.findall(r"[\"'].*[\"']", code)
    fstrings = regex.findall(r"f[\"'].*[\"']", code)

    encrypted_strings = {}

    for fstring in fstrings:
        # Split fstring into separate strings, excluding parts within curly braces

        fstring_content = fstring[2:-1]
        parts = regex.split(r"{.*}", fstring_content)

        for part in parts:
            if part.strip() == "":
                continue

            part_id = f"part_{time.time_ns()}_{random.randint(0, 1000000)}"

            encrypted_strings[part_id] = part
            code = code.replace(part, part_id)

    for string in strings:
        string_content = string[1:-1]
        string_id = f"str_{time.time_ns()}_{random.randint(0, 1000000)}"

        encrypted_strings[string_id] = string_content
        code = code.replace(string_content, string_id)

    return code, encrypted_strings


def decrypt_strings(code: str, encrypted_strings: dict):
    """Decrypts strings in code"""

    # Reinsert curly braces
    fstring_ids = [id_ for id_ in encrypted_strings.keys() if id_.startswith("part_")]
    for fstring_id in fstring_ids:
        expressions = regex.findall(r"{(.*?)}", encrypted_strings[fstring_id])
        for expr in expressions:
            code = code.replace(
                fstring_id,
                fstring_id.replace(encrypted_strings[fstring_id], "{" + expr + "}"),
            )

    for string_id, original_string in encrypted_strings.items():
        code = code.replace(string_id, original_string)

    return code
