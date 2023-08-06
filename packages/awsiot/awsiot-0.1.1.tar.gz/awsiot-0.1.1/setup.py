from setuptools import setup, find_packages

setup(
    name='awsiot',
    description='Command Line utility to easily provision IoT things in AWS',

    version='0.1.1',

    # Author details
    author='Adamson dela Cruz',
    author_email='adamson.delacruz@gmail.com',
    url='https://github.com/adamsondelacruz/awsiot',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='aws iot',

    #packages=['commands'],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=[
        'click', 'boto3', 'botocore'
    ],
    # entry_points='''
    #     [console_scripts]
    #     awsiot=commands.awsiot:main
    # ''',
    entry_points={
        'console_scripts': [
            'awsiot=commands.awsiot:main',
        ],
    },
)