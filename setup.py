import os
from setuptools import setup, find_packages

setup(
    name='pubnub_agent',
    version='1.0',
    description='Example snap app for pubnub',
    author='Abhishek Mishra',
    author_email='abhihdr03@gmail.com',
    url='',
    packages=['upstream', 'downstream'],
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    install_requires=[
        'pycryptodomex>=3.3',
        'requests>=2.4',
        'six>=1.10',
        'paho-mqtt',
        'pubnub'
    ],
    zip_safe=True,
)
