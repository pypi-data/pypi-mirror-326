from setuptools import setup, find_packages

setup(
    name="tamida",  # Tên thư viện trên PyPI
    version="0.1.0",  # Phiên bản
    author="Đặng Minh Tài",
    author_email="dmt826321@gmail.com",
    description="Một thư viện toán học hỗ trợ số chính phương, số nguyên tố, giai thừa, ...",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dangminhtai/", 
    packages=find_packages(),
    install_requires=[
        "scipy"  # Thêm các thư viện cần thiết
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
