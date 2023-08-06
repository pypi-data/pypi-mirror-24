from setuptools import find_packages, setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='myprojectdydy',
    version='0.0.2',
    description='optimizers',
    long_description=readme(),
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/DoyeobYeo/MyProject',
    license='MIT',
    author='DoyeobYeo',
    author_email='greatday87@gmail.com',
    install_requires=['numpy>=1.11.2','matplotlib>=1.5.3'],
    keywords=['LASSO','Group','GroupLASSO'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Mathematics'
    ]
)
