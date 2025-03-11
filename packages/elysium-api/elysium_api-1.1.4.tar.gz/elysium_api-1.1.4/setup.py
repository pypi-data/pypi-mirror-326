from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="elysium-api",
    version="1.1.4",
    description="API moderna e futurista para integração com o sistema Elysium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Elysium API",
    author_email="contato@elysiumx.com.br",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dateutil>=2.8.2"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications",
    ],
    keywords="elysium, api, mensagens, clientes, planos",
    python_requires=">=3.8",
)