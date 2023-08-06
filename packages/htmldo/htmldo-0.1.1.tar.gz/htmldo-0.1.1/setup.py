from setuptools import setup

setup(
    name='htmldo', 
    scripts=['htmldo/__init__.py', 'htmldo/htmld.py'],                  # The name of your scipt, and also the command you'll be using for calling it
    install_requires = [
        'beautifulsoup4'
    ],
    version='0.1.1',

    description = '',
    author = 'franklynchen',
    author_email = 'test@test.test',
    url = '',
    download_url = '',
    keywords = [''],
    classifiers = [],
)
