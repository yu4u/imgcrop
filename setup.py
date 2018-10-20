import setuptools
from pathlib import Path
from imgcrop import __version__

with open(Path(__file__).resolve().parent.joinpath("README.md"), "r") as f:
    long_description = f.read()

setuptools.setup(
    name="imgcrop",
    version=__version__,
    author="Yusuke Uchida",
    author_email="ren4yu@gmail.com",
    license="MIT",
    description="Simple image augmentation library focusing on random geometric cropping.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yu4u/imgcrop",
    packages=["imgcrop"],
    install_requires=["numpy", "opencv-python"],
    keywords=["augmentation", "image", "deep learning", "neural network", "machine learning"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
