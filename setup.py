"""
实现包在全局导入
"""
from setuptools import setup,find_packages

setup(
    name="deeptracer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cozepy>=0.20.0",
        "python-dotenv>=1.2.1",
    ],
    test_suite="test",
)