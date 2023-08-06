import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-paytm',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app to conduct payment using Paytm.',
    long_description=README,

    author='Naresh Chaudhary',
    author_email='naresh@quixom.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires = [
        "backports.shutil-get-terminal-size==1.0.0",
        "decorator==4.0.10",
        "enum34==1.1.6",
        "ipython-genutils==0.1.0",
        "pathlib2==2.1.0",
        "pexpect==4.2.1",
        "pickleshare==0.7.4",
        "prompt-toolkit==1.0.9",
        "ptyprocess==0.5.1",
        "pycrypto==2.6.1",
        "Pygments==2.1.3",
        "simplegeneric==0.8.1",
        "traitlets==4.3.1",
        "wcwidth==0.1.7"
    ]
)