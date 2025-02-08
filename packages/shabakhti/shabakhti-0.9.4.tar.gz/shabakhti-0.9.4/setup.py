from setuptools import setup, find_packages

setup(
    name="shabakhti",
    version="0.9.4",
    packages=find_packages(),
    install_requires=[
        "requests",  # مثال: اگر پکیج requests لازم دارید
        "pyttsx3",     # مثال: اگر پکیج numpy لازم دارید
    ],
    author="Mohammad Mahdi Shabakhti",
    description="Weather package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mohammadlegend",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
