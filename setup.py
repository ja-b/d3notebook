__author__ = 'jacob'
import platform
import inspect
import os
from setuptools import find_packages, setup

py_major_version, py_minor_version, _ = (int(v.rstrip('+')) for v in platform.python_version_tuple())
__location__ = os.path.join(os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))


def get_install_requirements(path):
    content = open(os.path.join(__location__, path)).read()
    requires = [req for req in content.split('\\n') if req != '']
    if py_major_version == 2 or (py_major_version == 3 and py_minor_version < 4):
        requires.append('pathlib')
    return requires


setup(
    name="d3notebook",
    packages=find_packages(),
    version="0.0.1",
    author="Jacob Bennett",
    description="test",
    url='http://github.com',
    install_requires=get_install_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    include_package_data=True
)
