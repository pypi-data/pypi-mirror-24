from setuptools import setup

setup(
    name='htmldo', 
    scripts=['htmldo/htmld.py'],                  # The name of your scipt, and also the command you'll be using for calling it
    install_requires = [
        'beautifulsoup4'
    ],
    version='0.1.3',

    description = '',
    author = 'franklynchen',
    author_email = 'test@test.test',
    url = 'https://github.com/Franklyncc/htmldo',
    download_url = '',
    keywords = [''],
    classifiers = [],
)
