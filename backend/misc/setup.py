import os
from typing import Optional


def get_program_path():
    return os.path.abspath(os.path.join(__file__, '../..'))


def is_already_setup() -> Optional[bool]:
    main_path = get_program_path()
    if os.path.exists(os.path.join(main_path, 'private.py')):
        return True


def setup_config():
    pass


if is_already_setup():
    import config
    config.NOT_FIRST_TIME_RUN = True
else:
    setup_config()
