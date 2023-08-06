# chardet's setup.py
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
setup(
    name = "globee",
    packages = ["bitpay"],
    version = "2.3.3",
    description = "Accept altcoins with GloBee",
    author = "GloBee Integrations Team",
    author_email = "integrations@globee.com",
    url = "https://github.com/GloBee-Official/bitpay-python",
    download_url = "https://github.com/GloBee-Official/bitpay-python/tarball/v2.3.3",
    keywords = ["bitcoin", "payments", "crypto", "altcoins"],
    install_requires = ["requests", "ecdsa"],
    classifiers = [
"Programming Language :: Python :: 3.4",
"Programming Language :: Python :: 3 :: Only",
"Development Status :: 5 - Production/Stable",
"Environment :: Web Environment",
"Intended Audience :: Developers",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
"Topic :: Software Development :: Libraries :: Python Modules",
"Topic :: Office/Business :: Financial"
],
    long_description = """\
Python Library for integrating with GloBee
-------------------------------------

This library is a simple way to integrate your application with
GloBee for accepting bitcoin & altcoin payments. It exposes three basic
functions, authenticating with globee, creating invoices,
and retrieving invoices. It is not meant as a replacement for 
the entire GloBee API. However, the key_utils module contains
all of the tools you need to use the BitPay API for other
purposes.

This version requires Python 3 or later; a Python 2 version is available separately.
"""
)
