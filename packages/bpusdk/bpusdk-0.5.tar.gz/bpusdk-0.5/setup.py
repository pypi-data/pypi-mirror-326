from setuptools import setup, find_packages

setup(
    name='bpusdk',
    version='0.5',
    license='MIT',
    author="GDIIST",
    author_email='739503445@qq.com',
    packages=find_packages(where='src'),  # Include all packages inside 'src'
    package_dir={'': 'src'},  # Map all packages to 'src'
    install_requires=['brainpy>=2.4.2'],
)
