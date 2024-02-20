from setuptools import setup
import re

requirements: list[str] = []
with open("requirements.txt") as file:
    requirements = file.read().splitlines()

readme = ''
with open('README.md') as file:
    readme: str = file.read()

version = ''
with open('ampapi/__init__.py') as file:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type:ignore

if not version:
    raise RuntimeError("version is not set")

packages = ["AMPapi",]

setup(
    name='cubecoders_amp_api',
    version=version,
    description='A python API package to interact with the AMP API by CubeCoders',
    url='https://github.com/k8thekat/AMPAPI_Python',
    author='Katelynn Cadwallader',
    author_email='Cadwalladerkatelynn+AMPAPI@gmail.com',
    license='GNU',
    packages=packages,
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires='>=3.9.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Framework :: AsyncIO',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)
