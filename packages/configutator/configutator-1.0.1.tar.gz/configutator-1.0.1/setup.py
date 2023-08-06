from setuptools import setup, find_packages

with open('README.rst') as readme:
    setup(
        name='configutator',
        version='1.0.1',
        packages=find_packages(),
        long_description=readme.read(),
        install_requires=['ruamel.yaml', 'jmespath', 'asciimatics'],
        url='https://github.com/innovate-invent/configutator',
        license='MIT',
        author='Nolan',
        author_email='innovate.invent@gmail.com',
        description='Maps yaml nodes and command line arguments to python function parameters.',
        include_package_data=True
    )
