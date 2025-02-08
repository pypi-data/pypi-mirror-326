from warnings import warn


def preprocess(code):
    raise_errors_and_warnings(code)

    code = code.replace("|>", ">>")
    code = code.replace("<|", "<<")

    return code


def raise_errors_and_warnings(code):
    shifting_operators = ["<<", ">>"]
    shifting_error = "When bit shifting, use the 'lshift' and 'rshift' function instead of the '>>' and '<<' operators respectively"

    io_functions = ["print", "input"]
    io_warning = "When performing io-operations, use cout and cin instead of the 'print' and 'input' functions respectively"

    function_definitions = ["def", "lambda"]
    function_error = (
        "When defining a function, use the 'fn' keyword instead of 'def' or 'lambda' like so: 'fn x -> x ** 2'"
    )

    not_operator = "<>"
    not_error = "When checking for inequality, use the '<>' operator instead of '!='"

    range_usage = "range"
    range_error = "When generating a range, use the '..' operator instead of the range function like so: '1..10'"

    for operator in shifting_operators:
        if operator in code:
            raise SyntaxError(shifting_error)

    for function in io_functions:
        if function in code:
            warn(SyntaxWarning(io_warning))

    for definition in function_definitions:
        if definition in code:
            warn(SyntaxWarning(function_error))

    if not_operator in code:
        warn(SyntaxWarning(not_error))

    if range_usage in code:
        warn(SyntaxWarning(range_error))