# Apache 2.0 licensed

"""
This module provides functions for evaluating Python code,
which is intended to be secure.

Warning: Since this module is new, its possible there are flaws in it.


How it Works
============

- Restrict built-in namespace access.
- Restrict byte-codes used.


What Works
==========

This works:

    a ** cos(b / c) - sin(d)

This will fail:

    a.b

    __import__("os").unlink("path")
"""

__all__ = (
    "safe_eval",
    "raise_if_code_unsafe",
    )

import dis


builtins_whitelist = {
    # basic funcs
    "all",
    "any",
    "len",
    "max",
    "min",

    # types
    "bool",
    "float",
    "int",

    # math
    "abs",
    "divmod",
    "pow",
    "round",
    "sum",
    }


opcode_whitelist = {
    'NOP',
    'UNARY_POSITIVE',
    'UNARY_NEGATIVE',
    'UNARY_NOT',
    'UNARY_INVERT',
    'BINARY_MATRIX_MULTIPLY',
    'INPLACE_MATRIX_MULTIPLY',
    'BINARY_POWER',
    'BINARY_MULTIPLY',
    'BINARY_MODULO',
    'BINARY_ADD',
    'BINARY_SUBTRACT',
    'BINARY_SUBSCR',
    'BINARY_FLOOR_DIVIDE',
    'BINARY_TRUE_DIVIDE',
    'INPLACE_FLOOR_DIVIDE',
    'INPLACE_TRUE_DIVIDE',
    'INPLACE_ADD',
    'INPLACE_SUBTRACT',
    'INPLACE_MULTIPLY',
    'INPLACE_MODULO',
    'BINARY_LSHIFT',
    'BINARY_RSHIFT',
    'BINARY_AND',
    'BINARY_XOR',
    'BINARY_OR',
    'INPLACE_POWER',
    'INPLACE_LSHIFT',
    'INPLACE_RSHIFT',
    'INPLACE_AND',
    'INPLACE_XOR',
    'INPLACE_OR',
    'RETURN_VALUE',
    'LOAD_CONST',
    'LOAD_NAME',
    'BUILD_TUPLE',
    'BUILD_LIST',
    'BUILD_SET',
    'BUILD_MAP',
    'COMPARE_OP',
    'JUMP_FORWARD',
    'JUMP_IF_FALSE_OR_POP',
    'JUMP_IF_TRUE_OR_POP',
    'JUMP_ABSOLUTE',
    'POP_JUMP_IF_FALSE',
    'POP_JUMP_IF_TRUE',
    'LOAD_GLOBAL',
    'LOAD_FAST',
    'STORE_FAST',
    'DELETE_FAST',
    'CALL_FUNCTION',
    'LOAD_DEREF',
    'STORE_DEREF',
    'CALL_FUNCTION_VAR',
    'CALL_FUNCTION_KW',
    'CALL_FUNCTION_VAR_KW',
    }

# Convert names to index
opname_reverse = {name: index for index, name in enumerate(dis.opname)}
opcode_whitelist_index = {opname_reverse[name] for name in opcode_whitelist}


def raise_if_code_unsafe(code, globals=None, locals=None):
    whitelist = set(builtins_whitelist)
    if globals:
        whitelist.update(globals)
    if locals:
        whitelist.update(locals)

    bad_ops = []
    for name in code.co_names:
        if name not in whitelist:
            bad_ops.append(name)

    if bad_ops:
        raise RuntimeError(
                "Name(s) %s not in white-list: (%s)" % (
                ", ".join(repr(name) for name in bad_ops),
                ", ".join(sorted(whitelist)))
                )
    del bad_ops

    code_bytes = code.co_code

    def code_size(opcode):
        if opcode >= dis.HAVE_ARGUMENT:
            return 3
        else:
            return 1

    i = 0
    code_len = len(code_bytes)
    while i < code_len:
        opcode = code_bytes[i]

        if opcode not in opcode_whitelist_index:
            raise RuntimeError("OpCode %r not in white-list" % dis.opname[opcode])

        i += code_size(opcode)


def safe_eval(source, globals=None, locals=None):

    code = compile(source, "<safe_eval>", "eval")

    raise_if_code_unsafe(code, globals=globals, locals=locals)

    return eval(code, globals, locals)
