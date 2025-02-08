from setuptools import setup, find_packages

# Read README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="code-combiner-rag",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=5.1",
    ],
    entry_points={
        'console_scripts': [
            'code-combiner=code_combiner.main:main',
        ],
    },
    author="Vishal Agrawal",
    author_email="vishal18593@gmail.com",
    description="A tool to combine code files into a single file for RAG pipelines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bazinga012/code-combiner-rag",
    project_urls={
        "Bug Tracker": "https://github.com/bazinga012/code-combiner-rag/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.10",
    keywords="code, combine, rag, llm, ai, machine learning, code-embedding",
)