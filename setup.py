try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Oura Sleep and Workout Tracker',
    'author': 'Jack DesCombes',
    'url': 'server.jpdesc.com',
    'author_email': 'jpdesc@alumni.stanford.edu',
    'version': '0.1',
    'install_requires': ['pytest'],
    'packages': ['ouraapp', 'tests'],
    'scripts': [],
    'name': 'jwa'
}

setup(**config)
# setup(name="oura/", packages=find_packages())
