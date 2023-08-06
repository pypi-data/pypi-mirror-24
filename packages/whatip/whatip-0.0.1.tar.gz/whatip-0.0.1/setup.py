import os

from setuptools import setup

ROOT = os.path.dirname(os.path.realpath(__file__))


setup(
    # Meta data
    name='whatip',
    version='0.0.1',
    author="Gregory Petukhov",
    author_email='lorien@lorien.name',
    maintainer="Gregory Petukhov",
    maintainer_email='lorien@lorien.name',
    url='https://github.com/lorien/whatip',
    description='Console script to find your IP',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    download_url='http://pypi.python.org/pypi/whatip',
    keywords="ip internet",
    license="MIT License",
    # Package files
    py_modules=['whatip'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'whatip = whatip:main',
        ],
    },
    # Topics
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        #'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
    ],
)
