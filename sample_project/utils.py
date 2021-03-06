def _create_key(path, length):
    """
    Creates project "secret key" in settings folder.
    """
    import string
    from django.utils.crypto import get_random_string

    # Generate key.
    key = get_random_string(
        length,
        string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    )

    # Write key to file.
    with open(path, 'w') as _f:
        _f.write(key)

    return key

def get_secret_key(base_dir):
    """
    Get SECRET_KEY from file system or generate new one
    """
    MIN_KEY_LENGTH = 50
    KEY_PATH = base_dir.joinpath('sample_project/SECRET_KEY')

    # Attempt to open and validate secret key.
    SECRET_KEY = ''
    _io_error = False  # pylint: disable=invalid-name
    try:
        with open(KEY_PATH, 'r') as _f:
            SECRET_KEY = _f.read().strip()
    except IOError:
        _io_error = True  # pylint: disable=invalid-name

    if _io_error or len(SECRET_KEY) < MIN_KEY_LENGTH:
        SECRET_KEY = _create_key(KEY_PATH, MIN_KEY_LENGTH)

    return SECRET_KEY