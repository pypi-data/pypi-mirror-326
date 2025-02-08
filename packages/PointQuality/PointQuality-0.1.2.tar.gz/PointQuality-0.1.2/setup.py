from setuptools import setup, find_packages

setup(
    name='PointQuality',
    version='0.1.2',
    description='Compute local and global quality metrics for comparing point clouds',
    author='David Fernandez Bonet',
    author_email='davferdz@gmail.com',
    url='https://github.com/DavidFernandezBonet/PointQuality',  # Update with your project URL
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'matplotlib',
        'networkx',
        'python-igraph',  # Ensure this is the correct package name on PyPI
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust license as needed
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
