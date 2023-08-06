from setuptools import setup, find_packages

setup(
    name='mturk-crowd-beta-client',
    version='1.0.0',
    description='A client for the MTurk Crowd REST API',
    long_description=open('README.rst').read(),
    url='https://github.com/awslabs/mturk-crowd-beta-client-python',
    author='Amazon Mechanical Turk',
    author_email='mturk-requester-preview@amazon.com',
    keywords='mturk-crowd-beta-client',
    license='Apache License 2.0',

    packages=find_packages(),

    install_requires=[
        'boto3>=1.4.4',
        'requests>=2.16',
    ],

    python_requires='>=2.7, <4',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)
