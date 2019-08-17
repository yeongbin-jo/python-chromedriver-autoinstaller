# coding: utf-8

from setuptools import setup
from setuptools.command.build_py import build_py
from chromedriver_autoinstaller.utils import download_chromedriver


__author__ = 'Yeongbin Jo <iam.yeongbin.jo@gmail.com>'


with open('README.md') as readme_file:
    long_description = readme_file.read()


class DownloadChromedriver(build_py):
    def run(self):
        """
        Downloads, unzips and installs chromedriver.
        If a chromedriver binary is found in PATH it will be copied, otherwise downloaded.
        """
        download_chromedriver()
        build_py.run(self)


setup(
    name="chromedriver-autoinstaller",
    version="0.0.1",
    author="Yeongbin Jo",
    author_email="iam.yeongbin.jo@gmail.com",
    description="Auto installer for chromedriver.",
    license="MIT",
    keywords="chromedriver chrome selenium splinter",
    url="https://github.com/yeongbin-jo/python-chromedriver-autoinstaller",
    packages=['chromedriver_autoinstaller'],
    package_data={
        'chromedriver_autoinstaller': ['chromedriver*']
    },
    entry_points={
        'console_scripts': ['chromedriver-path=chromedriver_autoinstaller.utils:print_chromedriver_path'],
    },
    long_description_content_type='text/markdown',
    long_description=long_description,
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Installation/Setup',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    cmdclass={'build_py': DownloadChromedriver}
)
