from setuptools import setup

setup(
    name='losswise',
    version='0.86',
    description='Official Losswise library for Python',
    long_description=open('README.rst').read(),
    url='https://losswise.com',
    author='Losswise, Inc.',
    author_email='nicodjimenez@gmail.com',
    license='Apache',
    install_requires=['requests >= 2.9.1', 'six >= 1.9.0'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2'
    ],

    keywords='losswise analytics dashboard deep machine learning tensorflow pytorch optimization ML deep learning',
    packages=['losswise'],
)

