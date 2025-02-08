import re as regex

definition_regex = r"\b(fn)\s+(\w+\s*\()"
lambda_regex = r"fn\s*([^->]*)->"
up_one_regex = r"(\w+)\s?\+\+"
down_one_regex = r"(\w+)\s?\-\-"
not_equal_regex = r"<>"

range_function_regex_two_groups = regex.compile(r"(\w+)\.\.(\w+)")
range_function_regex_one_group = regex.compile(r"\.\.(\w+)")
range_function_regex_infinite = regex.compile(r"(\w+)\.\.")

entry_point_regex = regex.compile(r"@entrypoint(\(.*\))?\s+")

def replace_keywords(code):
    code = regex.sub(definition_regex, r"def \2", code)
    code = regex.sub(lambda_regex, r"lambda \1:", code)
    code = regex.sub(up_one_regex, r"\1 += 1", code)
    code = regex.sub(down_one_regex, r"\1 -= 1", code)
    code = regex.sub(not_equal_regex, r"!=", code)

    return code


def better_range(code):
    if ".." not in code:
        return code

    for b in regex.findall(range_function_regex_two_groups, code):
        code = code.replace(f"{b[0]}..{b[1]}", f"range({b[0]}, {b[1]})")

    for b in regex.findall(range_function_regex_one_group, code):
        code = code.replace(f"..{b}", f"range({b})")

    for b in regex.findall(range_function_regex_infinite, code):
        code = code.replace(f"{b}..", f"infinite_range({b})")

    return code


def entry_point(code):
    entry_points = list(regex.finditer(entry_point_regex, code))

    if len(entry_points) == 0:
        return code

    if len(entry_points) > 1:
        raise Exception("Multiple entry points found")

    entry_point_found = entry_points[0]
    args = entry_point_found.group(1)

    if args is None:
        args = "()"

    next_line = ""
    for c in code[entry_point_found.end():]:
        if c == "\n":
            break

        next_line += c

    signature = list(regex.finditer(definition_regex, next_line))

    if len(signature) == 0:
        raise Exception("No function signature found after entry point")

    function_name = signature[0].group(2)[:-1]

    # quick and dirty fix
    poetry___name__ = "qb.__main__"

    idiom = f"\nif __name__ == \"{poetry___name__}\":\n\t{function_name}{args}"

    code += idiom
    code = code.replace("@entrypoint", "")

    return code
