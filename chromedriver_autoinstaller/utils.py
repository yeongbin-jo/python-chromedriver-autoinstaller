# coding: utf-8
"""
Helper functions for filename and URL generation.
"""

import logging
import os
import json
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as elemTree
import zipfile
from io import BytesIO
import platform as pf

__author__ = "Yeongbin Jo <iam.yeongbin.jo@gmail.com>"

from typing import AnyStr, Optional


def get_chromedriver_filename():
    """
    Returns the filename of the binary for the current platform.
    :return: Binary filename
    """
    if sys.platform.startswith("win"):
        return "chromedriver.exe"
    return "chromedriver"


def get_variable_separator():
    """
    Returns the environment variable separator for the current platform.
    :return: Environment variable separator
    """
    if sys.platform.startswith("win"):
        return ";"
    return ":"


def get_platform_architecture(chrome_version=None):
    if sys.platform.startswith("linux") and sys.maxsize > 2**32:
        platform = "linux"
        architecture = "64"
    elif sys.platform == "darwin":
        platform = "mac"
        if pf.processor() == "arm":
            architecture = "-arm64"
        elif pf.processor() == "i386":
            architecture = "-x64"
        else:
            raise RuntimeError("Could not determine Mac processor architecture.")
    elif sys.platform.startswith("win"):
        platform = "win"
        architecture = "32"
    else:
        raise RuntimeError(
            "Could not determine chromedriver download URL for this platform."
        )
    return platform, architecture


def get_chromedriver_url(download_options):
    """
    Selects the download URL from available options for current platform , architecture and the given version.
    Supports Linux, MacOS and Windows.
    :param download_options: list of objects containing platform, and url keys
    :return: Download URL for chromedriver
    """
    platform, architecture = get_platform_architecture()
    for download_option in download_options:
        if f'{platform}{architecture}' in download_option['platform']:
            return download_option['url']


def find_binary_in_path(filename):
    """
    Searches for a binary named `filename` in the current PATH. If an executable is found, its absolute path is returned
    else None.
    :param filename: Filename of the binary
    :return: Absolute path or None
    """
    if "PATH" not in os.environ:
        return None
    for directory in os.environ["PATH"].split(get_variable_separator()):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    return None


def check_version(binary, required_version):
    try:
        version = subprocess.check_output([binary, "-v"])
        version = re.match(r".*?([\d.]+).*?", version.decode("utf-8"))[1]
        if version == required_version:
            return True
    except Exception:
        return False
    return False


def get_chrome_version():
    """
    :return: the version of chrome installed on client
    """
    platform, _ = get_platform_architecture()
    if platform == "linux":
        path = get_linux_executable_path()
        with subprocess.Popen([path, "--version"], stdout=subprocess.PIPE) as proc:
            version = (
                proc.stdout.read()
                .decode("utf-8")
                .replace("Chromium", "")
                .replace("Google Chrome", "")
                .strip()
            )
    elif platform == "mac":
        process = subprocess.Popen(
            [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--version",
            ],
            stdout=subprocess.PIPE,
        )
        version = (
            process.communicate()[0]
            .decode("UTF-8")
            .replace("Google Chrome", "")
            .strip()
        )
    elif platform == "win":
        dirs = [f.name for f in os.scandir("C:\\Program Files\\Google\\Chrome\\Application") if f.is_dir() and re.match("^[0-9.]+$", f.name)]
        version = max(dirs)
    else:
        return
    return version


def get_linux_executable_path():
    """
    Look through a list of candidates for Google Chrome executables that might
    exist, and return the full path to first one that does. Raise a ValueError
    if none do.

    :return: the full path to a Chrome executable on the system
    """
    for executable in (
        "google-chrome",
        "google-chrome-stable",
        "google-chrome-beta",
        "google-chrome-dev",
        "chromium-browser",
        "chromium",
    ):
        path = shutil.which(executable)
        if path is not None:
            return path
    raise ValueError("No chrome executable found on PATH")


def get_major_version(version):
    """
    :param version: the version of chrome
    :return: the major version of chrome
    """
    return version.split(".")[0]


def get_chromedriver_version_and_download_options(version, no_ssl=False):
    """
    :param version: the version of chrome
    :return: the major version of chromedriver, download options for version
    """
    if no_ssl:
        doc = urllib.request.urlopen(
            "http://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"
        ).read()
    else:
        doc = urllib.request.urlopen(
            "https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json"
        ).read()
    data = json.loads(doc)
    current_major_version = get_major_version(version)
    available_milestones = data['milestones']
    if current_major_version in available_milestones.keys():
        if 'chromedriver' in available_milestones[current_major_version]['downloads'].keys():
            return current_major_version, available_milestones[current_major_version]['downloads']['chromedriver']
        
    return


def get_chromedriver_path():
    """
    :return: path of the chromedriver binary
    """
    return os.path.abspath(os.path.dirname(__file__))


def print_chromedriver_path():
    """
    Print the path of the chromedriver binary.
    """
    print(get_chromedriver_path())


def download_chromedriver(path: Optional[AnyStr] = None, no_ssl: bool = False):
    """
    Downloads, unzips and installs chromedriver.
    If a chromedriver binary is found in PATH it will be copied, otherwise downloaded.

    :param str path: Path of the directory where to save the downloaded chromedriver to.
    :param bool no_ssl: Determines whether or not to use the encryption protocol when downloading the chrome driver.
    :return: The file path of chromedriver
    """
    chrome_version = get_chrome_version()
    if not chrome_version:
        logging.debug("Chrome is not installed.")
        return
    major_version, download_options = get_chromedriver_version_and_download_options(chrome_version, no_ssl)
    if not major_version and download_options:
        logging.warning(
            "Can not find chromedriver for currently installed chrome version."
        )
        return
    
    if path:
        if not os.path.isdir(path):
            raise ValueError(f"Invalid path: {path}")
        chromedriver_dir = os.path.join(os.path.abspath(path), major_version)
    else:
        chromedriver_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), major_version
        )
    chromedriver_filename = get_chromedriver_filename()
    chromedriver_filepath = os.path.join(chromedriver_dir, chromedriver_filename)
    if not os.path.isfile(chromedriver_filepath) or not check_version(
        chromedriver_filepath, major_version
    ):
        logging.info(f"Downloading chromedriver ({major_version})...")
        if not os.path.isdir(chromedriver_dir):
            os.makedirs(chromedriver_dir)
        url = get_chromedriver_url(download_options)
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() != 200:
                raise urllib.error.URLError("Not Found")
        except urllib.error.URLError:
            raise RuntimeError(f"Failed to download chromedriver archive: {url}")
        archive = BytesIO(response.read())

        with zipfile.ZipFile(archive) as zip_file:
            # sub_folder in zip file is the same as the file name
            sub_folder_in_zip = url.split('/')[-1].split('.')[0]
            # we want to extract the chromedriver binary from the sub folder
            with open(chromedriver_filepath, 'wb') as f:
                f.write(zip_file.read(f'{sub_folder_in_zip}/{chromedriver_filename}'))
    else:
        logging.info("Chromedriver is already installed.")
    if not os.access(chromedriver_filepath, os.X_OK):
        os.chmod(chromedriver_filepath, 0o744)
    return chromedriver_filepath


if __name__ == "__main__":
    print(get_chrome_version())
    print(download_chromedriver(no_ssl=False))
