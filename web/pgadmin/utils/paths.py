##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2018, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
#########################################################################

"""This file contains functions fetching different utility paths."""

import os

from flask import url_for
from flask_security import current_user, login_required


@login_required
def get_storage_directory():
    import config
    if config.SERVER_MODE is not True:
        return None

    storage_dir = getattr(
        config, 'STORAGE_DIR',
        os.path.join(
            os.path.realpath(
                os.path.expanduser('~/.pgadmin/')
            ), 'storage'
        )
    )

    if storage_dir is None:
        return None

    username = current_user.email.split('@')[0]
    if len(username) == 0 or username[0].isdigit():
        username = 'pga_user_' + username

    storage_dir = os.path.join(
        storage_dir.decode('utf-8') if hasattr(storage_dir, 'decode')
        else storage_dir,
        username
    )

    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir, int('700', 8))

    return storage_dir


def init_app(app):
    import config
    if config.SERVER_MODE is not True:
        return None

    storage_dir = getattr(
        config, 'STORAGE_DIR',
        os.path.join(
            os.path.realpath(
                os.path.expanduser('~/.pgadmin/')
            ), 'storage'
        )
    )

    if storage_dir and not os.path.isdir(storage_dir):
        if os.path.exists(storage_dir):
            raise Exception(
                'The path specified for the storage directory is not a '
                'directory.'
            )
        os.makedirs(storage_dir, int('700', 8))

    if storage_dir and not os.access(storage_dir, os.W_OK | os.R_OK):
        raise Exception(
            'The user does not have permission to read and write to the '
            'specified storage directory.'
        )


def get_cookie_path():
    cookie_root_path = '/'
    pgadmin_root_path = url_for('browser.index')
    if pgadmin_root_path != '/browser/':
        cookie_root_path = pgadmin_root_path.replace(
            '/browser/', ''
        )
    return cookie_root_path
