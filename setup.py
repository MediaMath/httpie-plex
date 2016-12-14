from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def fread(fname):
    with open(os.path.join(CURRENT_DIR, fname)) as f:
        return f.read()


setup(
    name='httpie-plex',
    description='Auth plugin for HTTPie for MediaMath\'s Bid Opportunity '
                'Firehose.',
    long_description=fread('README.rst'),
    version='1.0.0',
    author='Prasanna Swaminathan',
    author_email='prasanna@mediamath.com',
    license=fread('LICENSE'),
    url='https://github.com/MediaMath/httpie-plex',
    download_url='https://github.com/MediaMath/httpie-plex',
    py_modules=['httpie_plex'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_plex = httpie_plex:PlexAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.9.2',
        'requests-oauthlib>=0.3.2',
    ],
    test_suite="test_httpie_plex",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
