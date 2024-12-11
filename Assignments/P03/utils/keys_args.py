import sys


def myKwargs(argv):
    """This process command line arguments and lets you "configure" the current run.
    It takes parameters that look like: key=value or num_people=100 (with NO spaces between)
    and puts them into a python dictionary that looks like:
    {
        "key":"value",
        "num_people":100
    }

    If a parameter doesn't have an "=" sign in it, it puts it into a list
    Both the dictionary (kwargs) and list (args) get returned.
    See usage below under if__name__=='__main__'
    """
    kwargs = {}
    args = []
    for param in argv:
        if "=" in param:
            k, v = param.split("=")
            if v.isnumeric():
                kwargs[k] = int(v)
            else:
                kwargs[k] = v
        else:
            if param.isnumeric():
                param = int(param)
            args.append(param)

    return kwargs, args
