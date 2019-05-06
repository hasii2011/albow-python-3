
import os

from albow.dialog.FileOpenDialog import FileOpenDialog
from albow.dialog.LookForFileDialog import LookForFileDialog
from albow.dialog.FileSaveDialog import FileSaveDialog


def request_new_filename(prompt=None, suffix=None, extra_suffixes=None, directory=None, filename=None, pathname=None):
    """
    Presents a dialog for specifying a new file.

    Args:
        prompt: The prompt is displayed as a prompt to the user.

        suffix: The suffix, if any, will be appended to the filename returned if necessary, and also
                specifies which files can be chosen.

        extra_suffixes: The extra_suffixes can be a list of additional suffixes of choosable files.

        directory:  Specifies the starting directory

        filename:   The initial contents of the filename box

        pathname:   Alternatively the pathname can be used to specify both of these together

    Returns:    The full pathname of the file chosen, or None if the dialog is cancelled.

    """
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
    Presents a dialog for choosing an existing file.

    Args:
        suffixes: The suffixes is a list of filename extensions defining
                  the files that can be chosen; if not specified, any file can be chosen.

        directory: The directory specifies the directory
                   in which to start browsing; if unspecified, the current working directory is used.

    Returns:    Returns the full pathname of the file chosen, or None if the dialog is cancelled.
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
    """
    This function is used to ask the user to locate a file or directory with a specific name
    Any directory can be visited, but only files whose last pathname component matches the target are visible
    and choosable.

    Args:
        target: The file/directory to look for

        prompt: The prompt to display

        directory:  Specifies the directory in which to start browsing.

    Returns:        Returns the full pathname of the file or directory chosen, or None if the dialog is cancelled.
    """

    dlog = LookForFileDialog(target=target, prompt=prompt)
    if directory:
        dlog.directory = directory
    if dlog.present():
        return dlog.pathname
    else:
        return None
