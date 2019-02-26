import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='user-token-store',
    version='1.0',
    author='Chris Toal',
    author_email='ctoal@bink.com',
    description='A store for user auth tokens',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.bink.com/libs/user-token-store',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
