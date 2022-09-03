try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Jack DesCombes',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'jpdesc@alumni.stanford.edu',
    'version': '0.1',
    'install_requires': ['pytest'],
    'packages': ['ouraapp', 'tests'],
    'scripts': [],
    'name': 'oura'
}

setup(**config)
# setup(name="oura/", packages=find_packages())
