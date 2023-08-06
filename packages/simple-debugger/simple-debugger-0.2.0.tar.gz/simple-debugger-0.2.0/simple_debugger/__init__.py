
import inspect


def generate_debug_statement(method, args=(), kwargs={}):

    def wrap_string_in_quotes(value):
        if isinstance(value, str):
            return '"' + value + '"'
        else:
            return value

    this_debug_statement = ""
    this_debug_statement +=  "\ndebugging '{name}':\n".format(name=method.__name__)

    inspector = inspect.getargspec(method)

    arg_names = inspector.args
    var_args = inspector.varargs
    keyword_args = inspector.keywords or 'kwargs'

    """
    for some reason, when running on something like

        @debugger
        def one_two_three_silent(one, two, three=3):
            print(three)

        one_two_three_silent(1, 2)

    the `three` arg doesn't come in either args or kwargs...
    """
    incoming_args_length = len(args) + len(kwargs.keys())
    if len(arg_names) > incoming_args_length:
        nearly_forgotten_args = arg_names[incoming_args_length:]
        for index, arg_name in enumerate(nearly_forgotten_args):
            kwargs[arg_name] = inspector.defaults[index]

    FOUR_SPACES = " " * 4
    EIGHT_SPACES = " " * 8

    if args and arg_names:
        this_debug_statement +=  "\n{four}args:\n\n".format(four=FOUR_SPACES)
        for index, arg_name in enumerate(arg_names):
            try:
                this_debug_statement +=  "{eight}{name} = {arg}\n".format(
                    eight=EIGHT_SPACES,
                    name=arg_name,
                    arg=wrap_string_in_quotes(args[index])
                )
            except:
                pass

    if var_args:
        start = len(arg_names)
        these_args = args[start:]
        this_debug_statement +=  "\n{four}*{star_arg_name}:\n\n".format(four=FOUR_SPACES, star_arg_name=var_args)
        for this_var_arg in these_args:
            this_debug_statement +=  "{eight}{arg}\n".format(eight=EIGHT_SPACES, arg=wrap_string_in_quotes(this_var_arg))

    if kwargs:
        this_debug_statement +=  "\n{four}**{kwargs_name}:\n\n".format(four=FOUR_SPACES, kwargs_name=keyword_args)
        for key, value in kwargs.items():
            this_debug_statement +=  "{eight}{key} = {value}\n".format(
                eight=EIGHT_SPACES,
                key=key,
                value=wrap_string_in_quotes(value)
            )

    return this_debug_statement


def debugger(method):

    def dec(*args, **kwargs):
        debug_statement = generate_debug_statement(method, args, kwargs)
        print(debug_statement)
        result = method(*args, **kwargs)
        return result

    return dec
