from setuptools import setup, find_packages

setup(
    name='bpusdk',
    version='0.9',
    license='MIT',
    author="GDIIST",
    author_email='739503445@qq.com',
    packages=find_packages(),  # Include all packages inside 'src'
    install_requires=['brainpy>=2.4.2','brainpylib'],
)

