from setuptools import setup

setup(
    name='questionnaire',
    version='1.4.0',
    description='Elegant mini-DSL for creating command line questionnaires',
    long_description='Check it out on GitHub...',
    keywords='terminal gui pick question option',
    url='https://github.com/kylebebak/questionnaire',
    download_url='https://github.com/kylebebak/questionnaire/tarball/1.4.0',
    author='kylebebak',
    author_email='kylebebak@gmail.com',
    license='MIT',
    packages=['questionnaire'],
    install_requires=['pick==0.6.0'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ]
)
