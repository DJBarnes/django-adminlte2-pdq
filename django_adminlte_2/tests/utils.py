def valid_string_hook_function(arg1, context, kwarg1='kwarg1'):
    """A valid hook function used in testing"""
    return 'foobar ' + arg1 + ' ' + kwarg1

def valid_tuple_hook_function(arg1, context, kwarg1='kwarg1'):
    """A invalid hook function used in testing"""
    return ('foobar', arg1 + ' ' + kwarg1,)