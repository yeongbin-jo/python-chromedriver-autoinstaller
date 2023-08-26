# chromedriver-autoupdater
Automatically download and install [chromedriver](https://chromedriver.chromium.org/) that supports the currently installed version of chrome. This installer supports Linux, MacOS and Windows operating systems.

Forked from [chromedriver-autoinstaller](https://github.com/yeongbin-jo/python-chromedriver-autoinstaller)

## Installation

```bash
pip install chromedriver_autoupdater
```

## Usage
Just type `import chromedriver_autoupdater` in the module you want to use chromedriver.

## Example
```
from selenium import webdriver
import chromedriver_autoupdater


chromedriver_autoupdater.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
```
