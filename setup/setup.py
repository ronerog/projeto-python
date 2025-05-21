from setuptools import setup, find_packages

setup(
    name='docker',  # ou outro nome que quiser, mas precisa bater com o pacote
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'install-docker=docker.__init__:main',
        ],
    },
)