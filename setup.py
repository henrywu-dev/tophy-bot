from setuptools import setup, find_packages

setup(
    name="tophy-bot",
    version="0.1.0",
    description="A cryptocurrency trading bot similar to freqtrade",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "ccxt>=4.0.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "python-dateutil>=2.8.2",
        "requests>=2.31.0",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "pytz>=2023.3",
        "ta>=0.10.2",
        "plotly>=5.16.1",
    ],
)
