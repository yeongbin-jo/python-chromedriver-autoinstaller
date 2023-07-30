# chromedriver-autoinstaller

[![PyPI](https://img.shields.io/pypi/v/chromedriver-autoinstaller.svg)](https://pypi.org/project/chromedriver-autoinstaller) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/chromedriver-autoinstaller.svg)](https://pypi.org/project/chromedriver-autoinstaller/)

Automatically download and install [chromedriver](https://chromedriver.chromium.org/) that supports the currently installed version of Chrome. This installer supports Linux, MacOS, and Windows operating systems.

## Installation

```bash
pip install chromedriver-autoinstaller
```

## Usage
Just type `import chromedriver_autoinstaller` in the module you want to use chromedriver.

## Example
```
from selenium import webdriver
import chromedriver_autoinstaller


chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # Then add chromedriver to the path

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
```
