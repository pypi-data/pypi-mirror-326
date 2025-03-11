from setuptools import setup, find_packages

setup(
    name='bpusdk',
    version='0.6',
    license='MIT',
    author="GDIIST",
    author_email='739503445@qq.com',
    packages=find_packages(where='bpusdk'),  # Include all packages inside 'src'
    package_dir={'': 'bpusdk'},  # Map all packages to 'src'
    install_requires=['brainpy>=2.4.2','brainpylib'],
)

