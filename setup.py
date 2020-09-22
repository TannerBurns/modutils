import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='modutils',
    version='0.1.9',
    packages=find_packages(),
    include_package_data=True,
    description='A library with modern utilities to assist development efficiency ',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://www.github.com/tannerburns/modutils',
    author='Tanner Burns',
    author_email='tjburns102@gmail.com',
    install_requires=[
        'requests',
        'colored',
        'tqdm',
        'beautifulsoup4'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ],
)