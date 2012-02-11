import re

from setuptools import setup

version = None
for line in open('./soundcloud/__init__.py'):
    m = re.search('__version__\s*=\s*(.*)', line)
    if m:
        version = m.group(1).strip()[1:-1]  # quotes
        break
assert version

setup(
    name='soundcloud',
    version=version,
    description='A friendly wrapper library for the Soundcloud API',
    author='Paul Osman',
    author_email='osman@soundcloud.com',
    url='https://github.com/soundcloud/soundcloud-python',
    license='BSD',
    packages=['soundcloud'],
    include_package_data=True,
    package_data={
        '': ['README.rst']
    },
    install_requires=[
        'nose==1.1.2',
        'fudge==1.0.3',
        'requests==0.10.1',
        'simplejson>=2.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
