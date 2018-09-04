''' Setup the pyomdbapi project '''
import io
import setuptools

from omdb import (__version__, __author__, __license__, __email__,
                  __url__, __bugtrack_url__)

KEYWORDS = ['python', 'omdb', 'omdb-api', 'API']


def read_file(filepath):
    ''' read the file '''
    with io.open(filepath, 'r') as filepointer:
        res = filepointer.read()
    return res


setuptools.setup(
    name='pyomdbapi',  # mediawiki was taken
    version=__version__,
    author=__author__,
    author_email=__email__,
    description='OMDB API python wrapper',
    license=__license__,
    keywords=' '.join(KEYWORDS),
    url=__url__,
    download_url='{0}/tarball/v{1}'.format(__url__, __version__),
    bugtrack_url=__bugtrack_url__,
    install_requires=read_file('./requirements/python').splitlines(),
    packages=['omdb'],
    long_description=read_file('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Topic :: Internet',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
