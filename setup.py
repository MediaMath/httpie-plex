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
    name='httpie-plex-auth',
    description='Auth plugin for HTTPie for MediaMath\'s Bid Opportunity Firehose.',
    long_description=fread('README.rst'),
    version='0.1.0',
    author='Prasanna Swaminathan',
    author_email='prasanna@mediamath.com',
    license=fread('LICENSE'),
    url='https://github.com/pswaminathan/httpie-plex-auth',
    download_url='https://github.com/pswaminathan/httpie-plex-auth',
    py_modules=['httpie_plex_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_plex_auth = httpie_plex_auth:PlexAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0',
        'requests-oauthlib>=0.3.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
