from setuptools import setup

setup(
    name="deaddrop_meta",
    version="0.0.6",
    description="Meta class definitions for the DeadDrop architecture",
    url="https://github.com/unr-deaddrop/deaddrop_meta",
    author="lgactna",
    author_email="lgonzalesna@gmail.com",
    license="BSD 2-clause",
    packages=["deaddrop_meta"],
    package_data={"deaddrop_meta": ["py.typed"]},
    install_requires=["pydantic"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.11",
    ],
)
