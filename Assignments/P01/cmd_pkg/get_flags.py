def get_flags(
    allowed_flags,
    args=None,
):
    flags = []
    flags_index = []
    invalid_flags = False

    if args:
        for index, arg in enumerate(args):
            if arg.startswith("-"):
                # Record the index of this flag
                flags_index.append(index)
                # If the flag contains multiple characters, split them up
                for char in arg[1:]:
                    flags.append(char)

    for flag in flags:
        if flag not in allowed_flags:
            invalid_flags = True
            break
    return {"flags": flags, "flags_index": flags_index, "invalid_flags": invalid_flags}
