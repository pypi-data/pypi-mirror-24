import codecs
from setuptools import setup, find_packages

def readme(filename):
    file = codecs.open(filename, 'r', 'utf-8')
    contents = file.read()
    try:
        return unicode(contents)
    except NameError:
        return str(contents)

setup(
    name='django-werkzeug-debugger-runserver',
    version='0.3.1',
    description='Replaces Django\'s runserver command with one that includes the Werkzeug debugger (shamelessly ripped out of django-extensions)',
    long_description=readme('README.rst'),
    author='Philipp Bosch and https://github.com/django-extensions/django-extensions/contributors',
    author_email='hello@pb.io',
    license='BSD',
    url='http://github.com/philippbosch/django-werkzeug-debugger-runserver',
    packages=find_packages(),
    install_requires=[
        'Werkzeug',
        'six',
    ]
)
