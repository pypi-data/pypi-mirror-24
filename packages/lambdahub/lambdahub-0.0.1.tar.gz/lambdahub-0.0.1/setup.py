from setuptools import setup #, find_packages
from codecs import open
from os import path

setup(
    name='lambdahub',
    version='0.0.1',
    description='Client library for LambdaHub',
    long_description="",
    url='https://lambdahub.com',
    author='LambdaHub',
    author_email='andrew@lambdahub.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='lambdahub client',
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=["lambdahub"], # instead of find_packages for now
    install_requires=[],
    extras_require={
        'dev': [],
        'test': [],
    },
    entry_points={
        'console_scripts': [],
    },
)
