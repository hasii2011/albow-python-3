
"""
    Albow file dialog utility methods
"""

import os


from albow.dialog.FileOpenDialog import FileOpenDialog
from albow.dialog.LookForFileDialog import LookForFileDialog
from albow.dialog.FileSaveDialog import FileSaveDialog


def request_new_filename(prompt=None, suffix=None, extra_suffixes=None, directory=None, filename=None, pathname=None):
    if pathname:
        directory, filename = os.path.split(pathname)
    if extra_suffixes:
        suffixes = extra_suffixes
    else:
        suffixes = []
    if suffix:
        suffixes = [suffix] + suffixes
    dlog = FileSaveDialog(prompt=prompt, suffixes=suffixes)
    if directory:
        dlog.directory = directory
    if filename:
        dlog.filename = filename
    if dlog.present():
        return dlog.pathname
    else:
        return None


def request_old_filename(suffixes=None, directory=None):
    """

    :param suffixes:
    :param directory:
    :return:
    """
    attrs = {'margin': 10}

    dlog = FileOpenDialog(suffixes=suffixes, **attrs)
    if directory:
        dlog.directory = directory
    if dlog.present():
        return dlog.pathname
    else:
        return None


def look_for_file_or_directory(target, prompt=None, directory=None):

    dlog = LookForFileDialog(target=target, prompt=prompt)
    if directory:
        dlog.directory = directory
    if dlog.present():
        return dlog.pathname
    else:
        return None
