from setuptools import setup

from better_contextvars import __version__ as version

with open('README.rst') as f:
    readme = f.read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='better-contextvars',
    version=version,
    url='https://github.com/itsVale/better-contextvars',
    description='PEP 567, but compatible to lower Python versions.',
    long_description=readme,
    author='Valentin B.',
    packages=['better_contextvars'],
    provides=['better_contextvars'],
    install_requires=requirements,
    license='MIT',
    include_package_data=True,
    test_suite='tests.suite',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
    ],
)
