from setuptools import setup, find_packages

setup(
    name="bssqrcode",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["qrcode", "cryptography", "opencv-python"],
    author="Sumedh Patil",
    author_email="admin@aipresso.uk",
    description="Private advanced QR code generation with encryption and authentication.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh1599/bssqrcode",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
