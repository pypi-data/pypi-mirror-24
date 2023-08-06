from setuptools import setup

setup(
    name='pagespeedwrapper',
    version='0.1.1',
    description='Easily get Google PageSpeed results',
    author='Peter W',
    author_email='peter@svrrack.com',
    license='MIT',
    packages=['pagespeedwrapper'],
    install_requires=['requests'],
    zip_safe=False
)