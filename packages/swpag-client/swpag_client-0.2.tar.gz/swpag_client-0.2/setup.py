from distutils.core import setup

setup(
    name='swpag_client',
    version='0.2',
    description='This is a python module that provides an interface to the SWPAG team API.',
    packages=['swpag_client'],
    install_requires=[
        'requests',
        'future',
    ],
)
