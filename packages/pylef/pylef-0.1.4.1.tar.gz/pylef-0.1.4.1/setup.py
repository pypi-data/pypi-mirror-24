import os
import sys
import codecs

from setuptools import setup


version = '0.1.4.1'

HERE = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    readme = f.read()


setup_requires = ['pytest-runner'] if \
    {'pytest', 'test', 'ptr'}.intersection(sys.argv) else []

setup(
    name='pylef',
    version=version,
    author='Felippe Barbosa',
    author_email='felippe.barbosa@gmail.com',
    license='MIT v1.0',
    url='https://github.com/gwiederhecker/pylef',
    description='Python module for controlling isntruments and support IFGW LEF',
    long_description=readme,
    keywords='instrument control',
    packages=['pylef'],
    package_dir={'pylef': 'pylef'},
    ext_modules=[],
    provides=['pylef'],
    install_requires=['numpy', 'pyvisa', 'pandas', 'matplotlib'] + (['future']
                                  if sys.version_info.major < 3 else []),
    setup_requires=setup_requires,
    tests_require=[],
    platforms='OS Independent',
    classifiers=[
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Intended Audience :: Education',
        'Topic :: Education :: Computer Aided Instruction (CAI)'
    ],
    zip_safe=False,
    include_package_data=True)
