from setuptools import setup

import soundcloud

setup(
    name='soundcloud',
    version=soundcloud.__version__,
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
    setup_requires=[
        'nose==1.1.2',
        'fudge==1.0.3',
        'requests==0.10.1',
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
