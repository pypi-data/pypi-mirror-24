from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

blurb = 'A package that provides ipywidgets for standard neuroimaging plotting'
if path.isfile('README.md'):
    readme = open('README.md', 'r').read()
else:
    readme = blurb

version = '0.1.3'

setup(
    name='niwidgets',
    version=version,
    description=blurb,
    long_description=readme,
    url='https://github.com/janfreyberg/niwidgets',
    download_url='https://github.com/janfreyberg/niwidgets/archive/' +
        version + '.tar.gz',
    # Author details
    author='Bjoern Soergel & Jan Freyberg',
    author_email='jan.freyberg@gmail.com',
    packages=['niwidgets'],
    install_requires=['ipywidgets', 'nilearn', 'nibabel'],
    # Include the template file
    package_data={
        '': ['data/*nii*']
    },
)
