from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="rpa-arc",
    version="0.3",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rpa-arc=rpa_arc.cli:main',
        ],
    },
     install_requires=[
        'colorama',
    ],
    author="Luis Costa",
     description="Ferramenta CLI para criar estrutura de projetos RPA.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)