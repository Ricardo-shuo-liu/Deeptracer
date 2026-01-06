"""
实现包在全局导入
"""
from setuptools import setup,find_packages

setup(
    name="deeptracer",
    version="0.1.0",
    packages=find_packages(),
    install_requires = [
        "cozepy>=0.20.0",
        "python-dotenv>=1.2.1",
        "objprint>=0.3.0",
        "memray>=1.19.1 ",
        "tqdm>=4.67.1",
        "pyvis>=0.3.2",
        "networkx>=3.4.2"
    ],
    test_suite = "test"
)