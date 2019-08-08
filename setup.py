from setuptools import setup, find_packages

VERSION = {}
with open('NLP_utils/version.py', 'r', encoding='utf-8')as version_file:
    exec(version_file.read(), VERSION)

setup(
    name='NLP_utils',
    version=VERSION['VERSION'],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    url='',
    license='',
    author='Liangs',
    author_email='liangsli.mail@gmail.com',
    description='',
    include_package_data=True,
)
