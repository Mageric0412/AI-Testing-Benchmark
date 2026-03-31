from setuptools import setup, find_packages
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Python版本检查
python_version = sys.version_info
if python_version < (3, 10) or python_version >= (3, 13):
    raise RuntimeError(
        f"AI-Testing-Benchmark requires Python >= 3.10 and < 3.13. "
        f"当前版本: {python_version.major}.{python_version.minor}"
    )

setup(
    name="ai-testing-benchmark",
    version="1.0.0",
    author="AI Testing Team",
    author_email="ai-testing@example.com",
    description="Comprehensive evaluation framework for AI-guided cloud migration journey systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mageric0412/AI-Testing-Benchmark",
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
    python_requires=">=3.10,<3.13",
    install_requires=[
        # 核心依赖 - 版本受限以确保兼容性
        "pydantic>=2.0.0,<3.0.0",
        "pytest>=7.4.0,<9.0.0",
        "pandas>=2.0.0,<3.0.0",  # pandas 3.x 需要更多测试
        "numpy>=1.24.0,<2.0.0",
        "datasets>=2.14.0,<3.0.0",
        "requests>=2.31.0,<3.0.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.66.0",
        "loguru>=0.7.0,<1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0,<9.0.0",
            "pytest-asyncio>=0.21.0,<1.0.0",
            "pytest-cov>=4.1.0,<6.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0,<1.15.0",
        ],
        # LangTest集成 - 使用langtest>=2.0以获得Python 3.12支持
        "langtest": [
            "langtest>=2.0.0",
            "pandas>=2.0.0,<3.0.0",
        ],
        # RAGAS集成
        "ragas": [
            "ragas>=0.1.0",
        ],
        # TruLens集成
        "trulens": [
            "trulens>=0.2.0",
        ],
        # 公平性测试 - aif360和fairlearn需要较旧的包版本
        "fairness": [
            "aif360>=0.4.0,<1.0.0",
            "fairlearn>=0.8.0,<1.0.0",
            "scipy>=1.7.0,<2.0.0",
            "scikit-learn>=1.0.0,<2.0.0",
        ],
        # 完整安装 - 所有可选包
        "all": [
            "langtest>=2.0.0",
            "ragas>=0.1.0",
            "trulens>=0.2.0",
            "aif360>=0.4.0,<1.0.0",
            "fairlearn>=0.8.0,<1.0.0",
        ],
    },
)
