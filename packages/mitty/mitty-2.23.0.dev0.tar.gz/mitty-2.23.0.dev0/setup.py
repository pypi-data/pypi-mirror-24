from setuptools import setup, find_packages

__version__ = eval(open('mitty/version.py').read().split('=')[1])
setup(
  name='mitty',
  version=__version__,
  description='Simulator for genomic data',
  author='Seven Bridges Genomics',
  author_email='kaushik.ghose@sbgdinc.com',
  url='https://github.com/sbg/Mitty',
  download_url='https://github.com/sbg/Mitty/archive/development.zip',
  keywords=['simulator', 'genomics', 'ngs', 'read mapper', 'aligner', 'variant caller'],
  classifiers=[
    # How mature is this project? Common values are
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: Apache Software License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.4',
  ],
  python_requires='>=3.4',
  packages=find_packages(include=['mitty*']),
  include_package_data=True,
  entry_points={'console_scripts': ['mitty = mitty.cli:cli']},
  install_requires=[
    'cython',
    'setuptools>=24.3.0',
    'numpy>=1.11.0',
    'click>=3.3',
    'pysam==0.10.0',
    'matplotlib>=1.3.0',
    'scipy',
    'nose'
  ],
  test_suite='nose.collector',
  tests_require=['nose'],
)