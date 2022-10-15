import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ippanel",
    version="2.0.7",
    author="Asghar Dadashzadeh",
    author_email="dev@ippanel.com",
    description="ippanel sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ippanel/python-rest-sdk",
    packages=setuptools.find_packages(),
    install_requires=['requests>=2.28.1'],
    license='BSD-2-Clause',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ]
)
