# coding: utf-8
"""
This will add the executable to your PATH so it will be found.
"""

import os
from . import utils


def install():
    """
    Appends the directory of the chromedriver binary file to PATH.

    :return: The file path of chromedriver
    """
    chromedriver_filepath = utils.download_chromedriver()
    chromedriver_dir = os.path.dirname(chromedriver_filepath)
    if 'PATH' not in os.environ:
        os.environ['PATH'] = chromedriver_dir
    elif chromedriver_dir not in os.environ['PATH']:
        os.environ['PATH'] = chromedriver_dir + utils.get_variable_separator() + os.environ['PATH']
    return chromedriver_filepath
