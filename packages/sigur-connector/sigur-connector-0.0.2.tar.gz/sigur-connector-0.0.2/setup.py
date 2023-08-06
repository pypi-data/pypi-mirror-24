try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='sigur-connector',
    version='0.0.2',
    author='GlebZaytsev',
    author_email='winter1silent@gmail.com',
    url='https://bitbucket.org/wintersilent/sigur_connector',
    description='Sigur TCP wrapper',
    download_url='https://bitbucket.org/wintersilent/sigur_connector/get/master.zip',
    license='MIT',

    packages=['sigur'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)