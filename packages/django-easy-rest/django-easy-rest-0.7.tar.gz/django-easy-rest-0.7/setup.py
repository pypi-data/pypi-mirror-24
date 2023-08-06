import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-easy-rest',
    version='0.7',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['djangorestframework'],
    license='MIT License',
    description='A simple Django app to create rest applications',
    url='https://github.com/jonatanSh/django-easy-rest/',
    author='Jonathan Shimon',
    author_email='jonatanshimon@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
