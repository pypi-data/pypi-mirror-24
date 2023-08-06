from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
        name='NaiveDE',
        version='1.2.0',
        description='The most trivial DE test based on likelihood ratio tests',
        long_description=readme(),
        packages=find_packages(),
        install_requires=['numpy', 'scipy', 'pandas', 'tqdm'],
        author='Valentine Svensson',
        author_email='valentine@nxn.se',
        license='MIT'
    )
