from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-testing-benchmark",
    version="1.0.0",
    author="AI Testing Team",
    author_email="ai-testing@example.com",
    description="Comprehensive evaluation framework for AI-guided cloud migration journey systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/AI-Testing-Benchmark",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.0.0",
        "pytest>=7.4.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "datasets>=2.14.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.66.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
        ],
        "langtest": ["langtest>=1.0.0"],
        "ragas": ["ragas>=0.1.0"],
        "trulens": ["trulens>=0.2.0"],
        "fairness": ["aif360>=0.4.0", "fairlearn>=0.8.0"],
    },
)
