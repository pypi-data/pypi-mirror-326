from setuptools import setup, find_packages

setup(
    name='ProxiGraph',
    version='0.1.2',
    description='Generate proximity graphs from point clouds with various modes and export formats.',
    author='David Fernandez Bonet',
    author_email='davferdz@gmail.com',
    url='https://github.com/DavidFernandezBonet/proxigraph',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0,<2.0.0',
        'scipy>=1.7.0,<2.0.0',
        'pandas>=1.3.0,<2.0.0',
        'matplotlib>=3.4.0,<4.0.0',
        'networkx>=2.6.0,<3.0.0',
        'scikit-learn>=1.2.2,<2.0.0',
        'seaborn>=0.11.0,<1.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)