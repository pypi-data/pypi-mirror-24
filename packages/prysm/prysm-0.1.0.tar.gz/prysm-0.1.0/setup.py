from setuptools import setup

setup(
    name='prysm',
    version='0.1.0',
    description='A python optics module',
    long_description='Uses geometric and fourier optics to model optical systems',
    license='MIT',
    author='Brandon Dube',
    author_email='brandondube@gmail.com',
    url='https://github.com/brandondube/prysm',
    packages=['prysm'],
    install_requires=['numpy', 'matplotlib', 'scipy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]
)
