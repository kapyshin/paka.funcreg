import setuptools


setuptools.setup(
    name="paka.funcreg",
    version="2.0.3",
    packages=setuptools.find_packages(),
    include_package_data=True,
    namespace_packages=["paka"],
    zip_safe=False,
    url="https://github.com/PavloKapyshin/paka.funcreg",
    keywords="registry",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"],
    license="BSD",
    author="Pavlo Kapyshin",
    author_email="i@93z.org")
