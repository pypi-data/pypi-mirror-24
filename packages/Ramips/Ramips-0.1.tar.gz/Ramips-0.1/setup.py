from setuptools import setup, find_packages
import os

HERE = os.path.abspath(os.path.dirname(__file__))
def get_long_description():
    dirs = [ HERE ]
    if os.getenv("TRAVIS"):
        dirs.append(os.getenv("TRAVIS_BUILD_DIR"))

    long_description = ""

    for d in dirs:
        rst_readme = os.path.join(d, "README.rst")
        if not os.path.exists(rst_readme):
            continue

        with open(rst_readme) as fp:
            long_description = fp.read()
            return long_description

    return long_description

long_description = get_long_description()

version = '0.1'
setup(
    name="Ramips",
    version=version,
    description="Simple and opiniated way to build APIs in Python",
    long_description=long_description,
    keywords='Ramips',
    author='RamIdavalapati',
    author_email="ramidavalapati4568@gmail.com",
    url="https://github.com/chowdaryidavalapati/Ram",
    download_url="https://github.com/chowdaryidavalapati/Ram/archive/0.1.tar.gz",
    license='MIT License',
    install_requires=[
    ],
    package_dir={'Ramips': 'Ramips'},
    packages = ['Ramips'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ]
)
