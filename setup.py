import re

from setuptools import setup

requirements: list[str] = []
with open("./requirements.txt") as file:
    requirements = file.read().splitlines()

readme = ''
with open('./README.md') as file:
    readme: str = file.read()

version = ''
with open('./ampapi/__init__.py') as file:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE).group(1)  # type:ignore

if not version:
    raise RuntimeError("version is not set")

packages = ["ampapi",]  # I believe this will affect the open #LN13

setup(
    name='cubecoders_amp_api_wrapper',
    version=version,
    description='A python wrapper for the AMP API by CubeCoders',
    url='https://github.com/k8thekat/AMPAPI_Python',
    author='Katelynn Cadwallader',
    author_email='Cadwalladerkatelynn+AMPAPI@gmail.com',
    license='GNU',
    project_urls={
        'GitHub': 'https://github.com/k8thekat/AMPAPI_Python',
        'Changelog': 'https://github.com/k8thekat/AMPAPI_Python/blob/master/CHANGELOG.md',
    },
    packages=packages,
    package_data={
        "docs": ["docs/api_spec.md", "docs/permission_nodes.md", "docs/setting_nodes.md"],
        "license": ["LICENSE"],
        "requirements": ["requirements.txt"],
        "readme": ["README.md"],
        "changelog": ["CHANGELOG.md"]},
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
